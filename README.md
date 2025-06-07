# Wine Tour Experience - Sistema de Gestão de Reservas e Experiências Turísticas

Sistema web desenvolvido em **Python (Django)** para a **Wine Tour Experience**, uma empresa especializada em **Cruzeiros** e **Endoturismo** na região de Lisboa (Douro). O sistema facilita a gestão de reservas, clientes, parceiros, experiências turísticas, pagamentos, faturas, calendário e notificações, proporcionando uma experiência otimizada para todos os envolvidos.

## Funcionalidades

- **Gestão de Reservas**: Controle de reservas de cruzeiros e experiências turísticas, com status de confirmação e histórico.
- **Gestão de Clientes**: Cadastro e gerenciamento de informações dos clientes, incluindo histórico de compras e preferências.
- **Gestão de Parceiros**: Cadastro de parceiros (como vinícolas e operadores turísticos) com informações detalhadas.
- **Experiências Turísticas**: Criação e gerenciamento de pacotes turísticos, como cruzeiros e visitas a vinícolas.
- **Pagamentos e Faturas**: Integração com sistema de pagamentos e geração automática de faturas.
- **Calendário**: Visualização e agendamento de experiências turísticas e reservas.
- **Notificações**: Sistema de notificações por e-mail ou SMS para clientes e equipe.

## Tecnologias

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript (Django Templates)
- **Banco de Dados**: PostgreSQL
- **Autenticação**: Django Allauth
- **Notificações**: Celery (para envio de e-mails e SMS)
- **Pagamentos**: Integração com API de pagamento (ex: Stripe, PayPal)

## Requisitos

Antes de rodar o projeto, certifique-se de ter o seguinte instalado:

- **Python 3.8+**
- **Django 3.2+**
- **PostgreSQL**
- **pip** para gerenciamento de pacotes Python

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/wine-tour-experience.git
cd wine-tour-experience
