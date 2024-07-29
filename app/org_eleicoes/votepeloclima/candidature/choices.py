from django.db import models


class CandidatureFlowStatus(models.TextChoices):
    draft = "draft", "Editando"
    submitted = "submitted", "Enviado"
    invalid = "invalid", "Inválido"
    is_valid = "is_valid", "Válido"
    draft_requested = "draft_requested", "Edição Requisitada"


class IntendedPosition(models.TextChoices):
    empty = "", "Selecione uma opção"
    prefeitura = "prefeitura", "Prefeitura"
    vice_prefeitura = "vice_prefeitura", "Vice-Prefeitura"
    vereadore = "vereadore", "Vereador(a)"


class PoliticalParty(models.TextChoices):
    empty = "", "Selecione seu partido"
    mdb = "mdb", "MDB"
    pdt = "pdt", "PDT"
    pt = "pt", "PT"
    pcdob = "pcdob", "PCdoB"
    psb = "psb", "PSB"
    psdb = "psdb", "PSDB"
    agir = "agir", "AGIR"
    mobiliza = "mobiliza", "MOBILIZA"
    cidadania = "cidadania", "CIDADANIA"
    pv = "pv", "PV"
    avante = "avante", "AVANTE"
    pstu = "pstu", "PSTU"
    pcb = "pcb", "PCB"
    prtb = "prtb", "PRTB"
    dc = "dc", "DC"
    pco = "pco", "PCO"
    pode = "pode", "PODE"
    republicanos = "republicanos", "REPUBLICANOS"
    psol = "psol", "PSOL"
    psd = "psd", "PSD"
    solidariedade = "solidariedade", "SOLIDARIEDADE"
    novo = "novo", "NOVO"
    rede = "rede", "REDE"
    pmb = "pmb", "PMB"
    up = "up", "UP"
    uniao = "uniao", "UNIÃO"
    prd = "prd", "PRD"


class Gender(models.TextChoices):
    empty = "", "Selecione uma opção"
    mulher_cis = "mulher_cis", "Mulher cis"
    mulher_trans = "mulher_trans", "Mulher trans"
    homem_cis = "homem_cis", "Homem cis"
    homem_trans = "homem_trans", "Homem trans"
    pessoa_nao_binaria = "pessoa_nao_binaria", "Pessoa não binária"
    travesti = "travesti", "Travesti"
    queer = "queer", "Queer"
    mandato_coletivo = "mandato_coletivo", "Mandato Coletivo"
    nao_declarado = "nao_declarado", "Não declarado"


class Sexuality(models.TextChoices):
    empty = "", "Selecione uma opção"
    heterossexual = "heterossexual", "Heterossexual"
    pansexual = "pansexual", "Pansexual"
    assexual = "assexual", "Assexual"
    bissexual = "bissexual", "Bissexual"
    queer = "queer", "Queer"
    gay = "gay", "Gay"
    lesbica = "lesbica", "Lésbica"
    nao_declarada = "nao_declarada", "Não declarada"


class Color(models.TextChoices):
    empty = "", "Selecione uma opção"
    preta = "preta", "Preta"
    parda = "parda", "Parda"
    indigena = "indigena", "Indígena"
    branca = "branca", "Branca"
    amarela = "amarela", "Amarela"
    nao_declarada = "nao_declarada", "Não declarada"


class Education(models.TextChoices):
    empty = "", "Selecione uma opção"
    ensino_fundamental_incompleto = "ensino_fundamental_incompleto", "Ensino Fundamental Incompleto"
    ensino_fundamental_completo = "ensino_fundamental_completo", "Ensino Fundamental Completo"
    ensino_medio_incompleto = "ensino_medio_incompleto", "Ensino Médio Incompleto"
    ensino_medio_completo = "ensino_medio_completo", "Ensino Médio Completo"
    tecnico_incompleto = "tecnico_incompleto", "Técnico Incompleto"
    tecnico_completo = "tecnico_completo", "Técnico Completo"
    superior_incompleto = "superior_incompleto", "Superior Incompleto"
    superior_completo = "superior_completo", "Superior Completo"
    pos_graduacao_incompleta = "pos_graduacao_incompleta", "Pós-Graduação Incompleta"
    pos_graduacao_completa = "pos_graduacao_completa", "Pós-Graduação Completa"
    mestrado_incompleto = "mestrado_incompleto", "Mestrado Incompleto"
    mestrado_completo = "mestrado_completo", "Mestrado Completo"
    doutorado_incompleto = "doutorado_incompleto", "Doutorado Incompleto"
    doutorado_completo = "doutorado_completo", "Doutorado Completo"