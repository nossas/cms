# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    provider = models.CharField(max_length=20)
    uid = models.CharField(max_length=20)
    encrypted_password = models.CharField(max_length=50)
    reset_password_token = models.CharField(max_length=50, blank=True, null=True)
    reset_password_sent_at = models.DateTimeField(blank=True, null=True)
    remember_created_at = models.DateTimeField(blank=True, null=True)
    sign_in_count = models.IntegerField()
    current_sign_in_at = models.DateTimeField(blank=True, null=True)
    last_sign_in_at = models.DateTimeField(blank=True, null=True)
    current_sign_in_ip = models.CharField(max_length=20, blank=True, null=True)
    last_sign_in_ip = models.CharField(max_length=20, blank=True, null=True)
    confirmation_token = models.CharField(max_length=30, blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    confirmation_sent_at = models.DateTimeField(blank=True, null=True)
    unconfirmed_email = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    tokens = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    avatar = models.CharField(max_length=200, blank=True, null=True)
    admin = models.BooleanField(blank=True, null=True)
    locale = models.TextField()
    is_admin = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
        unique_together = (('uid', 'provider'),)
