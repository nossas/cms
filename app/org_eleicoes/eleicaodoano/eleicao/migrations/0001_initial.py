# Generated by Django 3.2 on 2023-08-16 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AM', 'Amazonas'), ('AP', 'Amapá'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MG', 'Minas Gerais'), ('MS', 'Mato Grosso do Sul'), ('MT', 'Mato Grosso'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('PR', 'Paraná'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('RS', 'Rio Grande do Sul'), ('SC', 'Santa Catarina'), ('SE', 'Sergipe'), ('SP', 'São Paulo'), ('TO', 'Tocantins')], max_length=2, verbose_name='Estado')),
                ('city', models.CharField(max_length=80, verbose_name='Cidade')),
                ('neighborhood', models.CharField(max_length=80, verbose_name='Bairro onde se candidatou')),
            ],
        ),
        migrations.CreateModel(
            name='PollingPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nome')),
                ('address_line', models.CharField(blank=True, max_length=200, null=True, verbose_name='Endereço')),
                ('places', models.ManyToManyField(to='eleicao.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nome')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('whatsapp', models.CharField(blank=True, max_length=15, null=True, verbose_name='Whatsapp')),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eleicao.pollingplace')),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=120, unique=True, verbose_name='Seu link personalizado')),
                ('name', models.CharField(max_length=120, verbose_name='Nome completo')),
                ('bio', models.TextField(verbose_name='Minibio')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('birth', models.DateField(verbose_name='Data de nascimento')),
                ('occupation', models.CharField(max_length=100, verbose_name='Profissão')),
                ('photo', models.FileField(blank=True, help_text='Envie uma foto horizontal com no mínimo 700 pixels de largura, nos formatos JPEG ou PNG, para garantir a melhor qualidade visual. 📸✨', null=True, upload_to='candidaturas/fotos/', verbose_name='Foto')),
                ('video', models.FileField(blank=True, help_text='Carregue um vídeo de até 30 segundos na posição horizontal, escolhendo entre os formatos MP4, AVI ou MOV. 🎥📽️', null=True, upload_to='candidaturas/videos/', verbose_name='Video')),
                ('gender', models.CharField(choices=[('homem', 'Homem'), ('mulher', 'Mulher'), ('não binário', 'Não binário'), ('travesti', 'Travesti'), ('queer', 'Queer'), ('não declarado', 'Não declarado')], max_length=30, verbose_name='Gênero')),
                ('is_trans', models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=False, verbose_name='Se identifica como pessoa transgênero/transexual?')),
                ('race', models.CharField(choices=[('branca', 'Branca'), ('preta', 'Preta'), ('amarela', 'Amarela'), ('indigena', 'Indigena'), ('parda', 'Parda'), ('não declarada', 'Não declarada')], max_length=30, verbose_name='Raça')),
                ('social_media', models.JSONField(blank=True, null=True, verbose_name='Rede social')),
                ('number', models.PositiveSmallIntegerField(verbose_name='Numero de voto')),
                ('is_reelection', models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=False, verbose_name='Está se candidatando para reeleição?')),
                ('newsletter', models.BooleanField(default=False, verbose_name='Quero receber atualizações da campanha e do NOSSAS.')),
                ('status', models.CharField(choices=[('published', 'Publicado'), ('disabled', 'Desabilitado')], default='published', max_length=30, verbose_name='Status')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eleicao.address')),
            ],
        ),
    ]