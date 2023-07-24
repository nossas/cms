Pressão
#########

## Atributos de Widget (Bonde)

### Alvos e texto do e-mail
- `settings.pressure_type`
  - unique
  - group
  Configurar o tipo dos alvos: lista única ou grupo.

- `settings.is_subject_list`
  - s
  - n
  Configurar vários assuntos que serão utilizados de maneira aleatória.

- `settings.disable_edit_field`
  - s
  - n
  Habilitar a edição do assunto do corpo do e-mail para o usuário final.

- `settings.targets` (`settings.groups.[0].targets`)
  - name <email@provedor.com>
  Lista de e-mails de alvos.

- `settings.pressure_subject` (`settings.groups.[0].pressure_subject`)
  - "Assunto"
  Assunto do e-mail de pressão.

- `settings.pressure_body`(`settings.groups.[0].pressure_body`)
  - "Corpo do e-mail"
  Corpo do e-mail de pressão.

- `settings.subject_list`
  - ["Assunto", "Assunto"]
  Lista de assuntos que podem ser utilizados de maneira aleatória.

### Otimização do envio

- `settings.optimization_enabled`
  - s
  - n
  Habilita ou desabilita o envio de e-mails em lote.

- `settings.mail_limit`
  - 1000
  Definir limite de envios únicos (primeiros envios até começar a fazer o envio em lote).

- `settings.batch_limit`
  - 1000
  Intervalo de pressões para envio do e-mail (a cada novas 1000 pressões, a gente envia um e-mail).

### Configurações de compartilhamento de sucesso
- `settings.finish_message_type`
  - custom
  - share
  Tipo da renderização da mensagem de sucesso (não afeta envio do e-mail).

- `settings.whatsapp_text`
  - "Texto"
  Mensagem utilizada para compartilhar com o botão Whatsapp (não afeta o envio do e-mail).

### E-mail de agradecimento (AutoFire)
- `settings.sender_name`
  - "Nome do mobilizador"
  Nome do responsável mobilizador/comunicador pela campanha.

- `settings.sender_email`
  - "email@provedor.com"
  Endereço de e-mail utilizado na comunicação do agradecimento.

- `settings.email_subject`
  - "Assunto do e-mail"
  Assunto do e-mail utilizado na comunicação do agradecimento.

- `settings.email_text`
  - "Corpo do e-mail"
  Corpo do e-mail utilizado na comunicação do agradecimento.


### Informações de interface
Nenhum afeta o envio de e-mail.

- `settings.call_to_action`
  - "Titulo do formulário"
  Chamada principal do formulário.

- `settings.button_text`
  - "Enviar"
  Texto utilizado no botão de envio.

- `settings.count_text`
  - "pessoas já assinaram"
  Texto utilizado na apresentação do contador.

- `settings.show_state`
  - s
  - n
  Adiciona select de Estado no formulário.

- `settings.show_city`
  - "São Paulo"
  Adiciona input de cidade no formulário.

- `settings.main_color`
  - "#F9F9F9"
  Cor padrão para customizar a estilização do formulário.
