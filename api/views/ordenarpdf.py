import io
import os
import re
import pdfplumber
import pandas as pd
from reportlab.lib.pagesizes import A4
from PIL import Image as PILImage
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

FECHA_REGEX = re.compile(r'\d{1,2}\s+de\s+[A-Za-zÁÉÍÓÚáéíóúñÑ]+\s+del\s+\d{4}', re.IGNORECASE)

LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "logo_unsm.png")
VERDE_UNSM = colors.HexColor("#15803d")


def _extraer_filas(pdf_bytes):
    filas = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables() or []:
                for row in table:
                    if not row or not row[0]:
                        continue
                    nro = str(row[0]).strip()
                    if nro.startswith("V"):
                        filas.append(row)
    return filas


def _ordenar_filas(filas):
    df = pd.DataFrame(filas, columns=["NRO", "FECHA_EMISION", "NOMBRE", "CONCEPTO", "ENTRADA", "TIPO_PAGO"])
    df["NRO"] = df["NRO"].astype(str).str.strip()
    return df.sort_values("NRO").reset_index(drop=True)


def _extraer_fecha_caja(pdf_bytes):
    """Busca en la primera página del PDF original una fecha con formato 'dd de mes del yyyy'."""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            texto = pdf.pages[0].extract_text() or ""
        match = FECHA_REGEX.search(texto)
        return match.group(0) if match else ""
    except Exception:
        return ""


def _extraer_cajero(pdf_bytes):
    """Toma la última línea de texto no vacía de la última página como nombre del cajero (línea de firma)."""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            texto = pdf.pages[-1].extract_text() or ""
        lineas = [l.strip() for l in texto.split("\n") if l.strip()]
        if not lineas:
            return ""
        candidata = lineas[-1]
        if any(ch.isdigit() for ch in candidata):
            return ""
        return candidata
    except Exception:
        return ""


def _generar_pdf(df, fecha_caja="", cajero=""):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=2 * cm,
    )
    ancho_disponible = doc.width

    styles = getSampleStyleSheet()
    nombre_uni_style = ParagraphStyle(
        "nombre_uni", parent=styles["Normal"], fontSize=13, leading=14.5,
        fontName="Helvetica-Bold", textColor=VERDE_UNSM,
    )
    titulo_style = ParagraphStyle(
        "titulo", parent=styles["Title"], fontSize=22, textColor=colors.black,
        fontName="Times-Bold", alignment=0,
    )
    subtitulo_style = ParagraphStyle(
        "subtitulo", parent=styles["Normal"], fontSize=14, textColor=colors.black,
        fontName="Times-Roman", alignment=2,
    )
    cell_style = ParagraphStyle(
        "cell", parent=styles["Normal"], fontSize=7.5, leading=10,
        wordWrap="CJK", textColor=colors.black,
    )
    firma_style = ParagraphStyle(
        "firma", parent=styles["Normal"], fontSize=10, alignment=1, textColor=colors.black,
    )

    story = []

    # --- Cabecera: logo institucional + nombre de la universidad (estilo oficial) ---
    try:
        ancho_logo = 1.4 * cm
        with PILImage.open(LOGO_PATH) as img_pil:
            img_w, img_h = img_pil.size
        alto_logo = ancho_logo * (img_h / img_w) if img_w else ancho_logo

        logo_img = RLImage(LOGO_PATH, width=ancho_logo, height=alto_logo)

        barra = Table([[""]], colWidths=[0.05 * cm], rowHeights=[alto_logo])
        barra.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), VERDE_UNSM),
        ]))

        texto_uni = Paragraph("UNIVERSIDAD NACIONAL<br/>DE SAN MARTÍN", nombre_uni_style)

        fila_logo = [[logo_img, barra, texto_uni]]
        tabla_logo = Table(
            fila_logo,
            colWidths=[ancho_logo + 0.25 * cm, 0.4 * cm, ancho_disponible - ancho_logo - 0.65 * cm],
        )
        tabla_logo.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (0, 0), 0),
            ("RIGHTPADDING", (1, 0), (1, 0), 0),
            ("LEFTPADDING", (2, 0), (2, 0), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(tabla_logo)
    except Exception:
        story.append(Paragraph("UNIVERSIDAD NACIONAL DE SAN MARTÍN", nombre_uni_style))

    story.append(Spacer(1, 0.5 * cm))

    # --- Título CAJA + fecha ---
    fila_titulo = [[Paragraph("CAJA", titulo_style), Paragraph(fecha_caja, subtitulo_style)]]
    tabla_titulo = Table(fila_titulo, colWidths=[ancho_disponible * 0.5, ancho_disponible * 0.5])
    tabla_titulo.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(tabla_titulo)
    story.append(Spacer(1, 0.4 * cm))

    data = [["NRO", "FECHA\nEMISIÓN", "NOMBRE", "CONCEPTO", "ENTRADA", "TIPO PAGO"]]
    total = 0.0

    for _, row in df.iterrows():
        entrada_str = str(row["ENTRADA"]).replace(",", ".").strip() if row["ENTRADA"] else "0"
        try:
            total += float(entrada_str)
        except ValueError:
            pass
        data.append([
            Paragraph(str(row["NRO"]), cell_style),
            Paragraph(str(row["FECHA_EMISION"]).strip(), cell_style),
            Paragraph(str(row["NOMBRE"]).strip(), cell_style),
            Paragraph(str(row["CONCEPTO"]).strip(), cell_style),
            Paragraph(entrada_str, cell_style),
            Paragraph(str(row["TIPO_PAGO"]).strip(), cell_style),
        ])

    data.append(["", "", "", Paragraph("<b>TOTAL</b>", cell_style),
                  Paragraph(f"<b>{total:,.2f}</b>", cell_style), ""])

    fracciones_col = [0.145, 0.10, 0.19, 0.335, 0.10, 0.13]
    col_widths = [ancho_disponible * f for f in fracciones_col]
    tabla = Table(data, colWidths=col_widths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), colors.black),
        ("TEXTCOLOR",   (0, 0), (-1, 0), colors.white),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0), 8),
        ("ALIGN",       (0, 0), (-1, 0), "CENTER"),
        ("VALIGN",      (0, 0), (-1, 0), "MIDDLE"),
        ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 1), (-1, -1), 7.5),
        ("VALIGN",      (0, 1), (-1, -1), "MIDDLE"),
        ("ALIGN",       (4, 1), (4, -1), "RIGHT"),
        ("TEXTCOLOR",   (0, 1), (-1, -1), colors.black),
        *[("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F2F2F2")) for i in range(2, len(data) - 1, 2)],
        ("GRID",        (0, 0), (-1, -1), 0.4, colors.black),
        ("BACKGROUND",  (0, -1), (-1, -1), colors.HexColor("#E0E0E0")),
        ("FONTNAME",    (0, -1), (-1, -1), "Helvetica-Bold"),
        ("LINEABOVE",   (0, -1), (-1, -1), 1, colors.black),
    ]))

    story.append(tabla)

    # --- Firma del cajero, al final del documento ---
    if cajero:
        story.append(Spacer(1, 1.8 * cm))
        story.append(Paragraph("_" * 40, firma_style))
        story.append(Paragraph(cajero, firma_style))

    doc.build(story)
    buffer.seek(0)
    return buffer


@api_view(["POST"])
@parser_classes([MultiPartParser])
def ordenar_pdf(request):
    archivo = request.FILES.get("pdf")
    if not archivo:
        return Response({"error": "No se recibió ningún archivo PDF."}, status=status.HTTP_400_BAD_REQUEST)

    if not archivo.name.lower().endswith(".pdf"):
        return Response({"error": "El archivo debe ser un PDF."}, status=status.HTTP_400_BAD_REQUEST)

    pdf_bytes = archivo.read()
    filas = _extraer_filas(pdf_bytes)

    if not filas:
        return Response({"error": "No se encontraron filas válidas en el PDF."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    fecha_caja = _extraer_fecha_caja(pdf_bytes)
    cajero = _extraer_cajero(pdf_bytes)

    df_ordenado = _ordenar_filas(filas)
    pdf_buffer = _generar_pdf(df_ordenado, fecha_caja, cajero)

    response = HttpResponse(pdf_buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="caja_ordenado.pdf"'
    response["Access-Control-Expose-Headers"] = "Content-Disposition"
    return response
