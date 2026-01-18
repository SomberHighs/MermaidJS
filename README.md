# Nexus-Notify

![Build Status](https://github.com/SomberHighs/MermaidJS/actions/workflows/main.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)
![Architecture](https://img.shields.io/badge/Architecture-Hexagonal-orange.svg)

**A fault-tolerant notification gateway built with Hexagonal Architecture.**

Nexus-Notify acts as a decoupled abstraction layer between your microservices and notification providers (SendGrid, Twilio, Slack). It handles template rendering, provider failover, and rate limiting, allowing your business logic to remain agnostic of the delivery channel.

## 🏗️ Architecture
This project implements **Ports and Adapters (Hexagonal) Architecture** to ensure the core domain logic remains isolated from infrastructure concerns.

```mermaid
graph TD
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
