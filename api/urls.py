from django.urls import path
from .views.gmail import *
from .views.comedor import *
from .views.reportePostulantes import *
from .views.pagosComedor import *
from .views.encuesta import *
from .views.egresados import *
from .views.ordenarpdf import ordenar_pdf
from .views.escuela import *

urlpatterns = [
    # Gmail
    path('gmail/', gmail),
    path('enviar-correo/', enviar_correo_simple),
    # Cambio de becas en comedor
    path('comedor/', getStudents),
    path('getPeriodo/', getPeriodo),
    path('cambioBeca/', cambioBeca),
    path('cambioEstado/', cambioEstado),
    path('getStudentsDni/<str:dni>/', getStudentsDni),
    path('getStudentsPeriodoDni/<str:dni>/<str:periodo>/', getStudentsPeriodoDni),
    
    # Generar reportes de admisión
    path('generarReportes/<str:idApplicationTerm>/', generarReportes),
    path('getApplicationTerms/<str:idTerm>/', getApplicationTerms),
    path('getPeriodo/<str:dni>/', getPeriodo),

    # Pagos comedor delete
    path('getUser/', getUser),
    path('getPagos/<str:dni>/', getPagos),
    path('getestudiantedi/<str:dni>/', getStudentDni),
    path('deletePagos/<str:id>/', deletePagos),

    # Encuesta
    path('getencuesta/', getEncuesta),
    path('getencuestadepartamento/<str:iddepartamentoacademico>/', getEncuestaDepartamento),
    path('getencuestadocente/<str:dni>/', getEncuestaDocente),
    path('getdepartamentos/', getDepartamentos),
    path('getdocentes/<str:dni>/', getDocentes),
    path('getporencuesta/<str:idencuesta>/', getPorEncuesta),
    path('getencuestafiltro/', getEncuestaFiltro),
    path('getencuestas/', getEncuestas),

    # Ordenar PDF de caja
    path('ordenarpdf/', ordenar_pdf),
    
    # Egresados
    path('getegresados/', getEgresados),
    path('getegresado/<str:dni>/', getEgresado),
    
    # Escuelas
    path('getescuelas/', getEscuelas),
    path('getescuelaspornombre/<str:nombre>/', getEscuelasPorNombre),
]