# PostaFlow ✉️ - Sistema Distribuído de E-mails Corporativos

Este projeto consiste em um sistema completo de envio de e-mails corporativos utilizando uma arquitetura de microsserviços, totalmente containerizado e orquestrado com Docker Compose. O objetivo é demonstrar a integração de tecnologias de mensageria, configuração distribuída e balanceamento de carga.

## 👥 Equipe e Papéis

Este projeto foi desenvolvido em conjunto. Embora o repositório esteja hospedado na conta de um único usuário para facilitar a entrega e unificação do código-fonte, **todos os membros listados abaixo contribuíram ativamente e de forma igualitária** para a arquitetura, desenvolvimento e testes do sistema.

Abaixo, o foco principal de atuação de cada membro durante o desenvolvimento:

* **Carolina Pichelli Souza:** Desenvolvimento do Frontend (Flask e Interface UI/UX) e integração via chamadas assíncronas.
* **Heloísa Pichelli Souza:** Infraestrutura e DevOps (Configuração do Nginx como Load Balancer, orquestração com Docker e Docker Compose).
* **Lucas Batista de Sousa:** Desenvolvimento do Backend API (Flask) e integração de resiliência utilizando o ZooKeeper.
* **Maicon Pereira Veloso:** Arquitetura de Mensageria (Configuração do RabbitMQ) e desenvolvimento do Worker/Consumer em Python para disparo SMTP.

## 🏗️ Arquitetura do Sistema

O sistema implementa uma arquitetura robusta dividida em camadas:

1. **Load Balancer (Nginx):** Atua como porta de entrada única (Porta 80), distribuindo requisições entre as instâncias de Frontend e Backend.
2. **Frontend (Flask):** Interface web para composição de e-mails, rodando em 3 instâncias para alta disponibilidade.
3. **Backend API (Flask):** Cérebro do sistema que consulta configurações no ZooKeeper e publica mensagens no RabbitMQ. Também opera em 3 instâncias.
4. **ZooKeeper (Configuração):** Armazena configurações de conexão e oferece coordenação de serviços.
5. **RabbitMQ (Mensageria):** Broker que gerencia filas persistentes, garantindo que nenhuma mensagem seja perdida.
6. **Consumer (Email):** Processa as mensagens de forma assíncrona. Implementado com múltiplas instâncias para escalabilidade.
7. **MailHog (SMTP Test):** Servidor SMTP de teste que intercepta os envios para visualização em uma interface web dedicada.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.9+
* **Framework Web:** Flask
* **Mensageria:** RabbitMQ (biblioteca `pika`)
* **Configuração Distribuída:** ZooKeeper (biblioteca `kazoo`)
* **Envio de E-mail:** Biblioteca nativa `smtplib`
* **Orquestração:** Docker & Docker Compose
* **Servidor Web / Load Balancer:** Nginx

## 🚀 Como Executar

### Pré-requisitos
* Docker e Docker Desktop instalados e rodando na sua máquina.

### Passo a Passo
1. Clone este repositório:
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd postaflow
