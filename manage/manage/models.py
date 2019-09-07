# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'company'

class Status(models.Model):
    id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'status'


class Type(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'type'

class Daydata(models.Model):
    all = models.IntegerField(blank=True, null=True)
    have = models.IntegerField(blank=True, null=True)
    nohave = models.IntegerField(blank=True, null=True)
    time = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'daydata'


class Department(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'department'
    def __str__(self):
        return self.name









class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'django_session'


class Floor(models.Model):
    floor = models.IntegerField(blank=True, null=True)
    seatcount = models.IntegerField(db_column='seatCount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'floor'


class Func(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'func'


class Group(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    describe = models.CharField(max_length=255, blank=True, null=True)
    depart_list = models.CharField(max_length=255, blank=True, null=True)
    func_list = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'group'


class Message(models.Model):
    send_user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    receive_user_id = models.CharField(max_length=40, blank=True, null=True)
    receive_user_email = models.CharField(max_length=80, blank=True, null=True)
    seat_id = models.CharField(max_length=50, blank=True, null=True)
    send_status = models.IntegerField(blank=True, null=True)
    receive_suggestion = models.CharField(max_length=255, blank=True, null=True)
    send_msg = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.IntegerField(blank=True, null=True)
    is_pass = models.IntegerField(blank=True, null=True)
    send_time = models.DateTimeField(blank=True, null=True)
    read_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    count = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'message'


class Record(models.Model):
    type = models.IntegerField(blank=True, null=True)
    user_id = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    department = models.ForeignKey(Department, models.DO_NOTHING, blank=True, null=True)
    seat_id = models.CharField(max_length=20, blank=True, null=True)
    record_time = models.DateTimeField(blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)
    action = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'record'


class Role(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'role'


class Seat(models.Model):
    seat_id = models.CharField(max_length=50)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)
    floor = models.CharField(max_length=20, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    #
    # type = models.ForeignKey('Type', models.DO_NOTHING, db_column='type', blank=True, null=True)
    # status = models.ForeignKey('Status', models.DO_NOTHING, db_column='status', blank=True, null=True)
    department = models.ForeignKey(Department, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'seat'

class Empty(models.Model):
    five = models.FloatField(blank=True, null=True)
    six = models.FloatField(blank=True, null=True)
    time = models.DateField(blank=True, null=True)
    seven = models.FloatField(blank=True, null=True)
    eight = models.FloatField(blank=True, null=True)
    nine = models.FloatField(blank=True, null=True)
    zero = models.FloatField(blank=True, null=True)
    all = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'empty'



class Users(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    domain_accounts = models.CharField(max_length=50,blank=True,null=True)
    age = models.IntegerField(blank=True, null=True)
    join_time = models.DateField(blank=True, null=True)
    leave_time = models.DateField(blank=True, null=True)
    seat_id = models.CharField(max_length=50, blank=True, null=True)
    department = models.ForeignKey(Department, models.DO_NOTHING, blank=True, null=True)
    user_id = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=80, blank=True, null=True)
    mobile = models.CharField(max_length=80, blank=True, null=True)
    sex = models.CharField(max_length=12, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    role = models.ForeignKey(Role, models.DO_NOTHING, db_column='role', blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users'
