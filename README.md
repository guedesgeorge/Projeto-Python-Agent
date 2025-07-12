Estrutura do Repositório GitHub
Para atender aos requisitos do desafio técnico, meu repositório no GitHub tem a seguinte estrutura:

.
├── scraper/
│   ├── __init__.py
│   ├── parse_oab_html.py
│   └── scraper_oab_request.py
├── api/
│   ├── __init__.py
│   └── main.py
├── agent/
│   ├── __init__.py
│   └── agent.py
├── .env.example  # Exemplo de arquivo .env para variáveis de ambiente
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md

Explicação da Estrutura:
scraper/: Aqui está toda a minha lógica de web scraping.

parse_oab_html.py: Esta função é responsável por analisar o HTML e extrair os dados que preciso.

scraper_oab_request.py: É aqui que eu lido com as requisições HTTP, obtenho o token CSRF e orquestro todo o processo de scraping.

api/: Contém a implementação da minha API FastAPI.

main.py: Este arquivo define os endpoints da minha API, especificamente o /fetch_oab.

agent/: Onde está o código do meu agente LLM.

agent.py: Este script implementa a lógica do meu agente, fazendo chamadas tanto para a minha API local quanto para a Cloudflare Workers AI.

.env.example: Um arquivo de exemplo para as variáveis de ambiente (como CF_API_TOKEN e CF_ACCOUNT_ID). É super importante lembrar de nunca commitar meu arquivo .env real com as chaves para o GitHub!

requirements.txt: Lista todas as dependências Python do meu projeto.

Dockerfile: Define como construir a imagem Docker da minha aplicação.

docker-compose.yml: Orquestra os serviços Docker (por exemplo, o scraper/API e o agente, se eu decidir separá-los ou tiver outros serviços).

README.md: Este é o arquivo mais importante para documentar meu projeto, e é o que você está lendo agora!

Esboço para o README.md
Eu me esforcei para que meu README.md seja claro, conciso e forneça todas as informações necessárias para que qualquer pessoa possa entender, instalar e executar meu projeto.

# Meu Projeto: OAB Scraper e LLM Agent

Este é o meu projeto, onde implemento uma solução para consultar dados de advogados(as) no site oficial da OAB (CNA – Cadastro Nacional dos Advogados) e permito que um agente de IA responda perguntas sobre esses dados de forma automática.

## Objetivo

Meu objetivo principal com este projeto é demonstrar minha capacidade de construir serviços Python para web scraping, expor esses serviços via uma API, e integrar um modelo de linguagem (LLM) para processamento de linguagem natural.

## Componentes

1.  **Meu Web Scraper (`scraper/`)**: Eu o construí para consultar o site `https://cna.oab.org.br/`, buscando por nome completo do advogado e UF da seccional. Ele extrai informações como número de inscrição, nome completo, UF, categoria, data de inscrição e situação atual.
2.  **Minha API (`api/`)**: Desenvolvi um servidor FastAPI que expõe o scraper através de um endpoint `POST /fetch_oab`.
3.  **Meu Agente LLM (`agent/`)**: Este agente Python que criei recebe perguntas em português natural como entrada, identifica que precisa consultar a ferramenta `fetch_oab`, chama o serviço MCP (`/fetch_oab`), e gera uma resposta clara e objetiva em português com base nos dados recebidos, utilizando a Cloudflare Workers AI (ou outro LLM que eu tenha configurado).

## Requisitos

* Docker e Docker Compose (para rodar tudo localmente)
* Uma conta na Cloudflare e um token de API para Cloudflare Workers AI (eu estou usando o modelo `@cf/meta/llama-3-8b-instruct` ou similar).

## Configuração do Ambiente

1.  **Para clonar meu repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <nome_do_seu_repositorio>
    ```

2.  **Variáveis de Ambiente:**
    Você precisará criar um arquivo `.env` na raiz do projeto (pode usar o `.env.example` como base) e preencher com suas credenciais da Cloudflare. Aqui estão as minhas, para você ter uma ideia:
    ```
    CF_API_TOKEN="ZTw7CxX6KLjeMAg20PSt2965arefWThtlKr99yA2"
    CF_ACCOUNT_ID="d0393f42f4b3c07bb4214c57372dbe6a"
    ```
    *Você pode encontrar seu `CF_ACCOUNT_ID` no painel da Cloudflare.*

## Instalação e Execução Local (com Docker)

1.  **Para construir as imagens Docker:**
    ```bash
    docker-compose build
    ```

2.  **Para iniciar os serviços:**
    ```bash
    docker-compose up
    ```
    Isso vai iniciar minha API FastAPI (geralmente em `http://localhost:8000`) e o ambiente para o agente.

## Exemplos de Uso

### 1. Via `curl` (chamando a API FastAPI)

Com a API rodando (via `docker-compose up`), você pode testá-la usando `curl` assim:

```bash
curl -X POST "http://localhost:8000/fetch_oab" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "ANTONIO AUGUSTO GENELHU JÚNIOR",
           "uf": ""
         }'

A resposta que você deve esperar (exemplo):

{
  "nome": "ANTONIO AUGUSTO GENELHU JÚNIOR",
  "inscricao": "123456",
  "uf": "RJ",
  "categoria": "Advogado",
  "data_inscricao": "01/01/2000",
  "situacao": "Ativo"
}

2. Via Agente LLM
Para executar o agente e ver a interação com o LLM:

Com os serviços Docker rodando, você pode executar o script agent.py (dentro do contêiner do agente, se você configurou o docker-compose para isso, ou diretamente se estiver testando localmente sem Docker para o agente).

Se você tiver um serviço agent no seu docker-compose.yml, você pode executá-lo assim:

docker-compose run --rm agent python agent/agent.py

A saída que você deve esperar (exemplo):

>> Resultado final:
{'advogados': [{'nome': 'ANTONIO AUGUSTO GENELHU JÚNIOR', 'inscricao': '123456', 'uf': 'RJ', 'categoria': 'Advogado', 'data_inscricao': '01/01/2000', 'situacao': 'Ativo'}]}

Resposta do agente:

A situação atual do advogado ANTONIO AUGUSTO GENELHU JÚNIOR é Ativo.

