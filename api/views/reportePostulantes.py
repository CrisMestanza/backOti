from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny




@api_view(["GET"])
@permission_classes([AllowAny])
def getApplicationTerms(request, idTerm):    
    query = """
    SELECT at.Id, at.Name, t.Name as Periodo  FROM [UNSM.SIGAU.DB].Admission.ApplicationTerms AS at
    inner join [UNSM.SIGAU.DB].Enrollment.Terms AS t on t.Id = at.TermId 
    where at.TermId   =  %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [idTerm])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    reportes = [dict(zip(columns, row)) for row in rows]
    
    return Response(reportes)

@api_view(["GET"])
@permission_classes([AllowAny])
def generarReportes(request, idApplicationTerm):
    
    query = """
        select 
            p.Name,
            p.PaternalSurname,
            p.MaternalSurname,
            p.DocumentType,
            p.Document,
            p.Code,
            case p.sex 
                when 1 then 'Masculino'
                when 2 then 'Femenino'
            end as Sexo,
            c.Name as Procedencia,
            p.BirthDate as FechaNacimiento,
            DATEDIFF(YEAR, p.BirthDate, GETDATE()) as Edad,
            case p.MaritalStatus 
                when 1 then 'Soltero'
                when 2 then 'Casado'
                when 3 then 'Divorciado'
                when 4 then 'Viudo'
            end as EstadoCivil,
            p.Childrens as NumeroHijos,
            c.Name as Pais,
            d.Name as DepartamentoNacimiento,
            pv.Name as ProvinciaNacimiento,
            dt.Name as DistritoNacimiento,
            d2.Name as DepartamentoResidencia,
            pv2.Name as ProvinciaResidencia,
            dt2.Name as DistritoResidencia,
            p.Address,
            p.Email,
            p.Phone1,
            p.Phone2,
            p.WorkingCurrently as SeEncuentraTrabajando,
            p.Occupation,
            p.EmploymentStatus,
            p.Business,
            case p.Representative 
                when 1 then 'Ninguno'
                when 2 then 'Madre'
                when 3 then 'Padre'
                when 4 then 'Otro'
            end as FamiliarApoderado,
            p.RepresentativeName,
            p.RepresentativeRelation,
            p.RepresentativeOcupation,
            p.RepresentativeBusiness as CentroLaboral,
            p.RepresentativePhone,
            p.RepresentativeEmail,
            case p.SecondaryEducationType 
                when 1 then 'Público'
                when 2 then 'Privado'
                when 3 then 'Extranjero'
            end as TipoEducacion,
            case p.SecondaryEducationFinished 
                when 1 then 'Sí'
                when 2 then 'No, cursando 5° año'
                when 3 then 'Otros casos'
            end as EstudiosConcluidos,
            p.SecondaryEducationTypeOther,
            d3.Name as DepartamentoColegio,
            pv3.Name as ProvinciaColegio,
            dt3.Name as DistritoColegio,
            s.Name as Colegio,
            YEAR(p.SecondaryEducationStarts) as FechaInicioPeriodoEstudio,
            p.SecondaryEducationEnds as FechaFinPeriodoEstudio,
            case p.HasDiscapacity
                when 0 then 'Ninguna'
                when 1 then 'Si'
            end as PresentaDiscapacidad,
            p.DiscapacityType
        from Admission.Postulants p
        inner join Generals.Countries c on p.BirthCountryId = c.Id
        left join Generals.Departments d on p.BirthDepartmentId = d.Id
        left join Generals.Provinces pv on p.BirthProvinceId = pv.Id
        left join Generals.Districts dt on p.BirthDistrictId = dt.Id
        inner join Generals.Departments d2 on p.DepartmentId = d2.Id
        inner join Generals.Provinces pv2 on p.ProvinceId = pv2.Id
        inner join Generals.Districts dt2 on p.DistrictId = dt2.Id
        inner join Generals.Departments d3 on p.DepartmentId = d3.Id
        inner join Generals.Provinces pv3 on p.ProvinceId = pv3.Id
        inner join Generals.Districts dt3 on p.DistrictId = dt3.Id
        inner join Admission.Schools s on p.SecondaryEducationSchoolId = s.Id
        where p.ApplicationTermId = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [idApplicationTerm])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    reportes = [dict(zip(columns, row)) for row in rows]

    return Response(reportes)