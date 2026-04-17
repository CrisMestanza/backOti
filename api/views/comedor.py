from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def getPeriodo(request):
    """
    Obtiene los últimos 7 periodos académicos para llenar selectores de filtro.
    """
    query = """
        SELECT TOP 7
            t.Id AS value,
            t.Name AS label
        FROM [Enrollment].[Terms] AS t
        ORDER BY t.Name DESC
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)

            # Usamos una lista de comprensión para un mapeo rápido
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if not results:
            return Response({"mensaje": "No se encontraron periodos"}, status=404)

        return Response(results)

    except Exception as e:
        logger.error(f"Error al obtener periodos: {str(e)}")
        return Response({"error": "Error interno al conectar con la base de datos"}, status=500)


# Obtener todos los estudiantes
@api_view(['GET'])
@permission_classes([AllowAny])
def getStudents(request):
    """
    Obtiene el listado de estudiantes con sus beneficios de bienestar
    y el trámite documentario vinculado al mismo periodo.
    """
    query = """
        SELECT TOP 50
            s.Id AS id_estudiante,
            u.Dni AS dni,
            u.Name AS nombres,
            u.PaternalSurname AS ap_paterno,
            u.MaternalSurname AS ap_materno,
            u.Email AS email,
            s.CurrentAcademicYear AS ciclo,
            s.Status AS estado_estudiante,

            -- Datos de la Subvención
            esp.Id AS id_subvencion,
            esp.Name AS nombre_subvencion,

            -- Datos del Periodo
            t.Name AS nombre_periodo,
            t.Number AS numero_periodo,

            -- Trámite Documentario (Vinculado por Periodo para evitar duplicados)
            up.Id AS id_user_procedure,
            up.Status AS estado_tramite,
            up.CreatedAt AS fecha_tramite,
            p.Name AS nombre_procedure,
            sup.Id AS id_student_user_procedure,

            -- Request, traer estado
            src.Status AS estado,

            -- Sede
            c.Name AS nombre_sede

        FROM [Generals].[Students] s
        INNER JOIN [dbo].[AspNetUsers] u ON s.UserId = u.Id
        INNER JOIN [InstitutionalWelfare].[StudentRequestCafeterias] src ON src.StudentId = s.Id
        INNER JOIN [InstitutionalWelfare].[EconomicSubventionPrograms] esp ON esp.Id = src.EconomicSubventionProgramId
        INNER JOIN [Enrollment].[Terms] t ON t.Id = esp.TermId

        -- Unión con trámites filtrando por el mismo Periodo Académico
        INNER JOIN [DocumentaryProcedure].[StudentUserProcedures] sup ON sup.StudentId = s.Id
        INNER JOIN [DocumentaryProcedure].[UserProcedures] up ON up.StudentUserProcedureId = sup.Id
            AND up.TermId = t.Id  -- CRÍTICO: Solo trámites del mismo periodo que la beca
        INNER JOIN [DocumentaryProcedure].[Procedures] p ON p.Id = up.ProcedureId
        INNER JOIN [Enrollment].[Campuses] c ON s.CampusId = c.Id

        ORDER BY t.Name DESC, up.CreatedAt DESC
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    data_final = []
    for r in results:
        data_final.append({
            "entidad_estudiante": {
                "id": r['id_estudiante'],
                "dni": r['dni'],
                "nombre_completo": f"{r['nombres']} {r['ap_paterno']} {r['ap_materno']}".strip(),
                "email": r['email'],
                "ciclo_estudiante": r['ciclo'],
                "estado_academico": r['estado_estudiante'],
                "sede": r['nombre_sede'],
                "estado": r['estado']
            },
            "entidad_periodo": {
                "nombre": r['nombre_periodo'],
                "numero": r['numero_periodo']
            },
            "entidad_bienestar": {
                "id_subvencion": r['id_subvencion'],
                "programa": r['nombre_subvencion']
            },
            "entidad_tramite": {
                "nombre_tramite": r['nombre_procedure'],
                "id_documentario": r['id_user_procedure'],
                "estado_proceso": r['estado_tramite'],
                "fecha_creacion": r['fecha_tramite']
            },
            "metadatos": {
                "student_user_procedure_id": r['id_student_user_procedure']
            }
        })

    return Response(data_final)


@api_view(['GET'])
@permission_classes([AllowAny])
def getStudentsDni(request, dni=None):
    if not dni:
        return Response({"error": "DNI es requerido"}, status=400)

    # Nota: Eliminamos los JOINs de DocumentaryProcedure para evitar duplicados
    query = """
        SELECT
            s.Id AS id_estudiante,
            u.Dni AS dni,
            u.Name AS nombres,
            u.PaternalSurname AS ap_paterno,
            u.MaternalSurname AS ap_materno,
            u.Email AS email,
            s.CurrentAcademicYear AS ciclo,
            esp.Id AS id_subvencion,
            esp.Name AS nombre_subvencion,
            t.Name AS nombre_periodo,
            t.Number AS numero_periodo,
            c.Name AS nombre_sede,
            -- Request, traer estado
            src.Status AS estado

        FROM [Generals].[Students] s
        INNER JOIN [dbo].[AspNetUsers] u ON s.UserId = u.Id
        INNER JOIN [InstitutionalWelfare].[StudentRequestCafeterias] src ON src.StudentId = s.Id
        INNER JOIN [InstitutionalWelfare].[EconomicSubventionPrograms] esp ON esp.Id = src.EconomicSubventionProgramId
        INNER JOIN [Enrollment].[Terms] t ON t.Id = esp.TermId
        INNER JOIN [Enrollment].[Campuses] c ON s.CampusId = c.Id

        WHERE u.Dni = %s
        ORDER BY t.Name DESC
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [dni])
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    if not results:
        return Response({"mensaje": "No se encontraron beneficios para este DNI"}, status=404)

    data_final = []
    for r in results:
        data_final.append({
            "entidad_estudiante": {
                "dni": r['dni'],
                "nombre_completo": f"{r['nombres']} {r['ap_paterno']} {r['ap_materno']}".strip(),
                "ciclo_estudiante": r['ciclo'],
                "sede": r['nombre_sede'],
                "estado": r['estado']
            },
            "entidad_periodo": {
                "nombre": r['nombre_periodo'],
                "numero": r['numero_periodo']
            },
            "entidad_bienestar": {
                "id_subvencion": r['id_subvencion'],
                "programa": r['nombre_subvencion']
                
            }
        })

    return Response(data_final)


@api_view(['GET'])
@permission_classes([AllowAny])
def getStudentsPeriodoDni(request, dni=None, periodo=None):
    # 1. Validaciones iniciales
    if not dni:
        return Response({"error": "DNI es requerido"}, status=400)

    if not periodo:
        return Response({"error": "El periodo (TermId) es requerido"}, status=400)

    # 2. Query con filtros para DNI y Periodo (TermId)
    query = """
        SELECT
            s.Id AS id_estudiante,
            u.Dni AS dni,
            u.Name AS nombres,
            u.PaternalSurname AS ap_paterno,
            u.MaternalSurname AS ap_materno,
            u.Email AS email,
            s.CurrentAcademicYear AS ciclo,
            esp.Id AS id_subvencion,
            esp.Name AS nombre_subvencion,
            t.Name AS nombre_periodo,
            t.Number AS numero_periodo,
            c.Name AS nombre_sede

        FROM [Generals].[Students] s
        INNER JOIN [dbo].[AspNetUsers] u ON s.UserId = u.Id
        INNER JOIN [InstitutionalWelfare].[StudentRequestCafeterias] src ON src.StudentId = s.Id
        INNER JOIN [InstitutionalWelfare].[EconomicSubventionPrograms] esp ON esp.Id = src.EconomicSubventionProgramId
        INNER JOIN [Enrollment].[Terms] t ON t.Id = esp.TermId
        INNER JOIN [Enrollment].[Campuses] c ON s.CampusId = c.Id

        WHERE u.Dni = %s
          AND t.Name = %s  -- Filtro por Periodo (TermId)
        ORDER BY t.Name DESC
    """

    try:
        with connection.cursor() as cursor:
            # 3. Pasar los parámetros en el orden correcto
            cursor.execute(query, [dni, periodo])

            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if not results:
            return Response({"mensaje": "No se encontraron beneficios para los datos ingresados"}, status=404)

        data_final = []
        for r in results:
            data_final.append({
                "entidad_estudiante": {
                    "dni": r['dni'],
                    "nombre_completo": f"{r['nombres']} {r['ap_paterno']} {r['ap_materno']}".strip(),
                    "ciclo": r['ciclo'],
                    "sede": r['nombre_sede']
                },
                "entidad_periodo": {
                    "nombre": r['nombre_periodo'],
                    "numero": r['numero_periodo']
                },
                "entidad_bienestar": {
                    "id_subvencion": r['id_subvencion'],
                    "programa": r['nombre_subvencion']
                }
            })

        return Response(data_final)

    except Exception as e:
        return Response({"error": f"Error en el servidor: {str(e)}"}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def cambioEstado(request):
    dni = request.data.get('dni')
    periodo = request.data.get('periodo')
    sede = request.data.get('sede')
    beca = request.data.get('beca')
    estado = request.data.get('estado')

    # Obtener Estudiante
    queryAnu = f"""
        SELECT anu.* FROM [UNSM.SIGAU.DB].dbo.AspNetUsers AS anu
        where anu.DNI = '{dni}'
    """
    with connection.cursor() as cursor:
        cursor.execute(queryAnu)
        resultAnu = cursor.fetchall()

    queryStudent = f"""
        SELECT DISTINCT * FROM [UNSM.SIGAU.DB].Generals.Students AS s
        where s.UserId  = '{resultAnu[0][0]}'
    """
    with connection.cursor() as cursor:
        cursor.execute(queryStudent)
        resultStudent = cursor.fetchall()

    if beca == "BECA":
        queryEsp = f"""
            select DISTINCT esp.Id  ,esp.CreatedAt, esp.Name
            from InstitutionalWelfare.EconomicSubventionPrograms esp
            where  esp.Name like '%{periodo}%'
            AND  esp.Name like '%{sede}%'
            AND  esp.Name like '%COMEDOR%'
            AND  esp.Name NOT LIKE '%SEMI-BECAS%'
            order by esp.CreatedAt  desc
        """

    elif beca == "SEMI-BECA":
        # Si es Semi beca
        queryEsp = f"""
            select DISTINCT esp.Id  ,esp.CreatedAt, esp.Name
            from InstitutionalWelfare.EconomicSubventionPrograms esp
            where  esp.Name like '%{periodo}%'
            AND  esp.Name like '%{sede}%'
            AND  esp.Name like '%COMEDOR%'
            AND  esp.Name LIKE '%SEMI-BECAS%'
            order by esp.CreatedAt  desc
        """

    with connection.cursor() as cursor:
        cursor.execute(queryEsp)
        resultEsp = cursor.fetchall()

    querySrc = f"""
            select src.* from InstitutionalWelfare.StudentRequestCafeterias src
            where src.StudentId = '{resultStudent[0][0]}'
            AND src.EconomicSubventionProgramId = '{resultEsp[0][0]}'
        """
    with connection.cursor() as cursor:
        cursor.execute(querySrc)
        resultSrc = cursor.fetchall()

    if estado.lower() == "pendiente":
        queryActualizarSrc = f"""
        
            UPDATE InstitutionalWelfare.StudentRequestCafeterias 
            SET Status = '0'
            WHERE
            Id = '{resultSrc[0][0]}'
            
        """
        with connection.cursor() as cursor:
                cursor.execute(queryActualizarSrc)
        
                
    if estado.lower() == "aprobado":
        queryActualizarSrc = f"""
        
            UPDATE InstitutionalWelfare.StudentRequestCafeterias 
            SET Status = '1'
            WHERE
            Id = '{resultSrc[0][0]}'
            
        """
        with connection.cursor() as cursor:
                cursor.execute(queryActualizarSrc)    
                
    if estado.lower() == "denegado":
        queryActualizarSrc = f"""
        
            UPDATE InstitutionalWelfare.StudentRequestCafeterias 
            SET Status = '2'
            WHERE
            Id = '{resultSrc[0][0]}'
            
        """
        with connection.cursor() as cursor:
                cursor.execute(queryActualizarSrc)    
                
    return Response({"mensaje": "El estado del beneficio ha sido actualizado"}, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def cambioBeca(request):
    
    dni = request.data.get('dni')
    periodo = request.data.get('periodo')
    sede = request.data.get('sede')
    beca = request.data.get('beca')
    
    print(f"Datos recibidos - DNI: {dni}, Periodo: {periodo}, Sede: {sede}, Beca: {beca}")
    # ------ Tablas de abajo StudentRequestCafeterias y StudentUserProcedures ------------------
    # ------------------------------------------------------------------------------------------
    
    # Obtener Estudiante  
    queryAnu = f"""
        SELECT anu.* FROM [UNSM.SIGAU.DB].dbo.AspNetUsers AS anu
        where anu.DNI = '{dni}' 
    """
    with connection.cursor() as cursor:
        cursor.execute(queryAnu)
        resultAnu = cursor.fetchall()


    queryStudent = f"""
        SELECT DISTINCT * FROM [UNSM.SIGAU.DB].Generals.Students AS s
        where s.UserId  = '{resultAnu[0][0]}'
    """
    with connection.cursor() as cursor:
        cursor.execute(queryStudent)
        resultStudent = cursor.fetchall()


    
    # Obtener EconomicSubventionPrograms
    # Si es beca 
    if beca == "BECA":
        queryEsp = f"""
            select DISTINCT esp.Id  ,esp.CreatedAt, esp.Name  
            from InstitutionalWelfare.EconomicSubventionPrograms esp 
            where  esp.Name like '%{periodo}%'   
            AND  esp.Name like '%{sede}%' 
            AND  esp.Name like '%COMEDOR%'
            AND  esp.Name NOT LIKE '%SEMI-BECAS%' 
            order by esp.CreatedAt  desc
        """
        queryEspActualizar = f"""
            select DISTINCT esp.Id  ,esp.CreatedAt, esp.Name  
            from InstitutionalWelfare.EconomicSubventionPrograms esp 
            where  esp.Name like '%{periodo}%'   
            AND  esp.Name like '%{sede}%' 
            AND  esp.Name like '%COMEDOR%'
            AND  esp.Name LIKE '%SEMI-BECAS%' 
            order by esp.CreatedAt  desc
        """
        
    elif beca == "SEMI-BECA": 
        # Si es Semi beca 
        queryEsp = f"""
            select DISTINCT esp.Id  ,esp.CreatedAt, esp.Name  
            from InstitutionalWelfare.EconomicSubventionPrograms esp 
            where  esp.Name like '%{periodo}%'   
            AND  esp.Name like '%{sede}%' 
            AND  esp.Name like '%COMEDOR%'
            AND  esp.Name LIKE '%SEMI-BECAS%' 
            order by esp.CreatedAt  desc
        """
        
        queryEspActualizar = f"""
            select DISTINCT esp.Id  ,esp.CreatedAt, esp.Name  
            from InstitutionalWelfare.EconomicSubventionPrograms esp 
            where  esp.Name like '%{periodo}%'   
            AND  esp.Name like '%{sede}%' 
            AND  esp.Name like '%COMEDOR%'
            AND  esp.Name NOT LIKE '%SEMI-BECAS%' 
            order by esp.CreatedAt  desc
        """
        
    with connection.cursor() as cursor:
        cursor.execute(queryEsp)
        resultEsp = cursor.fetchall()
        
    with connection.cursor() as cursor:
        cursor.execute(queryEspActualizar)
        resultEspActualizar = cursor.fetchall()

    # Obtener el StudentRequestCafeterias 
    
    querySrc = f"""
        select src.* from InstitutionalWelfare.StudentRequestCafeterias src 
        where src.StudentId = '{resultStudent[0][0]}'
        AND src.EconomicSubventionProgramId = '{resultEsp[0][0]}'
    """
    with connection.cursor() as cursor:
        cursor.execute(querySrc)
        resultSrc = cursor.fetchall()
    
    # Obtener el StudentUserProcedures 
    querySup = f""" 
        SELECT sup.* FROM [UNSM.SIGAU.DB].DocumentaryProcedure.StudentUserProcedures AS sup
        where sup.StudentId = '{resultStudent[0][0]}'
        AND sup.EconomicSubventionProgramId = '{resultEsp[0][0]}'
    """
    
    with connection.cursor() as cursor:
        cursor.execute(querySup)
        resultSup = cursor.fetchall()

    
    # Actualizar Comedor en StudentUserProcedures
    queryActualizarSup = f"""
    
        UPDATE DocumentaryProcedure.StudentUserProcedures
        SET EconomicSubventionProgramId = '{resultEspActualizar[0][0]}'
        WHERE
        StudentId = '{resultStudent[0][0]}'
        AND EconomicSubventionProgramId = '{resultEsp[0][0]}'
        
    """
    
    # Actualizar Comedor en StudentRequestCafeterias
    
    queryActualizarSrc = f"""
    
        UPDATE InstitutionalWelfare.StudentRequestCafeterias 
        SET EconomicSubventionProgramId = '{resultEspActualizar[0][0]}'
        WHERE
        StudentId = '{resultStudent[0][0]}'
        AND EconomicSubventionProgramId = '{resultEsp[0][0]}'
        
    """
    
    with connection.cursor() as cursor:
        cursor.execute(queryActualizarSup)
        
    with connection.cursor() as cursor:
        cursor.execute(queryActualizarSrc)
    
    # ------ Tablas de arriba StudentRequestCafeterias y StudentUserProcedures ------------------
    # ------------------------------------------------------------------------------------------

    # Obtener Procedures
    # Si es beca 
    if beca == "BECA":
        queryProcedures = f"""
            SELECT DISTINCT p.Id, p.CreatedAt, p.Name 
            FROM DocumentaryProcedure.Procedures p  
            WHERE p.Name LIKE '%comedor%' 
            AND p.Name LIKE '%{sede}%'
            AND p.Name LIKE '%{periodo}%'
            AND p.Name NOT LIKE '%Semibeca%' 
            ORDER BY p.CreatedAt DESC
        """
        
        queryProceduresActualizar = f"""
            SELECT DISTINCT p.Id, p.CreatedAt, p.Name 
            FROM DocumentaryProcedure.Procedures p  
            WHERE p.Name LIKE '%comedor%' 
            AND p.Name LIKE '%{sede}%'
            AND p.Name LIKE '%{periodo}%'
            AND p.Name LIKE '%Semibeca%' 
            ORDER BY p.CreatedAt DESC
        """
        
        
    elif beca == "SEMI-BECA":
        queryProcedures = f"""
            SELECT DISTINCT p.Id, p.CreatedAt, p.Name 
            FROM DocumentaryProcedure.Procedures p  
            WHERE p.Name LIKE '%comedor%' 
            AND p.Name LIKE '%{sede}%'
            AND p.Name LIKE '%{periodo}%'
            AND p.Name LIKE '%Semibeca%' 
            ORDER BY p.CreatedAt DESC
        """
        
        queryProceduresActualizar  = f"""
            SELECT DISTINCT p.Id, p.CreatedAt, p.Name 
            FROM DocumentaryProcedure.Procedures p  
            WHERE p.Name LIKE '%comedor%' 
            AND p.Name LIKE '%{sede}%'
            AND p.Name LIKE '%{periodo}%'
            AND p.Name NOT LIKE '%Semibeca%' 
            ORDER BY p.CreatedAt DESC
        """
        
    with connection.cursor() as cursor:
        cursor.execute(queryProcedures)
        resultProcedures = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(queryProceduresActualizar)
        resultProceduresActualizar = cursor.fetchall()
    
    
    # Obtener UserProcedures
    queryUserProcedures = f"""
        select * from DocumentaryProcedure.UserProcedures up 
        where up.UserId = '{resultAnu[0][0]}'
        AND   up.ProcedureId = '{resultProcedures[0][0]}'
    """
    
    with connection.cursor() as cursor:
        cursor.execute(queryUserProcedures)
        resultUserProcedures = cursor.fetchall()
    
    queryActualizarUserProcedure= f"""
    
        UPDATE DocumentaryProcedure.UserProcedures 
        SET ProcedureId = '{resultProceduresActualizar[0][0]}'
        where UserId = '{resultAnu[0][0]}'
        AND   ProcedureId = '{resultProcedures[0][0]}'
        
    """   
    with connection.cursor() as cursor:

        cursor.execute(queryActualizarUserProcedure)
    
    # Falta para actualizar como tal
    
    return Response({"mensaje": "Los datos ya fueron actualizados"}, status=200)