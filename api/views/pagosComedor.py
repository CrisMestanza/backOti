from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def getUser(request):

    query = """
        SELECT TOP 10 anu.*
        FROM [UNSM.SIGAU.DB].dbo.AspNetUsers AS anu
    """

    with connection.cursor() as cursor:
        cursor.execute(query)

        columns = [col[0] for col in cursor.description]  # 🔹 nombres de columnas
        rows = cursor.fetchall()

        # convertir a lista de diccionarios
        result = [
            dict(zip(columns, row))
            for row in rows
        ]

    return Response({"data": result})


# Un unico estudiante por dni

@api_view(['GET'])
@permission_classes([AllowAny])
def getStudentDni(request, dni):

    queryAnu = """
        SELECT anu.* 
        FROM [UNSM.SIGAU.DB].dbo.AspNetUsers AS anu
        WHERE anu.UserName = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(queryAnu, [dni])

        columns = [col[0] for col in cursor.description]  # 🔹 nombres de columnas
        row = cursor.fetchone()

    #  Si no existe
    if not row:
        return Response({"error": "Usuario no encontrado"}, status=404)

    #  Convertir a diccionario
    resultAnu = dict(zip(columns, row))

    return Response({"data": resultAnu})


@api_view(['GET'])
@permission_classes([AllowAny])
def getPagos(request, dni):

    # 🔹 Obtener usuario de forma segura
    queryAnu = """
        SELECT anu.* 
        FROM [UNSM.SIGAU.DB].dbo.AspNetUsers AS anu
        WHERE anu.UserName = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(queryAnu, [dni])
        resultAnu = cursor.fetchone()

    # Validar si no existe
    if not resultAnu:
        return Response({"error": "Usuario no encontrado"}, status=404)

    user_id = resultAnu[0]

    # Obtener pagos
    querypayments = """
        SELECT *
        FROM EconomicManagement.Payments p
        WHERE p.UserId = %s
        AND p.status = 1
        AND p.ConceptId = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(querypayments, [user_id, '08DA9015-566B-446D-84ED-FD2279F87BD2'])
        
        columns = [col[0] for col in cursor.description]  # 👈 nombres de columnas
        rows = cursor.fetchall()

        # Convertir a diccionario
        resultPayments = [
            dict(zip(columns, row))
            for row in rows
        ]

    return Response({"data": resultPayments})


@api_view(['DELETE'])
@permission_classes([AllowAny])
def deletePagos(request, id):
    # Eliminamos el alias 'p' y la referencia 'p.Id'
    querypayments = """
        DELETE FROM EconomicManagement.Payments 
        WHERE Id = %s AND  status = 1
    """
    
    with connection.cursor() as cursor:
        # Pasamos el id como parámetro para evitar errores de sintaxis y seguridad
        cursor.execute(querypayments, [id])
        
    return Response({"message": "Registro eliminado con éxito"})