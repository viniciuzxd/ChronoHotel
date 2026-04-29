# 🏨 ChronoHotel - Sistema de Gestão de Ponto e Folha de Pagamento

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)

O **ChronoHotel** é uma aplicação desktop completa desenvolvida em Python para automatizar o controle de jornada, gestão de equipe e o cálculo financeiro da folha de pagamento de um hotel. O sistema foi projetado focado em usabilidade, rodando como uma *Single Page Application* (SPA) no Tkinter, garantindo transições fluidas e uma experiência de usuário moderna.

---

## ✨ Principais Funcionalidades

### 🔐 Controle de Acesso Baseado em Cargos (RBAC)
* **Dashboard do Gerente:** Acesso total à criação de usuários, gestão de funcionários, diaristas e emissão de relatórios financeiros mensais.
* **Dashboard da Recepção:** Interface focada na operação diária, permitindo o registro de ponto rápido de qualquer funcionário em serviço.

### 🕒 Motor de Ponto Inteligente
* **Cálculo Automático de Horas:** O sistema calcula as horas decimais trabalhadas com precisão.
* **Turnos Noturnos:** Detecção automática de turnos que cruzam a madrugada (ex: 22h às 06h = 8h trabalhadas).
* **Regras de Negócio Específicas:** Lógica customizada para "Folguistas" em plantões de 24h (domingo a segunda), incluindo acréscimos automáticos de auxílio-alimentação.
* **Entrada Expressa:** Sistema de pop-up minimalista para registro de chegada em apenas 2 cliques.

### 💰 Financeiro e Emissão de Documentos
* **Fechamento de Folha:** Cálculo automático do salário baseado no valor-hora específico de cada cargo.
* **Geração de PDFs (`fpdf`):** * Emissão de recibos de pagamento individuais compactos (3 por folha A4) padronizados com a identidade visual do hotel.
    * Geração de Relatórios Mensais detalhados e consolidados.
* **Controle de Diaristas:** Módulo separado para o lançamento rápido de ajudantes temporários, com geração de folha de pagamento quinzenal em lote.

### 🛡️ Segurança e Banco de Dados
* **Persistência em SQLite:** Banco de dados leve, rápido e embutido.
* **Backup Automático:** Rotina que cria cópias de segurança do banco de dados na pasta `/backups` sempre que o sistema é encerrado.

## 📚 Aprendizado e Desenvolvimento Assistido (IA)

Este projeto teve o apoio de Inteligência Artificial Generativa como ferramenta de mentoria técnica. A IA foi utilizada como um guia para:

* **Arquitetura de Software:** Discussão e implementação do modelo *Single Page Application* (SPA) dentro do Tkinter.
* **Depuração:** Auxílio no diagnóstico e correção de bugs de interface e fluxo de dados.

A transparência sobre o uso da IA reflete meu compromisso com o aprendizado contínuo e com o uso de tecnologias de ponta para otimizar o desenvolvimento de soluções robustas.

---

## 🏗️ Estrutura e Arquitetura do Projeto

O projeto segue uma arquitetura modular, separando a lógica de banco de dados, regras de negócio financeiras e as interfaces (Views):

```text
📦 ChronoHotel
 ┣ 📂 auth/                # Controle de login e gestão de acessos (Recepcionistas/Gerentes)
 ┣ 📂 database/            # Conexão SQLite, criação de tabelas e rotinas de Backup automático
 ┣ 📂 financeiro/          # Motor de cálculo de horas decimais e geração de PDFs (Recibos e Relatórios)
 ┣ 📂 funcionarios/        # CRUD de colaboradores e estruturação hierárquica
 ┣ 📂 ponto/               # Lógica de registro de entrada/saída e validações de turno
 ┣ 📜 main.py              # Ponto de entrada e inicialização do sistema
 ┗ 📜 dashboard.py         # Controladores SPA (Single Page Application) da interface principal