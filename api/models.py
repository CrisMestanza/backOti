from django.db import models

class Economicsubventionprograms(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=36)  # Field name made lowercase.
    code = models.TextField(db_column='Code', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    begindate = models.DateTimeField(db_column='BeginDate')  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type')  # Field name made lowercase.
    termid = models.CharField(db_column='TermId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    createdby = models.TextField(db_column='CreatedBy', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.TextField(db_column='UpdatedBy', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    campusid = models.CharField(db_column='CampusId', max_length=36, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '[InstitutionalWelfare].[EconomicSubventionPrograms]'


class Studentrequestcafeterias(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=36)  # Field name made lowercase.
    studentid = models.ForeignKey(
        'Students', 
        on_delete=models.DO_NOTHING, 
        db_column='StudentId'
        
    )
    
    # FK hacia Economicsubventionprograms
    economicsubventionprogramid = models.ForeignKey(
        'Economicsubventionprograms', 
        on_delete=models.DO_NOTHING, 
        db_column='EconomicSubventionProgramId'
    )
    
    userprocedureid = models.CharField(db_column='UserProcedureId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    observation = models.TextField(db_column='Observation', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    createdby = models.TextField(db_column='CreatedBy', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.TextField(db_column='UpdatedBy', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '[InstitutionalWelfare].[StudentRequestCafeterias]'  


class Userprocedures(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=36)  # Field name made lowercase.
    dependencyid = models.CharField(db_column='DependencyId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    paymentid = models.CharField(db_column='PaymentId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    procedureid = models.ForeignKey(
        'Procedures', 
        on_delete=models.DO_NOTHING, 
        db_column='ProcedureId', # Nombre real en SQL Server
        related_name='user_procedures'
    )
    termid = models.CharField(db_column='TermId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    procedurefolderid = models.CharField(db_column='ProcedureFolderId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserId', max_length=450, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    recordhistoryid = models.CharField(db_column='RecordHistoryId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    studentuserprocedureid = models.ForeignKey(
        'Studentuserprocedures', 
        on_delete=models.DO_NOTHING, 
        db_column='StudentUserProcedureId',
        blank=True, 
        null=True,
        related_name='general_procedures'
    )
        
    dni = models.CharField(db_column='DNI', max_length=8, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    number = models.IntegerField(db_column='Number')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    observation = models.TextField(db_column='Observation', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    observationstatus = models.TextField(db_column='ObservationStatus', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    urlimage = models.TextField(db_column='UrlImage', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    finalfileurl = models.TextField(db_column='FinalFileUrl', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    correlative = models.TextField(db_column='Correlative', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    proceduredependencyid = models.CharField(db_column='ProcedureDependencyId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    generatedid = models.IntegerField(db_column='GeneratedId')  # Field name made lowercase.
    deletedat = models.DateTimeField(db_column='DeletedAt', blank=True, null=True)  # Field name made lowercase.
    deletedby = models.TextField(db_column='DeletedBy', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    createdby = models.TextField(db_column='CreatedBy', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.TextField(db_column='UpdatedBy', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '[DocumentaryProcedure].[UserProcedures]'


class Procedures(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=36)  # Field name made lowercase.
    conceptid = models.CharField(db_column='ConceptId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    classifierid = models.CharField(db_column='ClassifierId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    dependencyid = models.CharField(db_column='DependencyId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    procedurecategoryid = models.CharField(db_column='ProcedureCategoryId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    proceduresubcategoryid = models.CharField(db_column='ProcedureSubcategoryId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    startdependencyid = models.CharField(db_column='StartDependencyId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    enabled = models.BooleanField(db_column='Enabled')  # Field name made lowercase.
    type = models.SmallIntegerField(db_column='Type')  # Field name made lowercase.
    code = models.TextField(db_column='Code', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    maximumrequestbyterm = models.SmallIntegerField(db_column='MaximumRequestByTerm', blank=True, null=True)  # Field name made lowercase.
    enabledstartdate = models.DateTimeField(db_column='EnabledStartDate', blank=True, null=True)  # Field name made lowercase.
    enabledenddate = models.DateTimeField(db_column='EnabledEndDate', blank=True, null=True)  # Field name made lowercase.
    duration = models.IntegerField(db_column='Duration')  # Field name made lowercase.
    name = models.TextField(db_column='Name', db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    score = models.IntegerField(db_column='Score')  # Field name made lowercase.
    legalbase = models.TextField(db_column='LegalBase', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    statictype = models.IntegerField(db_column='StaticType', blank=True, null=True)  # Field name made lowercase.
    haspicture = models.BooleanField(db_column='HasPicture')  # Field name made lowercase.
    facultyid = models.CharField(db_column='FacultyId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    deletedat = models.DateTimeField(db_column='DeletedAt', blank=True, null=True)  # Field name made lowercase.
    deletedby = models.TextField(db_column='DeletedBy', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    createdby = models.TextField(db_column='CreatedBy', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)  # Field name made lowercase.
    updatedby = models.TextField(db_column='UpdatedBy', db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    object_id = models.IntegerField()
    principal_id = models.IntegerField(blank=True, null=True)
    schema_id = models.IntegerField()
    parent_object_id = models.IntegerField()
    type_desc = models.CharField(max_length=60, blank=True, null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    is_ms_shipped = models.BooleanField()
    is_published = models.BooleanField()
    is_schema_published = models.BooleanField()
    is_auto_executed = models.BooleanField()
    is_execution_replicated = models.BooleanField(blank=True, null=True)
    is_repl_serializable_only = models.BooleanField(blank=True, null=True)
    skips_repl_constraints = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '[DocumentaryProcedure].[Procedures]'


class Studentuserprocedures(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=36)  # Field name made lowercase.
    studentid = models.ForeignKey(
        'Students', 
        on_delete=models.DO_NOTHING, 
        db_column='StudentId', # El nombre exacto en SQL Server
        related_name='user_procedures' # Nombre para busqueda inversa
    )
    
    activitytype = models.SmallIntegerField(db_column='ActivityType')  # Field name made lowercase.
    careerid = models.CharField(db_column='CareerId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    studentsectionid = models.CharField(db_column='StudentSectionId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    academicprogramid = models.CharField(db_column='AcademicProgramId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    curriculumid = models.CharField(db_column='CurriculumId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    termid = models.CharField(db_column='TermId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    courseid = models.CharField(db_column='CourseId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    additionalcredits = models.DecimalField(db_column='AdditionalCredits', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    economicsubventionprogramid = models.ForeignKey(
            'Economicsubventionprograms', 
            on_delete=models.DO_NOTHING, 
            db_column='EconomicSubventionProgramId',
            blank=True, 
            null=True,
            related_name='procedures_in_program'
        )
    
    class Meta:
        managed = False
        db_table = '[DocumentaryProcedure].[StudentUserProcedures]'

class Students(models.Model):
    # PK
    id = models.CharField(db_column='Id', primary_key=True, max_length=36)
    
    # Relaciones y IDs (UUIDs)
    academicagreementid = models.CharField(db_column='AcademicAgreementId', max_length=36, blank=True, null=True)
    academicprogramid = models.CharField(db_column='AcademicProgramId', max_length=36, blank=True, null=True)
    specialtyid = models.CharField(db_column='SpecialtyId', max_length=36, blank=True, null=True)
    admissiontermid = models.CharField(db_column='AdmissionTermId', max_length=36)
    admissiontypeid = models.CharField(db_column='AdmissionTypeId', max_length=36)
    campusid = models.CharField(db_column='CampusId', max_length=36, blank=True, null=True)
    careerid = models.CharField(db_column='CareerId', max_length=36)
    curriculumid = models.CharField(db_column='CurriculumId', max_length=36)
    userid = models.ForeignKey(
        'Aspnetusers', 
        on_delete=models.DO_NOTHING, 
        db_column='UserId',  # El nombre real en la tabla Students
        related_name='student_data'
    )
    studentinformationid = models.CharField(db_column='StudentInformationId', max_length=36, blank=True, null=True)

    # Datos Académicos
    admissiondate = models.DateTimeField(db_column='AdmissionDate', blank=True, null=True)
    careernumber = models.SmallIntegerField(db_column='CareerNumber')
    currentacademicyear = models.IntegerField(db_column='CurrentAcademicYear')
    status = models.IntegerField(db_column='Status')
    condition = models.SmallIntegerField(db_column='Condition')
    moodleid = models.IntegerField(db_column='MoodleId', blank=True, null=True)

    # Auditoría (Nombres exactos de tu lista)
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)
    createdby = models.TextField(db_column='CreatedBy', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)
    updatedby = models.TextField(db_column='UpdatedBy', blank=True, null=True)
    deletedat = models.DateTimeField(db_column='DeletedAt', blank=True, null=True)
    deletedby = models.TextField(db_column='DeletedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = '[Generals].[Students]'


class Aspnetusers(models.Model):
    # Clave primaria (UUID usualmente en ASP.NET Identity)
    id = models.CharField(db_column='Id', primary_key=True, max_length=450)
    
    # Ubicación y Dirección
    departmentid = models.CharField(db_column='DepartmentId', max_length=36, blank=True, null=True)
    provinceid = models.CharField(db_column='ProvinceId', max_length=36, blank=True, null=True)
    districtid = models.CharField(db_column='DistrictId', max_length=36, blank=True, null=True)
    ubigeo = models.TextField(db_column='Ubigeo', blank=True, null=True)
    address = models.TextField(db_column='Address', blank=True, null=True)
    
    # Datos Personales
    name = models.CharField(db_column='Name', max_length=250)
    paternalsurname = models.CharField(db_column='PaternalSurname', max_length=250, blank=True, null=True)
    maternalsurname = models.CharField(db_column='MaternalSurname', max_length=250, blank=True, null=True)
    fullname = models.CharField(db_column='FullName', max_length=450, blank=True, null=True)
    birthdate = models.DateTimeField(db_column='BirthDate', blank=True, null=True)
    sex = models.IntegerField(db_column='Sex', blank=True, null=True)
    dni = models.CharField(db_column='Dni', max_length=250, blank=True, null=True)
    document = models.CharField(db_column='Document', max_length=200, blank=True, null=True)
    documenttype = models.SmallIntegerField(db_column='DocumentType', blank=True, null=True)
    civilstatus = models.SmallIntegerField(db_column='CivilStatus', blank=True, null=True)
    personalemail = models.TextField(db_column='PersonalEmail', blank=True, null=True)
    picture = models.TextField(db_column='Picture', blank=True, null=True)

    # Identidad y Lengua Nativa
    birthdepartmentid = models.CharField(db_column='BirthDepartmentId', max_length=36, blank=True, null=True)
    birthprovinceid = models.CharField(db_column='BirthProvinceId', max_length=36, blank=True, null=True)
    birthdistrictid = models.CharField(db_column='BirthDistrictId', max_length=36, blank=True, null=True)
    ethnicity = models.IntegerField(db_column='Ethnicity', blank=True, null=True)
    ethnicityother = models.TextField(db_column='EthnicityOther', blank=True, null=True)
    ethnicityvar = models.IntegerField(db_column='EthnicityVar', blank=True, null=True)
    nativelanguage = models.IntegerField(db_column='NativeLanguage', blank=True, null=True)
    nativelanguageother = models.TextField(db_column='NativeLanguageOther', blank=True, null=True)
    nativelanguagevar = models.IntegerField(db_column='NativeLanguageVar', blank=True, null=True)
    hasselfidentificationdeclared = models.BooleanField(db_column='HasSelfIdentificationDeclared', blank=True, null=True)
    sourceethnicdata = models.IntegerField(db_column='SourceEthnicData', blank=True, null=True)

    # ASP.NET Identity Fields (Configuración de Cuenta)
    username = models.CharField(db_column='UserName', max_length=256, blank=True, null=True)
    normalizedusername = models.CharField(db_column='NormalizedUserName', max_length=256, blank=True, null=True)
    email = models.CharField(db_column='Email', max_length=256, blank=True, null=True)
    normalizedemail = models.CharField(db_column='NormalizedEmail', max_length=256, blank=True, null=True)
    emailconfirmed = models.BooleanField(db_column='EmailConfirmed')
    passwordhash = models.TextField(db_column='PasswordHash', blank=True, null=True)
    securitystamp = models.TextField(db_column='SecurityStamp', blank=True, null=True)
    concurrencystamp = models.TextField(db_column='ConcurrencyStamp', blank=True, null=True)
    phonenumber = models.TextField(db_column='PhoneNumber', blank=True, null=True)
    phonenumber2 = models.TextField(db_column='PhoneNumber2', blank=True, null=True)
    phonenumberconfirmed = models.BooleanField(db_column='PhoneNumberConfirmed')
    twofactorenabled = models.BooleanField(db_column='TwoFactorEnabled')
    lockoutend = models.DateTimeField(db_column='LockoutEnd', blank=True, null=True)
    lockoutenabled = models.BooleanField(db_column='LockoutEnabled')
    accessfailedcount = models.IntegerField(db_column='AccessFailedCount')
    
    # Estado del Sistema
    isactive = models.BooleanField(db_column='IsActive')
    islockedout = models.BooleanField(db_column='IsLockedOut')
    lockedoutreason = models.TextField(db_column='LockedOutReason', blank=True, null=True)
    state = models.IntegerField(db_column='State')
    type = models.IntegerField(db_column='Type')
    allowedsystem = models.TextField(db_column='AllowedSystem', blank=True, null=True)
    userweb = models.TextField(db_column='UserWeb', blank=True, null=True)
    firsttime = models.BooleanField(db_column='FirstTime', blank=True, null=True)

    # Auditoría
    relationid = models.CharField(db_column='RelationId', max_length=50, blank=True, null=True)
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)
    createdby = models.TextField(db_column='CreatedBy', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)
    updatedby = models.TextField(db_column='UpdatedBy', blank=True, null=True)
    deletedat = models.DateTimeField(db_column='DeletedAt', blank=True, null=True)
    deletedby = models.TextField(db_column='DeletedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = '[dbo].[AspNetUsers]'
        
        

# Cosas de reportes de admisión
from django.db import models


class Countries(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=36)
    code = models.CharField(db_column='Code', max_length=50, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=255)
    relationid = models.CharField(db_column='RelationId', max_length=50, blank=True, null=True)
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)
    createdby = models.TextField(db_column='CreatedBy', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)
    updatedby = models.TextField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Countries'


class Departments(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=36)
    countryid = models.ForeignKey(
        Countries,
        models.DO_NOTHING,
        db_column='CountryId',
        blank=True,
        null=True,
        related_name='departments',
    )
    code = models.CharField(db_column='Code', max_length=50, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=255)
    relationid = models.CharField(db_column='RelationId', max_length=50, blank=True, null=True)
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)
    createdby = models.TextField(db_column='CreatedBy', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)
    updatedby = models.TextField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Departments'


class Provinces(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=36)
    departmentid = models.ForeignKey(
        Departments,
        models.DO_NOTHING,
        db_column='DepartmentId',
        related_name='provinces',
    )
    code = models.CharField(db_column='Code', max_length=50, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=255)
    relationid = models.CharField(db_column='RelationId', max_length=50, blank=True, null=True)
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)
    createdby = models.TextField(db_column='CreatedBy', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)
    updatedby = models.TextField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Provinces'


class Districts(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=36)
    provinceid = models.ForeignKey(
        Provinces,
        models.DO_NOTHING,
        db_column='ProvinceId',
        related_name='districts',
    )
    code = models.CharField(db_column='Code', max_length=50, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=255)
    relationid = models.CharField(db_column='RelationId', max_length=50, blank=True, null=True)
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)
    createdby = models.TextField(db_column='CreatedBy', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)
    updatedby = models.TextField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Districts'


class Schools(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=36)
    modularcode = models.TextField(db_column='ModularCode', blank=True, null=True)
    localcode = models.TextField(db_column='LocalCode', blank=True, null=True)
    name = models.TextField(db_column='Name', blank=True, null=True)
    address = models.TextField(db_column='Address', blank=True, null=True)
    departmentid = models.ForeignKey(
        Departments,
        models.DO_NOTHING,
        db_column='DepartmentId',
        related_name='schools',
    )
    provinceid = models.ForeignKey(
        Provinces,
        models.DO_NOTHING,
        db_column='ProvinceId',
        related_name='schools',
    )
    districtid = models.ForeignKey(
        Districts,
        models.DO_NOTHING,
        db_column='DistrictId',
        related_name='schools',
    )
    ubigeocode = models.TextField(db_column='UbigeoCode', blank=True, null=True)
    type = models.SmallIntegerField(db_column='Type')
    isschooled = models.BooleanField(db_column='IsSchooled')
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)
    createdby = models.TextField(db_column='CreatedBy', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)
    updatedby = models.TextField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Schools'


class Postulants(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=36)

    # FK relacionadas a tu consulta SQL
    birthcountryid = models.ForeignKey(
        Countries,
        models.DO_NOTHING,
        db_column='BirthCountryId',
        related_name='postulants_birth_country',
    )
    birthdepartmentid = models.ForeignKey(
        Departments,
        models.DO_NOTHING,
        db_column='BirthDepartmentId',
        blank=True,
        null=True,
        related_name='postulants_birth_department',
    )
    birthprovinceid = models.ForeignKey(
        Provinces,
        models.DO_NOTHING,
        db_column='BirthProvinceId',
        blank=True,
        null=True,
        related_name='postulants_birth_province',
    )
    birthdistrictid = models.ForeignKey(
        Districts,
        models.DO_NOTHING,
        db_column='BirthDistrictId',
        blank=True,
        null=True,
        related_name='postulants_birth_district',
    )

    departmentid = models.ForeignKey(
        Departments,
        models.DO_NOTHING,
        db_column='DepartmentId',
        related_name='postulants_department',
    )
    provinceid = models.ForeignKey(
        Provinces,
        models.DO_NOTHING,
        db_column='ProvinceId',
        related_name='postulants_province',
    )
    districtid = models.ForeignKey(
        Districts,
        models.DO_NOTHING,
        db_column='DistrictId',
        related_name='postulants_district',
    )

    secondaryeducationdepartmentid = models.ForeignKey(
        Departments,
        models.DO_NOTHING,
        db_column='SecondaryEducationDepartmentId',
        blank=True,
        null=True,
        related_name='postulants_secondary_department',
    )
    secondaryeducationprovinceid = models.ForeignKey(
        Provinces,
        models.DO_NOTHING,
        db_column='SecondaryEducationProvinceId',
        blank=True,
        null=True,
        related_name='postulants_secondary_province',
    )
    secondaryeducationdistrictid = models.ForeignKey(
        Districts,
        models.DO_NOTHING,
        db_column='SecondaryEducationDistrictId',
        blank=True,
        null=True,
        related_name='postulants_secondary_district',
    )
    secondaryeducationschoolid = models.ForeignKey(
        Schools,
        models.DO_NOTHING,
        db_column='SecondaryEducationSchoolId',
        blank=True,
        null=True,
        related_name='postulants_school',
    )

    # Los demás campos quedan igual
    careerid = models.CharField(db_column='CareerId', max_length=36)
    academicprogramid = models.CharField(db_column='AcademicProgramId', max_length=36, blank=True, null=True)
    admissiontypeid = models.CharField(db_column='AdmissionTypeId', max_length=36)
    applicationtermid = models.CharField(db_column='ApplicationTermId', max_length=36)
    campusid = models.CharField(db_column='CampusId', max_length=36)
    examcampusid = models.CharField(db_column='ExamCampusId', max_length=36, blank=True, null=True)
    channelid = models.CharField(db_column='ChannelId', max_length=36, blank=True, null=True)
    nationalitycountryid = models.CharField(db_column='NationalityCountryId', max_length=36)
    studentid = models.CharField(db_column='StudentId', max_length=36, blank=True, null=True)

    address = models.TextField(db_column='Address')
    admissionfolder = models.IntegerField(db_column='AdmissionFolder', blank=True, null=True)
    admissionstate = models.SmallIntegerField(db_column='AdmissionState')
    birthdate = models.DateTimeField(db_column='BirthDate')
    broadcastmedium = models.IntegerField(db_column='BroadcastMedium')
    broadcastmediumother = models.TextField(db_column='BroadcastMediumOther', blank=True, null=True)
    business = models.TextField(db_column='Business', blank=True, null=True)
    childrens = models.IntegerField(db_column='Childrens')
    code = models.TextField(db_column='Code', blank=True, null=True)
    controlphotopath = models.TextField(db_column='ControlPhotoPath', blank=True, null=True)
    cvpostulant = models.TextField(db_column='CvPostulant', blank=True, null=True)
    discapacitytype = models.TextField(db_column='DiscapacityType', blank=True, null=True)
    document = models.TextField(db_column='Document')
    documenttype = models.SmallIntegerField(db_column='DocumentType')
    email = models.TextField(db_column='Email')
    employmentstatus = models.TextField(db_column='EmploymentStatus', blank=True, null=True)
    finalscore = models.DecimalField(db_column='FinalScore', max_digits=18, decimal_places=3)
    hasdiscapacity = models.BooleanField(db_column='HasDiscapacity')
    maritalstatus = models.IntegerField(db_column='MaritalStatus')
    name = models.CharField(db_column='Name', max_length=255)
    maternalsurname = models.CharField(db_column='MaternalSurname', max_length=255, blank=True, null=True)
    paternalsurname = models.CharField(db_column='PaternalSurname', max_length=255)
    occupation = models.TextField(db_column='Occupation', blank=True, null=True)
    phone1 = models.TextField(db_column='Phone1', blank=True, null=True)
    phone2 = models.TextField(db_column='Phone2', blank=True, null=True)
    representative = models.IntegerField(db_column='Representative')
    representativebusiness = models.TextField(db_column='RepresentativeBusiness', blank=True, null=True)
    representativeemail = models.TextField(db_column='RepresentativeEmail', blank=True, null=True)
    representativename = models.TextField(db_column='RepresentativeName', blank=True, null=True)
    representativeocupation = models.TextField(db_column='RepresentativeOcupation', blank=True, null=True)
    representativephone = models.TextField(db_column='RepresentativePhone', blank=True, null=True)
    representativerelation = models.TextField(db_column='RepresentativeRelation', blank=True, null=True)
    secondaryeducationaddress = models.TextField(db_column='SecondaryEducationAddress', blank=True, null=True)
    secondaryeducationends = models.DateTimeField(db_column='SecondaryEducationEnds', blank=True, null=True)
    secondaryeducationfinished = models.IntegerField(db_column='SecondaryEducationFinished')
    secondaryeducationfinishedother = models.TextField(db_column='SecondaryEducationFinishedOther', blank=True, null=True)
    secondaryeducationname = models.TextField(db_column='SecondaryEducationName')
    secondaryeducationstarts = models.DateTimeField(db_column='SecondaryEducationStarts')
    secondaryeducationtype = models.IntegerField(db_column='SecondaryEducationType')
    secondaryeducationtypeother = models.TextField(db_column='SecondaryEducationTypeOther', blank=True, null=True)
    sex = models.IntegerField(db_column='Sex')
    workingcurrently = models.BooleanField(db_column='WorkingCurrently')
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)
    createdby = models.TextField(db_column='CreatedBy', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)
    updatedby = models.TextField(db_column='UpdatedBy', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Postulants'