### Etapas para cadastrar um site

#### Adicionar registro de domínio

Variaveis:
- Comunidade ID (2548): Obrigatório
- Endereço de domínio do SITE (busao.localhost:8000): Obrigatório
- Comentário: Opcional

```
insert into dns_hosted_zones(community_id, domain_name, comment) values(2548, 'busao.localhost:8000', 'Criado manualmente');
```

#### Configurar ALLOWED_HOSTS e novo Site no projeto

Variaveis:
- Endereço de domínio do SITE (busao.localhost:8000): Obrigatório

Adicionar Endereço de domínio na variavel ALLOWED_HOSTS do serviço no Portainer.

Criar novo Site através do Administrador (Linkar tutorial de inserir Novo Site)
