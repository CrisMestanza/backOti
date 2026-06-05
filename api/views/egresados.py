from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def getEgresados(request):

    query = """
        SELECT TOP 20 anu.PaternalSurname, anu.MaternalSurname, anu.Name ,anu.Email, anu.PhoneNumber , 
        c.Name as 'Escuela Profesional', f.Name as 'Facultad', t.EndDate as 'Fecha de Egreso', t.Name as 'Semestre de egreso'
        FROM Generals.Students s 
        inner join Enrollment.Terms t on s.GraduationTermId = t.Id 
        inner join AspNetUsers anu on s.UserId = anu.Id 
        inner join Generals.Careers c on s.CareerId = c.Id
        inner join Enrollment.Faculties f on c.FacultyId = f.Id 
        where anu.[Type] ='1'
        order by t.EndDate desc
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
def getEgresado(request, dni):

    query = """
        SELECT anu.PaternalSurname, anu.MaternalSurname, anu.Name ,anu.Email, anu.PhoneNumber , 
        c.Name as 'Escuela Profesional', f.Name as 'Facultad', t.EndDate as 'Fecha de Egreso', t.Name as 'Semestre de egreso'
        FROM Generals.Students s 
        inner join Enrollment.Terms t on s.GraduationTermId = t.Id 
        inner join AspNetUsers anu on s.UserId = anu.Id 
        inner join Generals.Careers c on s.CareerId = c.Id
        inner join Enrollment.Faculties f on c.FacultyId = f.Id 
        where anu.Dni =%s  and anu.[Type] ='1'
        order by t.EndDate desc
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [dni])

        columns = [col[0] for col in cursor.description]  
        rows = cursor.fetchall()

        # convertir a lista de diccionarios
        result = [
            dict(zip(columns, row))
            for row in rows
        ]

    return Response({"data": result})