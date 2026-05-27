import io
import pdfplumber
import pandas as pd
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse


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


def _generar_pdf(df):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle("titulo", parent=styles["Title"], fontSize=16, spaceAfter=6)
    subtitulo_style = ParagraphStyle("subtitulo", parent=styles["Normal"], fontSize=12, spaceAfter=12, alignment=1)
    cell_style = ParagraphStyle("cell", parent=styles["Normal"], fontSize=7.5, leading=10, wordWrap="CJK")

    story = [
        Paragraph("UNIVERSIDAD NACIONAL DE SAN MARTÍN", titulo_style),
        Paragraph("CAJA", subtitulo_style),
        Spacer(1, 0.3 * cm),
    ]

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

    col_widths = [3.2 * cm, 2.2 * cm, 5.0 * cm, 8.5 * cm, 2.2 * cm, 2.5 * cm]
    tabla = Table(data, colWidths=col_widths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), colors.HexColor("#1F3864")),
        ("TEXTCOLOR",   (0, 0), (-1, 0), colors.white),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0), 8),
        ("ALIGN",       (0, 0), (-1, 0), "CENTER"),
        ("VALIGN",      (0, 0), (-1, 0), "MIDDLE"),
        ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 1), (-1, -1), 7.5),
        ("VALIGN",      (0, 1), (-1, -1), "MIDDLE"),
        ("ALIGN",       (4, 1), (4, -1), "RIGHT"),
        *[("BACKGROUND", (0, i), (-1, i), colors.HexColor("#EBF0FA")) for i in range(2, len(data) - 1, 2)],
        ("GRID",        (0, 0), (-1, -1), 0.4, colors.HexColor("#AAAAAA")),
        ("BACKGROUND",  (0, -1), (-1, -1), colors.HexColor("#D9E1F2")),
        ("FONTNAME",    (0, -1), (-1, -1), "Helvetica-Bold"),
        ("LINEABOVE",   (0, -1), (-1, -1), 1, colors.HexColor("#1F3864")),
    ]))

    story.append(tabla)
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

    df_ordenado = _ordenar_filas(filas)
    pdf_buffer = _generar_pdf(df_ordenado)

    response = HttpResponse(pdf_buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="caja_ordenado.pdf"'
    response["Access-Control-Expose-Headers"] = "Content-Disposition"
    return response
