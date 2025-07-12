# Projeto: Consulta OAB com Agente LLM

Este projeto foi desenvolvido para consultar dados de advogados registrados no site oficial da OAB (Cadastro Nacional dos Advogados - CNA) e responder a perguntas em linguagem natural sobre esses dados utilizando um agente de IA com modelo hospedado na Cloudflare Workers AI.

Objetivos

Automatizar a consulta ao site da OAB;

Expor os dados por meio de uma API REST com FastAPI;

Utilizar OCR para extrair dados presentes em imagens (quando aplicável);

Utilizar um agente LLM (LangChain + Cloudflare Workers AI) para responder perguntas em linguagem natural com base nos dados retornados.

# Funcionalidades

Consulta de advogado por nome;

Extração de:

Número da inscrição

Nome completo

UF da seccional

# Categoria

Data de inscrição (via OCR)

Situação atual (via OCR)

API REST com FastAPI

Integração com modelo LLM para respostas automatizadas.

# Erros encontrados e resolvidos

1. Erro de extração de dados detalhados

Problema: O campo DetailUrl retornado pelo JSON não vinha com o formato esperado, gerando IndexError ao fazer split("RenderDetail").
Solução: A URL completa já vinha no campo DetailUrl, então foi usada diretamente.

# 2. Extração de dados ocultos em imagens

Problema: Os campos data_inscricao e situação são exibidos como imagem no site da OAB.
Solução: Integrado o pytesseract para OCR. Adicionalmente, foi necessário instalar:

Tesseract OCR

Poppler (para extrair texto de PDF, se aplicável)

Pillow, pdf2image

# 3. Erro: pdfinfo_from_path - Poppler não instalado

Solução: Instalado Poppler e adicionado ao PATH do sistema.

 # 4. Erro na importação de CloudflareWorkersAI

Solução: Corrigido o import:

from langchain_community.llms import CloudflareWorkersAI

# 5. Token/API da Cloudflare com rota incorreta

Solução: Utilizado endpoint correto:

https://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/ai/run/@cf/meta/llama-3-8b-instruct

# Como executar localmente

Requisitos:

Python 3.10+

Tesseract OCR instalado

Poppler instalado e no PATH
