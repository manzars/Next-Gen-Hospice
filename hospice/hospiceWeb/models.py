from django.db import models

# Create your models here.
class Meta:
    db_table = "admission" #your existing mysql table name 

class Admission(models.Model):
    genderid = models.ForeignKey('Gender', models.DO_NOTHING, db_column='genderId')  # Field name made lowercase.
    diseaseid = models.ForeignKey('Disease', models.DO_NOTHING, db_column='diseaseId')  # Field name made lowercase.
    previousdiseaseid = models.ForeignKey('Previousdisease', models.DO_NOTHING, db_column='previousDiseaseId')  # Field name made lowercase.
    iscritical = models.IntegerField(db_column='isCritical', blank=True, null=True)  # Field name made lowercase.
    bloodgroupid = models.ForeignKey('Bloodgroup', models.DO_NOTHING, db_column='bloodGroupId')  # Field name made lowercase.
    admissiondate = models.DateTimeField(db_column='admissionDate')  # Field name made lowercase.
    dischargedate = models.DateTimeField(db_column='dischargeDate')  # Field name made lowercase.
    ipno = models.CharField(db_column='IPNo', max_length=40)  # Field name made lowercase.
    datediff = models.IntegerField(db_column='dateDiff', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'admission'
        
    def __str__(self):
        return self.admission


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bloodgroup(models.Model):
    bloodgroup = models.CharField(db_column='bloodGroup', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bloodgroup'


class Disease(models.Model):
    disease = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'disease'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Gender(models.Model):
    gender = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gender'


class Previousdisease(models.Model):
    previousdisease = models.CharField(db_column='previousDisease', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'previousdisease'