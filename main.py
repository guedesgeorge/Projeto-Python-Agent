from fastapi import FastAPI
from scraper_oab_request import fetch_oab_data
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class OABRequest(BaseModel):
    name: str
    uf: str

@app.get("/")
def read_root():
    return {"message": "API está funcionando!"}

@app.post("/fetch_oab")
def buscar_oab(request: OABRequest):
    try:
        resultado = fetch_oab_data(request.name)
        if not resultado.get("advogados"):
            return JSONResponse(content={"erro": "Advogado não encontrado."}, status_code=404)
        
        # Se quiser buscar por UF também, pode aplicar filtro aqui
        dados = resultado["advogados"][0]
        return {
            "oab": dados["inscricao"],
            "nome": dados["nome"],
            "uf": dados["uf"],
            "categoria": dados["categoria"],
            "data_inscricao": dados["data_inscricao"],
            "situacao": dados["situacao"]
        }
    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)
