import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Carrega token e ID da Cloudflare do .env
CF_API_TOKEN = os.getenv("CF_API_TOKEN")
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")

# Função que consulta a API local FastAPI do seu scraper
def buscar_dados_oab(nome: str) -> str:
    url = "http://localhost:8000/fetch_oab"
    payload = {"name": nome, "uf": ""}
    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return (
                f"Nome: {data['nome']}\n"
                f"Inscrição: {data['oab']}\n"
                f"UF: {data['uf']}\n"
                f"Categoria: {data['categoria']}\n"
                f"Data de inscrição: {data['data_inscricao']}\n"
                f"Situação: {data['situacao']}"
            )
        else:
            return f"Erro ao buscar dados: {response.status_code}"
    except Exception as e:
        return f"Erro de requisição: {str(e)}"

# Função que chama a API da Cloudflare Workers AI
def chamar_llm_cloudflare(mensagem: str) -> str:
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/meta/llama-3-8b-instruct"
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "system", "content": "Você é um assistente jurídico que responde com base em dados da OAB."},
            {"role": "user", "content": mensagem}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["result"]["response"]
        else:
            return f"Erro do modelo LLM: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Erro ao chamar Cloudflare Workers AI: {str(e)}"

# Executa a lógica completa
if __name__ == "__main__":
    nome_advogado = "ANTONIO AUGUSTO GENELHU JÚNIOR"
    dados = buscar_dados_oab(nome_advogado)
    pergunta = f"Com base nos dados abaixo, responda a pergunta: Qual é a situação do advogado?\n\n{dados}"
    resposta = chamar_llm_cloudflare(pergunta)
    print("\nResposta do agente:\n")
    print(resposta)
