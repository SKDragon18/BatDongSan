from django.db import models
from django.utils import timezone

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Baidang(models.Model):
    id_baidang = models.BigIntegerField(db_column='ID_BAIDANG', primary_key=True)  # Field name made lowercase.
    tieude = models.CharField(db_column='TIEUDE', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    loai = models.CharField(db_column='LOAI', max_length=7, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    diachi = models.CharField(db_column='DIACHI', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    huyen = models.CharField(db_column='HUYEN', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    quan = models.CharField(db_column='QUAN', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tinh = models.CharField(db_column='TINH', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    giayto = models.BooleanField(db_column='GIAYTO')  # Field name made lowercase.
    sopn = models.IntegerField(db_column='SOPN')  # Field name made lowercase.
    tinhtrang = models.CharField(db_column='TINHTRANG', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dientich = models.FloatField(db_column='DIENTICH')  # Field name made lowercase.
    dai = models.FloatField(db_column='DAI')  # Field name made lowercase.
    rong = models.FloatField(db_column='RONG')  # Field name made lowercase.
    giaban = models.DecimalField(db_column='GIABAN', max_digits=19, decimal_places=4)  # Field name made lowercase.
    chitiet = models.TextField(db_column='CHITIET', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    trangthai = models.IntegerField(db_column='TRANGTHAI')  # Field name made lowercase.
    chudang = models.CharField(db_column='CHUDANG', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    ngaydang = models.DateField(db_column='NGAYDANG', default=timezone.now())  # Field name made lowercase.
    ngayban = models.DateField(db_column='NGAYBAN', blank=True, null=True)  # Field name made lowercase.
    tendangnhap = models.ForeignKey('Nguoidung', models.DO_NOTHING, db_column='TENDANGNHAP')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BAIDANG'

    


class Chungcu(models.Model):
    machungcu = models.OneToOneField(Baidang, models.DO_NOTHING, db_column='MACHUNGCU', primary_key=True)  # Field name made lowercase.
    lo = models.CharField(db_column='LO', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    macan = models.CharField(db_column='MACAN', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sotang = models.IntegerField(db_column='SOTANG', blank=True, null=True)  # Field name made lowercase.
    huong = models.CharField(db_column='HUONG', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CHUNGCU'


class DsYeuthich(models.Model):
    tendangnhap = models.OneToOneField('Nguoidung', models.DO_NOTHING, db_column='TENDANGNHAP', primary_key=True)  # Field name made lowercase. The composite primary key (TENDANGNHAP, ID_BAIDANG) found, that is not supported. The first column is selected.
    id_baidang = models.ForeignKey(Baidang, models.DO_NOTHING, db_column='ID_BAIDANG')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DS_YEUTHICH'
        unique_together = (('tendangnhap', 'id_baidang'),)


class Hinhanh(models.Model):
    id_hinhanh = models.BigIntegerField(db_column='ID_HINHANH', primary_key=True)  # Field name made lowercase.
    nguon = models.CharField(db_column='NGUON', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    id_baidang = models.ForeignKey(Baidang, models.DO_NOTHING, db_column='ID_BAIDANG', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HINHANH'


class Nguoidung(models.Model):
    tendangnhap = models.CharField(db_column='TENDANGNHAP', primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    matkhau = models.CharField(db_column='MATKHAU', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    phanquyen = models.ForeignKey('Phanquyen', models.DO_NOTHING, db_column='PHANQUYEN')  # Field name made lowercase.
    khoa = models.BooleanField(db_column='KHOA')  # Field name made lowercase.
    ho = models.CharField(db_column='HO', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    ten = models.CharField(db_column='TEN', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    gioitinh = models.CharField(db_column='GIOITINH', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    ngaysinh = models.DateField(db_column='NGAYSINH', blank=True, null=True)  # Field name made lowercase.
    sdt = models.CharField(db_column='SDT', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NGUOIDUNG'


class Nha(models.Model):
    manha = models.OneToOneField(Baidang, models.DO_NOTHING, db_column='MANHA', primary_key=True)  # Field name made lowercase.
    loaihinh = models.CharField(db_column='LOAIHINH', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sotang = models.IntegerField(db_column='SOTANG')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NHA'
        


class Phanquyen(models.Model):
    maquyen = models.CharField(db_column='MAQUYEN', primary_key=True, max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tenquyen = models.CharField(db_column='TENQUYEN', unique=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PHANQUYEN'

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    email = models.CharField(max_length=254, db_collation='SQL_Latin1_General_CP1_CI_AS')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    model = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')
    session_data = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
