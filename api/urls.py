from django.urls import path
from .views.gmail import *
from .views.comedor import *
from .views.reportePostulantes import *
from .views.pagosComedor import *

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
    path('getPagos/<str:dni>/', getPagos),
    path('deletePagos/<str:id>/', deletePagos),
    path('getUser/', getUser),
]