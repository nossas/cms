# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    # provider = models.CharField(max_length=100)
    # uid = models.CharField(max_length=100)
    encrypted_password = models.CharField(max_length=60)
    # reset_password_token = models.CharField(max_length=60, blank=True, null=True)
    # reset_password_sent_at = models.DateTimeField(blank=True, null=True)
    # remember_created_at = models.DateTimeField(blank=True, null=True)
    # sign_in_count = models.IntegerField()
    # current_sign_in_at = models.DateTimeField(blank=True, null=True)
    # last_sign_in_at = models.DateTimeField(blank=True, null=True)
    # current_sign_in_ip = models.CharField(max_length=20, blank=True, null=True)
    # last_sign_in_ip = models.CharField(max_length=20, blank=True, null=True)
    # confirmation_token = models.CharField(max_length=60, blank=True, null=True)
    # confirmed_at = models.DateTimeField(blank=True, null=True)
    # confirmation_sent_at = models.DateTimeField(blank=True, null=True)
    # unconfirmed_email = models.CharField(max_length=60, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    # tokens = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    avatar = models.CharField(max_length=150, blank=True, null=True)
    # admin = models.BooleanField(blank=True, null=True)
    # locale = models.TextField()
    is_admin = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "users"
        # unique_together = (('uid', 'provider'),)

    def __str__(self):
        return self.email


class Community(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    # mailchimp_api_key = models.TextField(blank=True, null=True)
    # mailchimp_list_id = models.TextField(blank=True, null=True)
    # mailchimp_group_id = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    # recipient = models.ForeignKey('Recipients', models.DO_NOTHING, blank=True, null=True)
    facebook_app_id = models.CharField(max_length=100, blank=True, null=True)
    fb_link = models.CharField(max_length=100, blank=True, null=True)
    twitter_link = models.CharField(max_length=100, blank=True, null=True)
    # subscription_retry_interval = models.IntegerField(blank=True, null=True)
    # subscription_dead_days_interval = models.IntegerField(blank=True, null=True)
    email_template_from = models.CharField(max_length=100, blank=True, null=True)
    # mailchimp_sync_request_at = models.DateTimeField(blank=True, null=True)
    # modules = models.JSONField(blank=True, null=True)
    signature = models.JSONField(blank=True, null=True)
    # classification = models.CharField(max_length=20, blank=True, null=True)
    an_group_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "communities"

    def __str__(self):
        return self.name


class CommunityUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, blank=True, null=True
    )
    role = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "community_users"
        unique_together = (("community_id", "user_id", "role"),)


class DnsHostedZones(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True)
    domain_name = models.CharField(unique=True, max_length=100, blank=True, null=True)
    # comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    # response = models.JSONField(blank=True, null=True)
    # ns_ok = models.BooleanField(blank=True, null=True)
    # status = models.TextField(blank=True, null=True)  # This field type is a guess.
    # is_external_domain = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'dns_hosted_zones'