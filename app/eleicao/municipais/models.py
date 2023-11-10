from django.db import models
from django.utils.functional import lazy

from eleicao.csv.choices import get_states


class Candidatura(models.Model):
    nome = models.CharField("Nome completo", max_length=120)
    estado = models.CharField("Estado", max_length=2, choices=lazy(get_states, list)())
    cidade = models.CharField("Cidade", max_length=80)
    bio = models.TextField("Bio")
    numero_candidatura = models.CharField(max_length=8)

    def __str__(self) -> str:
      return self.nome


class Vereador(Candidatura):
    bairro = models.CharField("Bairro", max_length=80)


class Prefeito(Candidatura):
    pass
