import io
import re
import pdfplumber
import pandas as pd

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

from .ordenarpdf import _extraer_fecha_caja, _extraer_cajero, _generar_pdf

# Comprobantes tipo "Z001-00031732", "V001-00012345", etc. (prefijo + guion + correlativo)
NRO_REGEX = re.compile(r'^[A-Za-z]+\d*-\d+$')

N_COLUMNAS = 6
COLUMNAS = ["NRO", "FECHA_EMISION", "NOMBRE", "CONCEPTO", "ENTRADA", "TIPO_PAGO"]


def _extraer_filas(pdf_bytes):
    filas = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables() or []:
                for row in table:
                    if not row or not row[0]:
                        continue
                    nro = re.sub(r'\s+', '', str(row[0]))
                    if not NRO_REGEX.match(nro):
                        continue
                    fila = list(row)
                    fila[0] = nro
                    if len(fila) < N_COLUMNAS:
                        fila += [""] * (N_COLUMNAS - len(fila))
                    elif len(fila) > N_COLUMNAS:
                        fila = fila[:N_COLUMNAS]
                    filas.append(fila)
    return filas


def _ordenar_filas(filas):
    df = pd.DataFrame(filas, columns=COLUMNAS)
    df["NRO"] = df["NRO"].astype(str).str.strip()
    df["FECHA_EMISION"] = df["FECHA_EMISION"].astype(str).str.strip()
    df["_FECHA_ORDEN"] = pd.to_datetime(df["FECHA_EMISION"], format="%d/%m/%Y", errors="coerce")
    df = df.sort_values(["_FECHA_ORDEN", "NRO"], na_position="last")
    return df.drop(columns="_FECHA_ORDEN").reset_index(drop=True)


@api_view(["POST"])
@parser_classes([MultiPartParser])
def ordenar_pdf_fecha(request):
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
    response["Content-Disposition"] = 'attachment; filename="caja_ordenado_por_fecha.pdf"'
    response["Access-Control-Expose-Headers"] = "Content-Disposition"
    return response
