from django.db import models


class CandidatureFlowStatus(models.TextChoices):
    # Editando
    draft = "draft", "Cadastro Incompleto"
    # Já enviou um formulário, mas solicitou alterar algumas informações
    editing = "editing", "Edição Incompleta"
    # Passou pelo checkout e submeteu a candidatura
    submitted = "submitted", "Perfil em análise"
    # Não passou nas validações
    invalid = "invalid", "Perfil Reprovado"
    # Passour nas validções
    is_valid = "is_valid", "Perfil Ativo"
    # # Começou a editar, seu perfil continua público, mas o processo de atualizar
    # # a candidatura vai acontecer novamente para os novos dados
    # draft_requested = "draft_requested", "Edição Requisitada"


class IntendedPosition(models.TextChoices):
    empty = "", "Selecione uma opção"
    prefeitura = "prefeitura", "Prefeito/a"
    vereacao = "vereacao", "Vereador/a"


class PoliticalParty(models.TextChoices):
    empty = "", "Selecione o partido"
    agir = "agir", "Agir"
    avante = "avante", "Avante"
    cidadania = "cidadania", "Cidadania"
    dc = "dc", "DC"
    mdb = "mdb", "MDB"
    mobiliza = "mobiliza", "Mobiliza"
    novo = "novo", "Novo"
    patriota = "patriota", "Patriota"
    pcb = "pcb", "PCB"
    pcdob = "pcdob", "PCdoB"
    pco = "pco", "PCO"
    pdt = "pdt", "PDT"
    pl = "pl", "PL"
    pmb = "pmb", "PMB"
    pmn = "pmn", "PMN"
    pode = "pode", "PODE"
    pp = "pp", "PP"
    prd = "prd", "PRD"
    pros = "pros", "PROS"
    prtb = "prtb", "PRTB"
    psb = "psb", "PSB"
    psc = "psc", "PSC"
    psd = "psd", "PSD"
    psdb = "psdb", "PSDB"
    psol = "psol", "PSOL"
    pstu = "pstu", "PSTU"
    pt = "pt", "PT"
    ptb = "ptb", "PTB"
    ptc = "ptc", "PTC"
    pv = "pv", "PV"
    rede = "rede", "Rede"
    republicanos = "republicanos", "Republicanos"
    solidariedade = "solidariedade", "Solidariedade"
    união = "união", "União"
    up = "up", "UP"


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
    bissexual = "bissexual", "Bissexual"
    homossexual = "homossexual", "Homossexual"
    queer = "queer", "Queer"
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

class ElectionStatus(models.TextChoices):
    empty = "", "Selecione uma opção"
    eleita = "eleita", "Eleita/o"
    segundo_turno = "segundo_turno", "Segundo Turno"
    nao_eleita = "nao_eleito", "Não Eleita/o"