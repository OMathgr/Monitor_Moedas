# 💱 Monitor de Cotações de Moedas

Aplicação desenvolvida em Python para monitorar, em tempo real, as cotações de moedas estrangeiras em relação ao Real brasileiro (BRL).

O projeto realiza consultas periódicas a uma API de cotações, calcula a variação dos valores, apresenta as informações em um dashboard no terminal e armazena o histórico das cotações em um banco de dados SQLite.

## 🎯 Objetivo

Este projeto foi desenvolvido como prática de:

* Consumo de APIs REST;
* Requisições HTTP com Python;
* Manipulação de dados em JSON;
* Programação Orientada a Objetos;
* Persistência de dados com SQLite;
* Tratamento de exceções;
* Organização de projetos Python;
* Automação de consultas periódicas.

## ⚙️ Funcionalidades

* Consulta das cotações de moedas em relação ao BRL;
* Monitoramento automático das cotações;
* Atualização a cada 30 segundos;
* Exibição das cotações em um dashboard no terminal;
* Cálculo da variação absoluta entre consultas;
* Cálculo da variação percentual;
* Indicação visual de alta e baixa;
* Sistema de alertas baseado em variação de preço;
* Registro das cotações em banco de dados SQLite;
* Armazenamento de histórico das consultas;
* Tratamento de erros de conexão, timeout e respostas HTTP.

### Moedas monitoradas atualmente

| Código | Moeda |
| ------ | ----- |
| USD    | Dólar |
| EUR    | Euro  |
| GBP    | Libra |

## 🗂️ Estrutura do projeto

```text
Monitor_Moedas/
│
├── data/
│   └── banco.py              # Persistência e consulta do histórico
│
├── models/
│   └── moeda.py              # Modelo e regras de negócio das moedas
│
├── services/
│   └── cotacao.py            # Comunicação com a API de cotações
│
├── .gitignore
├── main.py                   # Ponto de entrada da aplicação
├── moedas.db                 # Banco SQLite criado automaticamente
└── requirements.txt          # Dependências do projeto
```

> O arquivo `moedas.db` é gerado automaticamente durante a execução e não precisa ser versionado no Git.

## 🧩 Arquitetura

O projeto utiliza uma separação simples de responsabilidades:

### `models/`

Contém as classes responsáveis pela representação e comportamento dos objetos utilizados pela aplicação.

A classe `Moeda` mantém informações como:

* código da moeda;
* nome;
* valor atual;
* valor anterior;
* histórico;
* limites de alerta.

Também é responsável pelos cálculos de variação e pelo gerenciamento dos alertas.

### `services/`

Responsável pela comunicação com serviços externos.

O módulo `cotacao.py` realiza as requisições à API, processa a resposta JSON e atualiza os objetos `Moeda`.

### `data/`

Responsável pela persistência dos dados.

O módulo `banco.py` utiliza SQLite para armazenar e recuperar o histórico das cotações.

### `main.py`

Responsável pela execução principal da aplicação, atualização periódica das cotações e apresentação do dashboard no terminal.

## 🌐 API

As cotações são obtidas através da AwesomeAPI.

O projeto utiliza o endpoint:

```text
https://economia.awesomeapi.com.br/json/last
```

As moedas são consultadas no formato:

```text
USD-BRL
EUR-BRL
GBP-BRL
```

A aplicação utiliza o valor `bid` retornado pela API como cotação utilizada no monitoramento.

## 🛠️ Tecnologias utilizadas

* **Python 3**
* **Requests** — requisições HTTP
* **SQLite** — armazenamento do histórico
* **Git/GitHub** — versionamento e hospedagem do projeto

## 🚀 Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/Monitor_Moedas.git
```

Entre na pasta:

```bash
cd Monitor_Moedas
```

### 2. Crie um ambiente virtual

No Windows:

```bash
python -m venv venv
```

Ative o ambiente virtual:

```bash
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o projeto

```bash
python main.py
```

O monitor iniciará as consultas e atualizará o dashboard automaticamente.

Para encerrar:

```text
Ctrl + C
```

## 🖥️ Exemplo de funcionamento

```text
╔══════════════════════════════════════════════════════════╗
║                 MONITOR DE COTAÇÕES                     ║
║                    25/09/2026 16:30:00                 ║
╠══════════════════════════════════════════════════════════╣
║  Dólar    R$  5.3200  ▲ +0.0120 (+0.23%)              ║
║  Euro     R$  6.2400  ▼ -0.0180 (-0.29%)              ║
║  Libra    R$  7.1800  ━ +0.0000 (+0.00%)              ║
╚══════════════════════════════════════════════════════════╝

  Próxima atualização em 30s — Ctrl+C para sair
```

> Os valores apresentados acima são apenas um exemplo visual e não representam cotações reais.

## 🗄️ Banco de dados

As cotações são armazenadas em um banco SQLite local.

A tabela `historico` possui os seguintes campos:

| Campo       | Tipo    | Descrição               |
| ----------- | ------- | ----------------------- |
| `id`        | INTEGER | Identificador único     |
| `codigo`    | TEXT    | Código da moeda         |
| `valor`     | REAL    | Valor da cotação        |
| `data_hora` | TEXT    | Data e hora da consulta |

Isso permite consultar posteriormente o histórico das cotações registradas.

## 🚨 Sistema de alertas

Após a primeira cotação recebida, o sistema define automaticamente uma faixa de alerta em torno do valor inicial.

Quando uma cotação ultrapassa um dos limites, o sistema:

1. Identifica se o valor ultrapassou o limite superior ou inferior;
2. Exibe um alerta no dashboard;
3. Registra qual limite foi atingido;
4. Reajusta a faixa de alerta com base no novo valor.

## 📚 Conceitos praticados

Este projeto foi desenvolvido principalmente como exercício prático de integração entre diferentes componentes de uma aplicação Python.

Entre os conceitos praticados estão:

* Classes e objetos;
* Propriedades (`@property`);
* Métodos especiais (`__str__` e `__repr__`);
* Listas e dicionários;
* Compreensão de listas;
* Requisições HTTP;
* APIs REST;
* JSON;
* Tratamento de exceções;
* SQLite;
* SQL parametrizado;
* Organização modular;
* Ambientes virtuais;
* Versionamento com Git.

## 🗺️ Roadmap

O projeto será desenvolvido de forma incremental, começando com uma aplicação executada no terminal e evoluindo posteriormente para uma aplicação web, sistema de notificações e aplicativo mobile.

### 🟢 Versão 1 — Monitor no Terminal

**Status: Em desenvolvimento**

* [x] Dashboard no terminal
* [x] Monitoramento de USD, EUR e GBP
* [x] Consulta periódica à API de cotações
* [x] Cálculo da variação absoluta
* [x] Cálculo da variação percentual
* [x] Indicador visual de alta e baixa
* [x] Persistência do histórico em SQLite
* [x] Alertas de variação no terminal
* [x] Configuração personalizada dos limites de alerta

### 🔵 Versão 2 — Dashboard Web

**Objetivo:** transformar o monitor de terminal em uma interface web para visualização e interação com os dados.

* [ ] Dashboard web
* [ ] Página individual para cada moeda
* [ ] Gráfico do histórico de cotações
* [ ] Variação percentual
* [ ] Cotação máxima do dia
* [ ] Cotação mínima do dia
* [ ] Alertas visuais na interface
* [ ] Definição de valor de alerta pelo usuário
* [ ] Seleção das moedas monitoradas

### 🟣 Versão 3 — Notificações

**Objetivo:** permitir que o usuário receba alertas mesmo quando não estiver acompanhando o dashboard.

* [ ] Integração com Telegram Bot
* [ ] Notificação quando uma moeda atingir o valor configurado
* [ ] Notificação de variações relevantes
* [ ] Configuração das moedas monitoradas
* [ ] Configuração dos valores de alerta
* [ ] Controle das notificações pelo Telegram

### 🟠 Versão 4 — API e Aplicativo Mobile

**Objetivo:** transformar o projeto em uma aplicação distribuída, com uma API própria responsável por disponibilizar os dados para diferentes clientes.

#### Backend

* [ ] Criar API própria com FastAPI
* [ ] Endpoints para consulta das moedas
* [ ] Endpoints para histórico
* [ ] Endpoints para alertas
* [ ] Persistência estruturada dos dados
* [ ] Documentação automática da API
* [ ] Autenticação de usuários

#### Mobile

* [ ] Aplicativo mobile consumindo a API própria
* [ ] Dashboard de cotações
* [ ] Página individual das moedas
* [ ] Gráficos históricos
* [ ] Configuração de alertas
* [ ] Recebimento de notificações

**Tecnologias a avaliar:**

* React Native
* Flutter

## 🎯 Objetivo final

Evoluir o projeto de um simples monitor de cotações para uma aplicação completa, composta por:

```text
                    ┌─────────────────┐
                    │   AwesomeAPI    │
                    │  Cotações BRL   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Backend     │
                    │     FastAPI     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │   Web    │   │ Telegram │   │  Mobile  │
        │Dashboard │   │   Bot    │   │   App    │
        └──────────┘   └──────────┘   └──────────┘
```

A aplicação deverá utilizar uma única fonte de dados própria, permitindo que diferentes interfaces consumam as mesmas informações de cotações, histórico e alertas.

## 👨‍💻 Autor

Desenvolvido por **Matheus Graciano Ribeiro** como projeto de estudo em Python, com foco em integração com APIs, orientação a objetos e persistência de dados.

[GitHub](https://github.com/OMathgr)
