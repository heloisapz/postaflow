# PostaFlow ✉️ - Sistema Distribuído de E-mails Corporativos

[cite_start]Este projeto consiste em um sistema completo de envio de e-mails utilizando uma arquitetura de microsserviços, totalmente containerizado e orquestrado com Docker Compose[cite: 4, 5]. [cite_start]O objetivo é demonstrar a integração de tecnologias de mensageria, configuração distribuída e balanceamento de carga[cite: 4, 7].

## 🏗️ Arquitetura do Sistema

O sistema implementa uma arquitetura robusta dividida em camadas:

1.  [cite_start]**Load Balancer (Nginx):** Atua como porta de entrada única (Porta 80), distribuindo requisições entre as instâncias de Frontend e Backend[cite: 29, 30].
2.  [cite_start]**Frontend (Flask):** Interface web para composição de e-mails, rodando em 3 instâncias para alta disponibilidade[cite: 7, 30].
3.  **Backend API (Flask):** Cérebro do sistema que consulta configurações no ZooKeeper e publica mensagens no RabbitMQ. [cite_start]Também opera em 3 instâncias[cite: 7, 30].
4.  [cite_start]**ZooKeeper (Configuração):** Armazena configurações de conexão e oferece coordenação de serviços[cite: 7, 23].
5.  [cite_start]**RabbitMQ (Mensageria):** Broker que gerencia filas persistentes, garantindo que nenhuma mensagem seja perdida[cite: 7, 19].
6.  **Consumer (Email):** Processa as mensagens de forma assíncrona. [cite_start]Implementado com múltiplas instâncias para escalabilidade[cite: 8, 27].
7.  [cite_start]**MailHog (SMTP Test):** Servidor SMTP de teste que intercepta os envios para visualização em uma interface web dedicada[cite: 8, 25].

## 🛠️ Tecnologias Utilizadas
* [cite_start]**Linguagem:** Python 3.9+[cite: 3].
* [cite_start]**Framework Web:** Flask[cite: 3].
* [cite_start]**Mensageria:** RabbitMQ (pika)[cite: 3].
* [cite_start]**Configuração:** ZooKeeper (kazoo)[cite: 3].
* [cite_start]**Envio de E-mail:** Biblioteca nativa `smtplib`[cite: 3].
* [cite_start]**Orquestração:** Docker & Docker Compose[cite: 3].
* [cite_start]**Servidor Web/LB:** Nginx[cite: 29].

## 🚀 Como Executar

### Pré-requisitos
* Docker Desktop instalado e rodando.

### Passo a Passo
1.  Clone este repositório:
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd postaflow
    ```
2.  Inicie todo o ecossistema:
    ```bash
    docker-compose up --build -d
    ```

### Portas de Acesso
* **Frontend (Aplicação):** [http://localhost](http://localhost) (Porta 80 via Nginx).
* **MailHog (Caixa de Entrada):** [http://localhost:8025](http://localhost:8025).
* **RabbitMQ Management:** [http://localhost:15672](http://localhost:15672) (usuário/senha: `guest`).

## 🛡️ Resiliência e Fallback
O sistema foi projetado para ser resiliente. [cite_start]Caso o ZooKeeper esteja indisponível no momento da requisição, o Backend API utiliza automaticamente configurações de fallback (variáveis de ambiente) para localizar o RabbitMQ e manter o serviço operando[cite: 8].