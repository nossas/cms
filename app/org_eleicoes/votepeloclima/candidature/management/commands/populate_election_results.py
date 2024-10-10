import csv

from django.core.management.base import BaseCommand
from contrib.bonde.models import PlacesIBGE

from ...models import Candidature, ElectionResult
from ...choices import ElectionStatus


class Command(BaseCommand):
    help = 'Popula os resultados eleitorais a partir de arquivos CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            'eleicao',
            type=str,
            help="Tipo de eleição: 'vereador' ou 'prefeito'."
        )

    def map_situacao_to_status(self, situacao, eleicao):
        """
        Mapeia as situações eleitorais do CSV para os valores do ElectionStatus.
        """
        situacao = situacao.lower()

        if eleicao == "prefeito":
            if situacao == "eleito":
                return ElectionStatus.eleita
            elif situacao == "2º turno":
                return ElectionStatus.segundo_turno
            elif situacao == "não eleito":
                return ElectionStatus.nao_eleita
        elif eleicao == "vereador":
            if situacao in ["eleito", "eleito por qp", "eleito por média"]:
                return ElectionStatus.eleita
            elif situacao == "não eleito" or situacao == "suplente":
                return ElectionStatus.nao_eleita

        return ElectionStatus.empty

    def handle(self, *args, **kwargs):
        eleicao = kwargs['eleicao']

        # Define o caminho correto para o CSV com base no tipo de eleição
        if eleicao == 'vereador':
            csv_path = 'org_eleicoes/votepeloclima/candidature/csv/resultados_primeiro_turno_vereacao_2024.csv'
            csv_key_num = 'numero_na_urna'
        elif eleicao == 'prefeito':
            csv_path = 'org_eleicoes/votepeloclima/candidature/csv/resultados_primeiro_turno_prefeituras_2024.csv'
            csv_key_num = 'numero'
        else:
            self.stdout.write(self.style.ERROR("Tipo de eleição inválido. Use 'vereador' ou 'prefeito'."))
            return

        try:
            # Carrega o CSV em um dicionário com uma chave composta
            csv_data = {}
            with open(csv_path, mode='r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    numero = row[csv_key_num].strip()
                    municipio = row['municipio'].strip().lower()  # Normaliza para lowercase
                    estado = row['estado'].strip().upper()

                    # Cria a chave composta (numero, municipio, estado)
                    chave_composta = f"{numero}|{municipio}|{estado}"

                    csv_data[chave_composta] = row

            # Carrega todas as candidaturas da base de dados
            candidatures = Candidature.objects.all()

            # Itera pelas candidaturas e busca os resultados no CSV
            for candidature in candidatures:
                numero = str(candidature.number_id)

                # Busca o município e estado no banco de dados
                places = PlacesIBGE.objects.filter(
                    codigo_municipio_completo=candidature.city,
                    uf=candidature.state
                )

                if not places.exists():
                    self.stdout.write(self.style.WARNING(f"Nenhum lugar encontrado para a candidatura {numero}. Ignorando..."))
                    continue

                place = places.first()

                municipio = place.nome_municipio.lower()  # Normaliza para lowercase
                estado = place.sigla_uf.upper()

                # Cria a chave composta para a candidatura atual
                chave_composta = f"{numero}|{municipio}|{estado}"

                # Verifica se a candidatura atual existe no CSV
                if chave_composta in csv_data:
                    row = csv_data[chave_composta]

                    # Ajusta as colunas com base no tipo de eleição
                    situacao = row['situacao'].strip()

                    # Mapeia a situação para o ElectionStatus
                    election_status = self.map_situacao_to_status(situacao, eleicao)

                    if election_status == ElectionStatus.empty:
                        self.stdout.write(self.style.WARNING(f"Situação inválida encontrada no CSV: {situacao}. Ignorando..."))
                        continue

                    # Cria ou atualiza o resultado da eleição
                    ElectionResult.objects.update_or_create(
                        candidature=candidature,
                        defaults={'status': election_status}
                    )
                    self.stdout.write(self.style.SUCCESS(f"Resultado da eleição atualizado para candidatura {numero} em {municipio}, {estado}."))
                else:
                    self.stdout.write(self.style.WARNING(f"Resultado não encontrado no CSV para candidatura {numero} em {municipio}, {estado}. Ignorando..."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Arquivo CSV não encontrado no caminho: {csv_path}"))
