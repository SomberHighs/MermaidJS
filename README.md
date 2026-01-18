# MermaidJSgraph TD
    subgraph Client Layer
        User[User / Client App] -->|POST /notify| API[FastAPI Entrypoint]
    end

    subgraph Core Application
        API -->|Validate Request| Svc[Notification Service]
        Svc -->|1. Render Template| Tmpl[Template Engine]
        Svc -->|2. Enqueue Job| Q[Redis Queue]
    end

    subgraph Async Workers
        Worker[Celery/Arq Worker] -->|Fetch Job| Q
        Worker -->|Process Logic| Router{Channel Router}
    end

    subgraph Infrastructure Adapters
        Router -->|Email| EmailAdpt[SMTP Adapter]
        Router -->|SMS| SMSAdpt[Twilio Adapter]
        Router -->|Slack| SlackAdpt[Webhook Adapter]
    end

    subgraph External Services
        EmailAdpt -.->|SMTP| Mailhog[Mailhog (Dev) / SendGrid (Prod)]
        SMSAdpt -.->|HTTP| TwilioAPI[Twilio API]
        SlackAdpt -.->|HTTP| SlackAPI[Slack API]
    end

    classDef core fill:#f9f,stroke:#333,stroke-width:2px;
    classDef infra fill:#bbf,stroke:#333,stroke-width:1px;
    class API,Svc,Tmpl,Q,Worker core;
    class EmailAdpt,SMSAdpt,SlackAdpt,Mailhog infra;
