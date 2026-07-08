from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(["GET"])
@permission_classes([AllowAny])
def getPeriodoTerm(request):    
    query = """
    select top 5 *from Admission.ApplicationTerms 
    order by Admission.ApplicationTerms.CreatedAt desc
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    reportes = [dict(zip(columns, row)) for row in rows]
    
    return Response(reportes)


@api_view(["GET"])
@permission_classes([AllowAny])
def getBoletas(request, idTerm, dni):
    query = """
    SELECT
        CONCAT(i.Series, '-', i.Number) AS 'RECIBO DE PAGO',
        i.ClientName AS 'Cliente',
        i.Dni AS 'Doc. Ident. No mostrar',
        p.Address AS 'Direc.',
        CONVERT(VARCHAR(10), CAST(i.[Date] AS DATETIME), 103) AS 'Fecha Emis.',
        LEFT(CONVERT(VARCHAR(8), DATEADD(HOUR, -5, i.[Date]), 108), 5) AS 'Hora',
        'Moneda: Soles' AS 'Moneda',
        p2.Description AS 'Descripcion',
        id.Quantity AS 'Cantidad',
        'UND' AS 'Unidad',
        id.SubTotal AS 'Precio',
        id.Total AS 'Total',
        i.Subtotal AS 'Sub.Total',
        i.TotalAmount AS 'TOTAL S/',
        CONCAT('En Efectivo: ', i.TotalAmount) AS 'Efectivo',
        i.CreatedBy AS 'Usuario'
    FROM Admission.Postulants p
    INNER JOIN EconomicManagement.Payments p2 ON p.Id = p2.EntityId
    INNER JOIN Intranet.Invoices i ON p2.InvoiceId = i.Id
    INNER JOIN Admission.ApplicationTerms t ON p.ApplicationTermId = t.Id
    INNER JOIN Enrollment.Terms t2 ON t.TermId = t2.Id
    INNER JOIN Intranet.InvoiceDetails id ON i.Id = id.InvoiceId
    WHERE p.PaidAdmission = '1'
        AND p.Document = %s
        AND i.Annulled != '1'
        AND t.Id = %s
    ORDER BY p.CreatedAt DESC
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [dni, idTerm])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    print(idTerm, dni)
    reportes = [dict(zip(columns, row)) for row in rows]

    return Response(reportes)

