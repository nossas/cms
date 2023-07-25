# Super Pressão

Capacidade de criar pressão em diversos canais de comunicação.
Entre eles *email*, *telefone*, *whatsapp*, *twitter*, *instagram*.

::: mermaid
flowchart TD
    A[Usuário preenche os dados] --> B{Escolhe qual canal pressionar}
    B -->|Email| C[Enviar requisição de pressão 01]
    B -->|Telefone| D[Enviar requisição de pressão 02]
    B -->|Twitter| K[Enviar requisição de pressão 03]
    C --> E[Configurar pressão por e-mail]
    E --> F[Enviar mensagem para servidor de e-mail]
    F ---> G[Pós ação]
    D --> H[Ligar para número do ativista]
    H --> I[Conectar com número do alvo]
    I --> J[Finalizar a ligação]
    J --> G
    K --> L[Abrir nova janela com o twitter configurado]
    K -----> G
:::

::: mermaid
classDiagram
    Pressure <|-- EmailPressure
    Pressure <|-- PhonePressure
    Pressure <|-- TwitterPressure
    ActivistAction "*" --o "1" WidgetMobilization
    EmailPressure --> ActivistAction
    PhonePressure --> ActivistAction
    TwitterPressure --> ActivistAction
    WidgetMobilization -- Pressure
    WidgetMobilization -- Donation
    class ActivistAction{
        str name
        str email_address
        str phone_number
        str city
        int action_id
        timestamp action_date
        str action_app_name
    }
    class Donation
    class WidgetMobilization{
        Object settings
        call_action(Activist input) HttpResponse
    }
    class Pressure{
        str targets
        int widget_id
    }
    class EmailPressure~Pressure~{
        str sendgrid
    }
    class PhonePressure~Pressure~{
        str twilio
    }
    class TwitterPressure~Pressure~{
        str message
    }
:::