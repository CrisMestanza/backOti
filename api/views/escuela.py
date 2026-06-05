from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def getEscuelas(request):

    query = """
        select*from Generals.Careers c 
    """

    with connection.cursor() as cursor:
        cursor.execute(query)

        columns = [col[0] for col in cursor.description]  
        rows = cursor.fetchall()

        # convertir a lista de diccionarios
        result = [
            dict(zip(columns, row))
            for row in rows
        ]

    return Response({"data": result})

@api_view(['GET'])
@permission_classes([AllowAny])
def getEscuelasPorNombre(request,nombre):

    query = """
        select*from Generals.Careers c 
        where c.Name = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query,[nombre])

        columns = [col[0] for col in cursor.description]  
        rows = cursor.fetchall()

        # convertir a lista de diccionarios
        result = [
            dict(zip(columns, row))
            for row in rows
        ]

    return Response({"data": result})