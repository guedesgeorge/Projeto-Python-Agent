# Projeto OAB Scraper e LLM Agent

Este projeto implementa uma solução para consultar dados de advogados no site oficial da OAB (CNA – Cadastro Nacional dos Advogados) e permite que um agente de IA responda perguntas sobre esses dados.

## Objetivo

O objetivo principal é demonstrar a capacidade de construir serviços Python para web scraping, expor esses serviços via uma API, e integrar um modelo de linguagem (LLM) para processamento de linguagem natural.

## Componentes

1.  **Web Scraper (`scraper/`)**: Consulta o site `https://cna.oab.org.br/` para buscar dados de advogados por nome e UF, extraindo informações como número de inscrição, nome completo, UF, categoria, data de inscrição e situação atual.
2.  **API (`api/`)**: Um servidor FastAPI que expõe o scraper através de um endpoint `POST /fetch_oab`.
3.  **Agente LLM (`agent/`)**: Um agente Python que recebe perguntas em linguagem natural, utiliza a API do scraper como ferramenta e gera respostas claras com base nos dados obtidos, utilizando a Cloudflare Workers AI (ou outro LLM configurado).

## Requisitos

* Docker e Docker Compose (para execução local)
* Conta na Cloudflare e token de API para Cloudflare Workers AI (se estiver usando o modelo `@cf/meta/llama-3-8b-instruct` ou similar).

## Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <nome_do_seu_repositorio>
    ```

2.  **Variáveis de Ambiente:**
    Crie um arquivo `.env` na raiz do projeto (baseado no `.env.example`) e preencha com suas credenciais da Cloudflare:
    ```
    CF_API_TOKEN="seu_token_da_cloudflare"
    CF_ACCOUNT_ID="seu_account_id_da_cloudflare"
    ```
    *Você pode encontrar seu `CF_ACCOUNT_ID` no painel da Cloudflare.*

## Instalação e Execução Local (com Docker)

1.  **Construa as imagens Docker:**
    ```bash
    docker-compose build
    ```

2.  **Inicie os serviços:**
    ```bash
    docker-compose up
    ```
    Isso iniciará a API FastAPI (geralmente em `http://localhost:8000`) e o ambiente para o agente.

## Exemplos de Uso

### 1. Via `curl` (chamando a API FastAPI)

Com a API rodando (via `docker-compose up`), você pode testá-la usando `curl`:

```bash
curl -X POST "http://localhost:8000/fetch_oab" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "ANTONIO AUGUSTO GENELHU JÚNIOR",
           "uf": ""
         }'
