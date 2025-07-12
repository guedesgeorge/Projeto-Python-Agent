from bs4 import BeautifulSoup

def parse_oab_html(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    card = soup.select_one(".search-result")

    if not card:
        return {"erro": "Dados não encontrados no HTML."}

    try:
        nome = card.select_one("h4").get_text(strip=True)
        campos = card.select("p")

        dados = {}
        for campo in campos:
            texto = campo.get_text(strip=True)
            if ":" in texto:
                chave, valor = texto.split(":", 1)
                dados[chave.strip().lower()] = valor.strip()

        return {
            "nome": nome,
            "oab": dados.get("número da inscrição", ""),
            "uf": dados.get("uf", ""),
            "categoria": dados.get("categoria", ""),
            "data_inscricao": dados.get("data de inscrição", ""),
            "situacao": dados.get("situação atual", "")
        }

    except Exception as e:
        return {"erro": f"Erro ao extrair dados: {str(e)}"}
