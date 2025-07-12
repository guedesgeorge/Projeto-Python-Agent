import requests
from bs4 import BeautifulSoup
import json

def fetch_oab_data(name: str) -> dict:
    url_busca = "https://cna.oab.org.br/Home/Search"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    session = requests.Session()

    # 1. Obter o token CSRF
    response_get = session.get("https://cna.oab.org.br/")
    soup = BeautifulSoup(response_get.text, "html.parser")
    token_input = soup.find("input", {"name": "__RequestVerificationToken"})
    if not token_input:
        return {"erro": "Token CSRF não encontrado."}
    
    token = token_input.get("value")

    # 2. Enviar o nome
    data = {
        "__RequestVerificationToken": token,
        "IsMobile": "false",
        "NomeAdvo": name,
        "Insc": "",
        "Uf": "",
        "TipoInsc": "1"
    }

    response_post = session.post(url_busca, headers=headers, data=data)
    if response_post.status_code != 200:
        return {"erro": f"Erro na requisição: {response_post.status_code}"}

    try:
        results = json.loads(response_post.text)
    except json.JSONDecodeError:
        return {"erro": "Erro ao decodificar JSON."}

    advogados = []

    for entry in results.get("Data", []):
        nome = entry.get("Nome")
        inscricao = entry.get("Inscricao")
        uf = entry.get("UF")
        categoria = entry.get("TipoInscOab")
        
        detail_url = "https://cna.oab.org.br" + entry.get("DetailUrl")  # Já vem com RenderDetail

        # 3. Acessa o detalhe completo com RenderDetail
        detail_response = session.get(detail_url, headers=headers)
        detail_soup = BeautifulSoup(detail_response.text, "html.parser")

        # Salvando para debug opcional
        with open("html_detalhe_renderizado.html", "w", encoding="utf-8") as f:
            f.write(detail_soup.prettify())

        data_inscricao = None
        situacao = None

        texto = detail_soup.get_text(separator="\n").lower()
        for linha in texto.splitlines():
            if "data de inscrição" in linha:
                data_inscricao = linha.split(":")[-1].strip()
            if "situação" in linha:
                situacao = linha.split(":")[-1].strip()

        advogados.append({
            "nome": nome,
            "inscricao": inscricao,
            "uf": uf,
            "categoria": categoria,
            "data_inscricao": data_inscricao,
            "situacao": situacao
        })

    return {"advogados": advogados}
