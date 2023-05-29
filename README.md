Bonde CMS
----------

Projeto baseado em Python, Django e Django CMS, utilizado para criar e administrar páginas de campanhas da organização NOSSAS.


## Arquitetura

Além das particularidades da arquitetura herdada pelo framework Django criamos algumas singularidades que se baseia na lógica de negócio deste projeto.

```
CMS
|-- contrib
	|-- bonde
	|-- campaign
|-- project
|-- tailwind
```

O módulo **contrib.bonde** é responsável por gerir modelos de dados existentes no nosso projeto core chamado Bonde, ele possui uma base de dados independentes que inicialmente cuida do acesso dos nossos usuários, ou seja para acessar o CMS este usuário precisa estar previamente cadastrado no Bonde.

O módulo **contrib.campaign** está ligado a nossa capacidade de criar plugins e extensões ao Django CMS utilizado na criação de páginas e campanhas.

A pasta **project** é onde encontramos nossas configurações do projeto, arquivo `settings.py`, `urls.py` e `wsgi.py` por exemplo.

O módulo **tailwind** é onde guardamos nossa estilização, baseada no TailwindCSS ela depende do NodeJS para compilar os estilos que serão utilizados e por isso nosso projeto em modo desenvolvimento depende do uso de 2 abas do terminais, uma que executando o comando `runserver` da aplicação e outro que executa o build do CSS no modo `watch`.


## Como contribuir?

Primeiro é necessário instalar as dependencias de desenvolvimento no seu sistema.

Comando baseado em sistema Debian:

<!-- https://stackoverflow.com/questions/70508775/error-could-not-build-wheels-for-pycairo-which-is-required-to-install-pyprojec -->

`sudo apt-get install sox ffmpeg libcairo2 libcairo2-dev`

`sudo apt-get install build-essential cargo libssl-dev libffi-dev python3-dev`

Clone o repositório e acesse a pasta **cms**:

`git clone git@github.com:nossas/cms.git`

Esse projeto utiliza Python com NodeJS e recomendamos o uso dos ambientes virtuais para manter organizado e isolado as suas dependencias.

**Python**

Criando o ambiente virtual Python com módulo `venv`:

`python3 -m venv venv`

Ativando um ambiente virtual Python:

`source venv/bin/activate`

**Node JS**

Instalando o `nvm` para gerenciamento dos ambientes virtuais NodeJS:

`curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash`

`source ~/.profile`

Instalando a versão NodeJS que será utilizada no desenvolvimento:

`nvm install stable`

Ativando o ambiente virtual NodeJS:

`nvm use stable`

### Instalar dependencias do projeto

Dependencias Python:

`pip install -r requirements.txt`

Dependencias NodeJS (necessário executar dentro da pasta **tailwind**):

`npm i`

### Principais comandos

Executar migrações pendentes:

`python manage.py migrate`

Executando o servidor de desenvolvimento:

`python manage.py runserver`

Executando o build dos estilos CSS (necessário executar dentro da pasta **tailwind**):

`npx tailwindcss -i ./static/css/input.css -o ./static/dist/css/output.css --watch`


### Configurações

Criar um arquivo `.env` na raiz do projeto com as seguintes configurações:

```
DEBUG=
ALLOWED_HOSTS=
CMS_DATABASE_URL=
BONDE_DATABASE_URL=
```

<!-- Como publicar vários sites?

1. Carregar a configuração do site no Django a partir do host

    Importante entender que a marca e o dominio são algo extremamente forte.
        
        Rede Nossas Cidades: nossas.org.br
        
        Meu Rio: meurio.org.br
        
        Minha Manaus: minhamanaus.org.br

    Cada campanha seria acessada inicialmente através de subpaths.

        Essa conta eu não pago: minhamanaus.org.br/essacontaeunaopago
        
        Respeita Paquetá: meurio.org.br/respeitapaqueta
        
        Amazônia contra COVID: nossas.org.br/amazoniacontracovid

2. Publicar em produção:

Exige a configuração dos Sites antecipadamente (Comando, configurar sites buscar sites do Bonde)

Base de dados compartilhada


Dúvidas (É outra camada):

Como manter no mesmo dominio 2 aplicações (Bonde e Novo CMS)
Caso seja negativa, como migrar campanhas já existentes no Bonde

subdominios continuam pro Bonde
enquanto o dominio principal, precisaria ser migrado pro CMS


Remove ideia google autenticate
Criptografar com a mesma chave o password -->