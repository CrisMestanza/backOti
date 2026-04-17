from rest_framework import serializers
from .models import *
class AspnetusersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aspnetusers
        # Excluimos campos sensibles de seguridad
        exclude = ['passwordhash', 'securitystamp', 'concurrencystamp', 'mysqlpasswordhash']

class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'

class EconomicsubventionprogramsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Economicsubventionprograms
        fields = '__all__'

class UserproceduresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprocedures
        fields = '__all__'

class StudentrequestcafeteriasSerializer(serializers.ModelSerializer):
    # Opcional: Si quieres incluir detalles de los programas en la misma respuesta
    # program_details = EconomicsubventionprogramsSerializer(source='economicsubventionprogramid', read_only=True)
    
    class Meta:
        model = Studentrequestcafeterias
        fields = '__all__'