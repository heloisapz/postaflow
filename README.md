# ✉️ PostaFlow — Sistema Distribuído de E-mails Corporativos

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-Web_Framework-000000?style=for-the-badge&logo=flask"/>
  <img src="https://img.shields.io/badge/RabbitMQ-Mensageria-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-Containerizado-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Nginx-Load_Balancer-009639?style=for-the-badge&logo=nginx&logoColor=white"/>
</p>

---

## 📌 Sobre o Projeto

O **PostaFlow** consiste em um sistema completo de envio de e-mails corporativos utilizando uma arquitetura de microsserviços, totalmente containerizado e orquestrado com Docker Compose.

O objetivo do projeto é demonstrar a integração de tecnologias modernas de:

- 📬 Mensageria assíncrona  
- ⚙️ Configuração distribuída  
- 🔄 Balanceamento de carga  
- 🐳 Containerização  
- 🛡️ Resiliência e fallback  

---

# 👥 Equipe e Papéis

> Este projeto foi desenvolvido em conjunto.  
> Embora o repositório esteja hospedado na conta de um único usuário para facilitar a entrega e unificação do código-fonte, todos os membros listados abaixo contribuíram ativamente e de forma igualitária para a arquitetura, desenvolvimento e testes do sistema.

---

### 🎨 Carolina Pichelli Souza
- Desenvolvimento do Frontend (Flask e Interface UI/UX)
- Integração via chamadas assíncronas

### ⚙️ Heloísa Pichelli Souza
- Infraestrutura e DevOps
- Configuração do Nginx como Load Balancer
- Orquestração com Docker e Docker Compose

### 🧠 Lucas Batista de Sousa
- Desenvolvimento do Backend API (Flask)
- Integração de resiliência utilizando o ZooKeeper

### 📨 Maicon Pereira Veloso
- Arquitetura de Mensageria
- Configuração do RabbitMQ
- Desenvolvimento do Worker/Consumer em Python para disparo SMTP

---

# 🏗️ Arquitetura do Sistema

```text
                ┌────────────────────┐
                │       NGINX        │
                │   Load Balancer    │
                └─────────┬──────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
┌───────▼────────┐                ┌────────▼───────┐
│   Frontend     │                │   Backend API  │
│ Flask (x3)     │                │ Flask (x3)     │
└───────┬────────┘                └────────┬───────┘
        │                                   │
        │                         ┌─────────▼─────────┐
        │                         │     RabbitMQ      │
        │                         │  Mensageria/Fila  │
        │                         └─────────┬─────────┘
        │                                   │
        │                         ┌─────────▼─────────┐
        │                         │     Consumer      │
        │                         │ Processamento SMTP│
        │                         └─────────┬─────────┘
        │                                   │
        │                         ┌─────────▼─────────┐
        │                         │      MailHog      │
        │                         │ SMTP de Testes    │
        │                         └───────────────────┘

                 ┌──────────────────────┐
                 │      ZooKeeper       │
                 │ Configuração Central │
                 └──────────────────────┘
```

# 🛠️ Tecnologias Utilizadas

<div align="center">

| Categoria | Tecnologia |
|:---:|---|
| 🐍 **Linguagem** | `Python 3.9+` |
| 🌐 **Framework Web** | `Flask` |
| 📨 **Mensageria** | `RabbitMQ (pika)` |
| ⚙️ **Configuração** | `ZooKeeper (kazoo)` |
| 📧 **Envio de E-mail** | `smtplib (nativo)` |
| 🐳 **Orquestração** | `Docker & Docker Compose` |
| 🔀 **Servidor / Load Balancer** | `Nginx` |

</div>

---

# 🛡️ Resiliência e Fallback

O sistema utiliza uma estratégia de **fallback** para garantir **continuidade operacional** e maior tolerância a falhas.

> Caso o **ZooKeeper** esteja indisponível, o **Backend API** passa automaticamente a consumir variáveis de ambiente locais para localizar o **RabbitMQ**, garantindo que o serviço continue funcionando sem interrupções.

---

# 🚀 Como Executar

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de possuir instalado em sua máquina:

- ✅ Docker
- ✅ Docker Desktop

---

## ▶️ Passo a Passo

### 1️⃣ Clone o repositório

```bash id="3ph8d2"
git clone https://github.com/heloisapz/postaflow.git
```
## ▶️ Passo a Passo

### 2️⃣ Acesse a pasta do projeto

```bash
cd postaflow
```

---

### 3️⃣ Inicie os containers

```bash
docker-compose up --build -d
```

---

# 🌐 Portas de Acesso

<div align="center">

| Serviço | URL |
|---|---|
| 🖥️ Frontend | `http://localhost` |
| 📬 MailHog | `http://localhost:8025` |
| 📨 RabbitMQ | `http://localhost:15672` |
| 🔑 RabbitMQ Login | `guest / guest` |

</div>

---

# 🛑 Para Parar o Sistema

```bash
docker-compose down
```

---

# 📦 Estrutura da Solução

```text
postaflow/
│
├── frontend/
├── backend/
├── consumer/
├── nginx/
├── zookeeper/
├── rabbitmq/
├── docker-compose.yml
└── README.md
```

---

# ✨ Destaques do Projeto


✅ Arquitetura baseada em microsserviços  
✅ Processamento assíncrono com filas  
✅ Balanceamento de carga com Nginx  
✅ Configuração distribuída com ZooKeeper  
✅ Containerização completa com Docker  
✅ Estratégia de fallback para alta disponibilidade  
✅ Ambiente de testes SMTP com MailHog  
