# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site

from cms.models import CMSPlugin


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


class RequestManager(models.Manager):
    def __init__(self, lookup_field=None):
        self.lookup_field = lookup_field
        super(RequestManager, self).__init__()

    def on_site(self, request=None):
        site = Site.objects.get(id=settings.SITE_ID)
        if request:
            site = request.current_site

        prefix = "" if not self.lookup_field else f"{self.lookup_field}__"

        params = {f"{prefix}dnshostedzone__domain_name": site.domain}

        return self.get_queryset().filter(**params)


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

    objects = RequestManager()

    class Meta:
        managed = False
        db_table = "communities"

    def __str__(self):
        return self.name

    def get_signature(self):
        signature = self.signature or {}
        return {
            "name": signature.get("name", self.name),
            "url": signature.get("url", "#"),
        }


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


class DnsHostedZone(models.Model):
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, blank=True, null=True
    )
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
        db_table = "dns_hosted_zones"


class MobilizationStatus(models.TextChoices):
    archived = "archived", "Arquivada"
    active = "active", "Ativa"


class Mobilization(models.Model):
    name = models.CharField(max_length=266, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # user_id = models.IntegerField(blank=True, null=True)
    # color_scheme = models.CharField(max_length=-1, blank=True, null=True)
    # google_analytics_code = models.CharField(max_length=-1, blank=True, null=True)
    # goal = models.TextField(blank=True, null=True)
    # header_font = models.CharField(max_length=-1, blank=True, null=True)
    # body_font = models.CharField(max_length=-1, blank=True, null=True)
    # facebook_share_title = models.CharField(max_length=-1, blank=True, null=True)
    # facebook_share_description = models.TextField(blank=True, null=True)
    # facebook_share_image = models.CharField(max_length=-1, blank=True, null=True)
    # slug = models.CharField(unique=True, max_length=-1, blank=True, null=True)
    custom_domain = models.CharField(unique=True, max_length=255, blank=True, null=True)
    twitter_share_text = models.CharField(max_length=300, blank=True, null=True)
    community = models.ForeignKey(Community, models.DO_NOTHING, blank=True, null=True)
    # favicon = models.CharField(max_length=-1, blank=True, null=True)
    # deleted_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        choices=MobilizationStatus.choices, max_length=30, blank=True, null=True
    )
    # traefik_host_rule = models.CharField(max_length=-1, blank=True, null=True)
    # traefik_backend_address = models.CharField(max_length=-1, blank=True, null=True)
    language = models.CharField(max_length=5, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    # theme = models.ForeignKey('Themes', models.DO_NOTHING, blank=True, null=True)

    objects = RequestManager(lookup_field="community")

    class Meta:
        managed = False
        db_table = "mobilizations"


class Block(models.Model):
    mobilization = models.ForeignKey(
        Mobilization, models.DO_NOTHING, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # bg_class = models.CharField(max_length=-1, blank=True, null=True)
    # position = models.IntegerField(blank=True, null=True)
    # hidden = models.BooleanField(blank=True, null=True)
    # bg_image = models.TextField(blank=True, null=True)
    # name = models.CharField(max_length=-1, blank=True, null=True)
    # menu_hidden = models.BooleanField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "blocks"


class Theme(models.Model):
    value = models.TextField(unique=True)
    label = models.TextField()
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "themes"

    def __str__(self):
        return self.label


class Subtheme(models.Model):
    value = models.TextField(unique=True)
    label = models.TextField()
    theme = models.ForeignKey(Theme, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "subthemes"

    def __str__(self):
        return self.label


class WidgetKind(models.TextChoices):
    content = "content", "Conteúdo"
    donation = "donation", "Doação"
    draft = "draft", "Rascunho"
    form = "form", "Formulário"
    phone = "phone", "Pressão por telefone"
    plip = "plip", "PLIP"
    pressure = "pressure", "Pressão por email"


class Widget(models.Model):
    block = models.ForeignKey(Block, models.DO_NOTHING, blank=True, null=True)
    settings = models.JSONField(blank=True, null=True)
    kind = models.CharField(
        max_length=50, choices=WidgetKind.choices, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # sm_size = models.IntegerField(blank=True, null=True)
    # md_size = models.IntegerField(blank=True, null=True)
    # lg_size = models.IntegerField(blank=True, null=True)
    # mailchimp_segment_id = models.CharField(max_length=-1, blank=True, null=True)
    # action_community = models.BooleanField(blank=True, null=True)
    # exported_at = models.DateTimeField(blank=True, null=True)
    # mailchimp_unique_segment_id = models.CharField(max_length=-1, blank=True, null=True)
    # mailchimp_recurring_active_segment_id = models.CharField(max_length=-1, blank=True, null=True)
    # mailchimp_recurring_inactive_segment_id = models.CharField(max_length=-1, blank=True, null=True)
    # goal = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = RequestManager(lookup_field="block__mobilization__community")

    class Meta:
        managed = False
        db_table = "widgets"

    def __str__(self):
        return f"{self.block.mobilization.name} {self.kind} #{self.id}"

    def total_actions(self) -> int:
        if self.kind == "pressure":
            return (
                ActionPressure.objects.filter(widget=self.id)
                .values("activist_id")
                .distinct()
                .count()
            )
        return 0


class ActionPressure(models.Model):
    activist_id = models.PositiveIntegerField()
    widget = models.ForeignKey(Widget, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "activist_pressures"


class Activist(models.Model):
    name = models.CharField(max_length=155)
    first_name = models.CharField(max_length=55, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    # document_number = models.CharField(max_length=-1, blank=True, null=True)
    # document_type = models.CharField(max_length=-1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activists'


class FormEntry(models.Model):
    # widget = models.ForeignKey(Widget, models.DO_NOTHING, blank=True, null=True)
    fields = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    synchronized = models.BooleanField(blank=True, null=True)
    activist = models.ForeignKey(Activist, models.DO_NOTHING, blank=True, null=True)
    # mailchimp_syncronization_at = models.DateTimeField(blank=True, null=True)
    # mailchimp_syncronization_error_reason = models.TextField(blank=True, null=True)
    widget_id = models.IntegerField()
    cached_community_id = models.IntegerField(blank=True, null=True)
    # rede_syncronized = models.BooleanField(blank=True, null=True)
    mobilization_id = models.IntegerField(blank=True, null=True)
    # mailchimp_status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'form_entries'
    
    def __str__(self):
        return f'ID: {self.id} / WidgetID: {self.widget_id}'


class BondeBasePluginModel(CMSPlugin):
    """
    """
    reference_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="ID de referência da widget na plataforma Bonde"
    )

    class Meta:
        abstract = True

    def get_widget(self) -> Widget | None:
        if not self.reference_id:
            return None

        return Widget.objects.get(id=self.reference_id)

    @property
    def widget(self) -> Widget | None:
        return self.get_widget()