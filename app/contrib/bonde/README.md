# Bonde (Database / API)
Parte central da plataforma de ativismo, com objetivo de definir modelos de dados e implementações visando simplificar a construção de ferramentas.

Exemplos de ferramentas em desenvolvimento: CMS e BOT
Exemplos de ferramentos integradas: CRM

## Idiomas

**Comunidade:** Modelo grupo, responsável por contextualizar Campanhas, Ações, Mobilizadores e Ativistas

**Mobilizador:** Pessoa capaz de criar e usar diferentes estrategias de Ação para mobilizar Ativistas

**Ativista:** Pessoa que engaja em Campanhas e Ações em prol do interesse coletivo

**Campanha:** Causa projeto que pode utilizar uma ou mais estratégias de Ação para mobilizar Ativistas

**Ação:** Resultado da interação entre o Ativista e uma Estrategia de Campanha


## Modelo de domínio: BONDE (Plataforma de ativismo)

```mermaid
---
title: BONDE (Plataforma de ativismo)
---
classDiagram
  Comunidade <.. Membro
  Membro <-- Mobilizador
  Comunidade <.. Campanha
  note for Acao "identificador é um atributo único utilizado na ação"
  Ativista ..> Acao
  Acao ..> Estrategia
  Campanha --> Estrategia
  class Comunidade {
    +JSON assinatura
    +JSON integrações
    +agrupar_ativistas(JSON filtro) List~Ativista~
  }
  class Membro {
    +string função
    +agrupar_membros(JSON filtro) List~Mobilizador~
  }
  class Mobilizador {
    +string email
  }
  class Campanha {
    +string nome
    +List~string~ temas
    +agrupar_estrategias(JSON filtro) List~Ação~
    +agrupar_ativistas(JSON filtro) List~Ativistas~
  }
  class Estrategia {
    +string tática
    +JSON configurações
  }
  class Acao {
    +string identificador
  }
  class Ativista {
    +string nome
    +List~string~ endereços_de_email
    +List~string~ números_de_telefone
    +List~string~ endereços
    +JSON dados_adicionais
    +criar_acao(JSON atributos) Acao
  }
```
