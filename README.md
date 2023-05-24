Open Action Tool
-----------------


<!-- https://stackoverflow.com/questions/70508775/error-could-not-build-wheels-for-pycairo-which-is-required-to-install-pyprojec -->

`sudo apt-get install sox ffmpeg libcairo2 libcairo2-dev`

`sudo apt-get install build-essential cargo`


Como publicar vários sites?

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
Criptograr com a mesma chave o password