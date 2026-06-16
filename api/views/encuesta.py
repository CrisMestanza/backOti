from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)

# Datos generales
@api_view(['GET'])
@permission_classes([AllowAny])
def getEncuesta(request):
    """
    Obtiene todos los datos con puntaje individual y total por docente
    """
    query = """
        select 
        s.Name as nombre_encuesta, anu.UserName, anu.FullName, ad.Name as departamento_academico,
        si.Title as amarrillo, q.Description as pregunta,
        case abu.Description
        when 'Muy de acuerdo' then 5
        when 'De acuerdo' then 4
        when 'Ni acuerdo, ni desacuerdo' then 3
        when 'En desacuerdo' then 2
        when 'Muy en desacuerdo' then 1
        ELSE 0 end as Puntuacion,
        abu.Description as respuesta
        from Intranet.AnswerByUsers abu 
        inner join Intranet.SurveyUsers su on abu.SurveyUserId = su.Id 
        inner join Intranet.Survey s on su.SurveyId = s.Id 
        inner join Intranet.Question q on abu.QuestionId = q.Id 
        inner join Intranet.SurveyItems si on q.SurveyItemId = si.Id 
        inner join AspNetUsers anu on su.UserId = anu.Id 
        inner join Generals.Teachers t on anu.Id = t.UserId 
        inner join [Scale].AcademicDepartments ad on t.AcademicDepartmentId = ad.Id  
        where (s.Id = 'B14512E6-BB5D-4A45-A98B-08DEAD34C078' OR s.Id = 'F2BC126C-A345-4D41-CF90-08DEAD2C050C')
        order by anu.UserName, si.Title
        """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if not results:
            return Response({"mensaje": "No se encontraron datos"}, status=404)

        # --- Reestructurar JSON ---
        docentes = {}

        for row in results:
            dni = row["UserName"]

            # Inicializar docente si no existe
            if dni not in docentes:
                docentes[dni] = {
                    "nombre_encuesta": row["nombre_encuesta"],
                    "UserName": row["UserName"],
                    "FullName": row["FullName"],
                    "departamento_academico": row["departamento_academico"],
                    "puntaje_total": 0,
                    "PBM": 0,
                    "categorias": {}
                }

            # Acumular puntaje total
            docentes[dni]["puntaje_total"] += row["Puntuacion"]
            docentes[dni]["PBM"] += 5
            categoria = row["amarrillo"]

            # Inicializar categoría si no existe
            if categoria not in docentes[dni]["categorias"]:
                docentes[dni]["categorias"][categoria] = {
                    "amarrillo": categoria,
                    "preguntas": []
                }

            # Agregar pregunta a la categoría
            docentes[dni]["categorias"][categoria]["preguntas"].append({
                "pregunta": row["pregunta"],
                "Puntuacion": row["Puntuacion"],
                "respuesta": row["respuesta"]
            })

        # Convertir categorias de dict a lista
        resultado_final = []
        for docente in docentes.values():
            docente["categorias"] = list(docente["categorias"].values())
            resultado_final.append(docente)

        return Response(resultado_final)

    except Exception as e:
        logger.error(f"Error al obtener encuesta: {str(e)}")
        return Response({"error": "Error interno al conectar con la base de datos"}, status=500)
    
    
# Encuesta por departamento
@api_view(['GET'])
@permission_classes([AllowAny])
def getEncuestaDepartamento(request, iddepartamentoacademico=None):
    """
    Obtiene todos los datos con puntaje individual y total por docente filtrado por departamento
    """
    query = """
        select s.Name as nombre_encuesta, anu.UserName, anu.FullName, ad.Name as departamento_academico,
        si.Title as amarrillo, q.Description as pregunta,
        case abu.Description
        when 'Muy de acuerdo' then 5
        when 'De acuerdo' then 4
        when 'Ni acuerdo, ni desacuerdo' then 3
        when 'En desacuerdo' then 2
        when 'Muy en desacuerdo' then 1
        ELSE 0 end as Puntuacion,
        abu.Description as respuesta
        from Intranet.AnswerByUsers abu 
        inner join Intranet.SurveyUsers su on abu.SurveyUserId = su.Id 
        inner join Intranet.Survey s on su.SurveyId = s.Id 
        inner join Intranet.Question q on abu.QuestionId = q.Id 
        inner join Intranet.SurveyItems si on q.SurveyItemId = si.Id 
        inner join AspNetUsers anu on su.UserId = anu.Id 
        inner join Generals.Teachers t on anu.Id = t.UserId 
        inner join [Scale].AcademicDepartments ad on t.AcademicDepartmentId = ad.Id  
        where(s.Id = 'B14512E6-BB5D-4A45-A98B-08DEAD34C078' OR s.Id = 'F2BC126C-A345-4D41-CF90-08DEAD2C050C') and ad.Id = %s
        order by anu.UserName, si.Title
        """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, [iddepartamentoacademico])
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if not results:
            return Response({"mensaje": "No se encontraron datos"}, status=404)

        # --- Reestructurar JSON ---
        docentes = {}

        for row in results:
            dni = row["UserName"]

            if dni not in docentes:
                docentes[dni] = {
                    "nombre_encuesta": row["nombre_encuesta"],
                    "UserName": row["UserName"],
                    "FullName": row["FullName"],
                    "departamento_academico": row["departamento_academico"],
                    "puntaje_total": 0,
                    "categorias": {}
                }

            docentes[dni]["puntaje_total"] += row["Puntuacion"]

            categoria = row["amarrillo"]

            if categoria not in docentes[dni]["categorias"]:
                docentes[dni]["categorias"][categoria] = {
                    "amarrillo": categoria,
                    "preguntas": []
                }

            docentes[dni]["categorias"][categoria]["preguntas"].append({
                "pregunta": row["pregunta"],
                "Puntuacion": row["Puntuacion"],
                "respuesta": row["respuesta"]
            })

        resultado_final = []
        for docente in docentes.values():
            docente["categorias"] = list(docente["categorias"].values())
            resultado_final.append(docente)

        return Response(resultado_final)

    except Exception as e:
        logger.error(f"Error al obtener encuesta por departamento: {str(e)}")
        return Response({"error": "Error interno al conectar con la base de datos"}, status=500)


# Datos por docente
@api_view(['GET'])
@permission_classes([AllowAny])
def getEncuestaDocente(request, dni=None):
    """
    Obtiene todos los datos con puntaje individual y total por docente filtrado por DNI
    """
    query = """
        select s.Name as nombre_encuesta, anu.UserName, anu.FullName, ad.Name as departamento_academico,
        si.Title as amarrillo, q.Description as pregunta,
        case abu.Description
        when 'Muy de acuerdo' then 5
        when 'De acuerdo' then 4
        when 'Ni acuerdo, ni desacuerdo' then 3
        when 'En desacuerdo' then 2
        when 'Muy en desacuerdo' then 1
        ELSE 0 end as Puntuacion,
        abu.Description as respuesta
        from Intranet.AnswerByUsers abu 
        inner join Intranet.SurveyUsers su on abu.SurveyUserId = su.Id 
        inner join Intranet.Survey s on su.SurveyId = s.Id 
        inner join Intranet.Question q on abu.QuestionId = q.Id 
        inner join Intranet.SurveyItems si on q.SurveyItemId = si.Id 
        inner join AspNetUsers anu on su.UserId = anu.Id 
        inner join Generals.Teachers t on anu.Id = t.UserId 
        inner join [Scale].AcademicDepartments ad on t.AcademicDepartmentId = ad.Id  
        where (s.Id = 'B14512E6-BB5D-4A45-A98B-08DEAD34C078' OR s.Id = 'F2BC126C-A345-4D41-CF90-08DEAD2C050C') and anu.Dni = %s
        order by anu.UserName, si.Title
        """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, [dni])
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if not results:
            return Response({"mensaje": "No se encontraron datos"}, status=404)

        # --- Reestructurar JSON (retorna objeto único, no lista) ---
        docente = None

        for row in results:
            if docente is None:
                docente = {
                    "nombre_encuesta": row["nombre_encuesta"],
                    "UserName": row["UserName"],
                    "FullName": row["FullName"],
                    "departamento_academico": row["departamento_academico"],
                    "puntaje_total": 0,
                    "PBM": 0,
                    "categorias": {}
                }

            docente["puntaje_total"] += row["Puntuacion"]
            docente["PBM"] += 5

            categoria = row["amarrillo"]

            if categoria not in docente["categorias"]:
                docente["categorias"][categoria] = {
                    "amarrillo": categoria,
                    "preguntas": []
                }

            docente["categorias"][categoria]["preguntas"].append({
                "pregunta": row["pregunta"],
                "Puntuacion": row["Puntuacion"],
                "respuesta": row["respuesta"]
            })

        docente["categorias"] = list(docente["categorias"].values())

        return Response(docente)

    except Exception as e:
        logger.error(f"Error al obtener encuesta por docente: {str(e)}")
        return Response({"error": "Error interno al conectar con la base de datos"}, status=500)



# Extraer departamentos
@api_view(['GET'])
@permission_classes([AllowAny])
def getDepartamentos(request):
    """
    Obtiene los últimos 7 periodos académicos para llenar selectores de filtro.
    """
    query = """
        select*from [Scale].AcademicDepartments ad 
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



# Extraer docentes
@api_view(['GET'])
@permission_classes([AllowAny])
def getDocentes(request, dni=None):
    """
    Obtiene los últimos 7 periodos académicos para llenar selectores de filtro.
    """
    query = """
        select top 1*from   AspNetUsers	anus
        where anus.Dni like %s  
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, [f"%{dni}%"])

            # Usamos una lista de comprensión para un mapeo rápido
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if not results:
            return Response({"mensaje": "No se encontraron periodos"}, status=404)

        return Response(results)

    except Exception as e:
        logger.error(f"Error al obtener periodos: {str(e)}")
        return Response({"error": "Error interno al conectar con la base de datos"}, status=500)


# Traer todas los tipos de encuestas
@api_view(['GET'])
@permission_classes([AllowAny])
def getEncuestas(request):

    query = """
        select*from Intranet.Survey s
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


# Datos Por encuesta
@api_view(['GET'])
@permission_classes([AllowAny])
def getPorEncuesta(request, idencuesta=None):
    """
    Obtiene todos los datos con puntaje individual y total por docente
    """
    query = """
        select s.Name as nombre_encuesta, anu.UserName, anu.FullName, ad.Name as departamento_academico,
        si.Title as amarrillo, q.Description as pregunta,
        case abu.Description
        when 'Muy de acuerdo' then 5
        when 'De acuerdo' then 4
        when 'Ni acuerdo, ni desacuerdo' then 3
        when 'En desacuerdo' then 2
        when 'Muy en desacuerdo' then 1
        ELSE 0 end as Puntuacion,
        abu.Description as respuesta
        from Intranet.AnswerByUsers abu 
        inner join Intranet.SurveyUsers su on abu.SurveyUserId = su.Id 
        inner join Intranet.Survey s on su.SurveyId = s.Id 
        inner join Intranet.Question q on abu.QuestionId = q.Id 
        inner join Intranet.SurveyItems si on q.SurveyItemId = si.Id 
        inner join AspNetUsers anu on su.UserId = anu.Id 
        inner join Generals.Teachers t on anu.Id = t.UserId 
        inner join [Scale].AcademicDepartments ad on t.AcademicDepartmentId = ad.Id  
        where s.Id = %s
        order by anu.UserName, si.Title
        """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, [idencuesta])
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if not results:
            return Response({"mensaje": "No se encontraron datos"}, status=404)

        # --- Reestructurar JSON ---
        docentes = {}

        for row in results:
            dni = row["UserName"]

            # Inicializar docente si no existe
            if dni not in docentes:
                docentes[dni] = {
                    "nombre_encuesta": row["nombre_encuesta"],
                    "UserName": row["UserName"],
                    "FullName": row["FullName"],
                    "departamento_academico": row["departamento_academico"],
                    "puntaje_total": 0,
                    "categorias": {}
                }

            # Acumular puntaje total
            docentes[dni]["puntaje_total"] += row["Puntuacion"]

            categoria = row["amarrillo"]

            # Inicializar categoría si no existe
            if categoria not in docentes[dni]["categorias"]:
                docentes[dni]["categorias"][categoria] = {
                    "amarrillo": categoria,
                    "preguntas": []
                }

            # Agregar pregunta a la categoría
            docentes[dni]["categorias"][categoria]["preguntas"].append({
                "pregunta": row["pregunta"],
                "Puntuacion": row["Puntuacion"],
                "respuesta": row["respuesta"]
            })

        # Convertir categorias de dict a lista
        resultado_final = []
        for docente in docentes.values():
            docente["categorias"] = list(docente["categorias"].values())
            resultado_final.append(docente)

        return Response(resultado_final)

    except Exception as e:
        logger.error(f"Error al obtener encuesta: {str(e)}")
        return Response({"error": "Error interno al conectar con la base de datos"}, status=500)
    
    