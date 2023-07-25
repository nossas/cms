from django.db import models


class Group(models.Model):
    name = models.CharField(verbose_name="Nome do grupo", max_length=150)
    reference_json = models.JSONField(
        verbose_name="Objeto de referência", blank=True, null=True
    )

    class Meta:
        verbose_name = "grupo"

    def __str__(self):
        return self.name or self.reference_json.get("name")


class Campaign(models.Model):
    """Campanha que representa a causa da mobilização""",

    name = models.CharField(verbose_name="Nome da ação", max_length=255)
    slug = models.SlugField(
        verbose_name="Slug",
        help_text="Deve ser único para cada ação, usado para agrupar seus dados",
        unique=True,
    )
    settings = models.JSONField(blank=True, null=True)
    owner_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="Criado em", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "campanha"

    def __str__(self):
        return self.name


class OriginActionChoices(models.TextChoices):
    table_activist_pressures = "table:activist_pressures", "Tabela ação de ativistas"
    app_super_pressure = "app:super_pressure", "App de superpressão"
    upload_csv = "upload:csv", "Upload de arquivo CSV"
    app_lunda_donation = "app:lunda_donation", "Doação pelo Lunda"
    app_cms_pressure = "app:cms_pressure_email", "Pressão pelo CMS"


class Action(models.Model):
    given_name = models.CharField(verbose_name="Primeiro nome", max_length=50)
    family_name = models.CharField(
        verbose_name="Sobrenome", max_length=105, blank=True, null=True
    )
    email_address = models.EmailField(verbose_name="Endereço de e-mail")
    phone_number = models.CharField(verbose_name="Número de telefone", max_length=15)
    city = models.CharField(
        verbose_name="Cidade", max_length=100, blank=True, null=True
    )

    # Relação com Campanha
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    # Relação com a origem dos dados
    origin_uid = models.PositiveIntegerField(verbose_name="ID da ação")
    origin_name = models.CharField(
        verbose_name="Origem da ação",
        max_length=100,
        choices=OriginActionChoices.choices,
    )
    origin_action_date = models.DateTimeField(
        verbose_name="Data da ação", auto_now_add=True
    )

    class Meta:
        verbose_name = "ação"
        verbose_name_plural = "ações"
        indexes = [
            models.Index(
                fields=[
                    "origin_name",
                    "origin_action_date",
                ]
            ),
        ]