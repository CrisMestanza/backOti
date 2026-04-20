from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def getUser(request):
    query = f"""
        SELECT TOP 10 anu.* FROM [UNSM.SIGAU.DB].dbo.AspNetUsers AS anu
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        
    return Response({"data": result})


@api_view(['GET'])
@permission_classes([AllowAny])
def getPagos(request, dni):
    
    # Obtener Estudiante
    queryAnu = f"""
        SELECT anu.* FROM [UNSM.SIGAU.DB].dbo.AspNetUsers AS anu
        where anu.UserName = '{dni}'
    """
    with connection.cursor() as cursor:
        cursor.execute(queryAnu)
        resultAnu = cursor.fetchall()

    querypayments = f"""
        select*from EconomicManagement.Payments p 
        where p.UserId  = '{resultAnu[0][0]}'
        AND  p.status = 1
    """
    with connection.cursor() as cursor:
        cursor.execute(querypayments)
        resultPayments = cursor.fetchall()
        
    return Response({"data": resultPayments})


@api_view(['POST'])
@permission_classes([AllowAny])
def deletePagos(request, id):
    
    querypayments = f"""
        delete from EconomicManagement.Payments p 
        where p.Id = '{id}'
    """
    with connection.cursor() as cursor:
        cursor.execute(querypayments)
        resultPayments = cursor.fetchall()
        
    return Response({"data": resultPayments})
