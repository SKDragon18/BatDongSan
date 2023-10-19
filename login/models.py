# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

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


class Nguoidung(models.Model):
    tendangnhap = models.CharField(db_column='TENDANGNHAP', primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    matkhau = models.CharField(db_column='MATKHAU', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    phanquyen = models.ForeignKey('Phanquyen', models.DO_NOTHING, db_column='PHANQUYEN')  # Field name made lowercase.
    khoa = models.BooleanField(db_column='KHOA')  # Field name made lowercase.
    ho = models.CharField(db_column='HO', max_length=50,null=True, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    ten = models.CharField(db_column='TEN', max_length=20,null=True, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    gioitinh = models.CharField(db_column='GIOITINH', max_length=3,null=True, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    ngaysinh = models.DateField(db_column='NGAYSINH', blank=True, null=True)  # Field name made lowercase.
    sdt = models.CharField(db_column='SDT', max_length=10,null=True, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NGUOIDUNG'


class Phanquyen(models.Model):
    maquyen = models.CharField(db_column='MAQUYEN', primary_key=True, max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tenquyen = models.CharField(db_column='TENQUYEN', unique=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PHANQUYEN'
