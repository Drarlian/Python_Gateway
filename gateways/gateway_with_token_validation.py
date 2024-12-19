# Versão do Gateway com validação de Token para rotas especificas:

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

# Dicionário dinâmico de rotas
routes_config = {
    "service1": {"url": "http://localhost:8001", "have_token": False},
    "service2": {"url": "http://localhost:8002", "have_token": True},
}


# Função para validar token:
def validate_token(token: str):
    if token != "Bearer my-secure-token":  # Validação simples de exemplo.
        raise HTTPException(status_code=401, detail="Invalid or missing token")


# Roteamento dinâmico:
@app.api_route("/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def dynamic_gateway(service_name: str, path: str, request: Request):
    # Verificando se o serviço existe no dicionário de rotas:
    service_config = routes_config.get(service_name)
    if not service_config:
        raise HTTPException(status_code=404, detail="Service not found")

    # Verificando se a rota requer autenticação:
    if service_config["have_token"]:
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Authorization token missing")

        # Validando o token recebido do usuário:
        validate_token(token)

    # Recriando a requisição original: (Basicamente encaminhando o usuário para o serviço solicitado)
    async with httpx.AsyncClient() as client:
        url = f"{service_config['url']}/{service_name}/{path}"
        response = await client.request(
            method=request.method,
            url=url,
            headers=request.headers,
            content=await request.body(),
        )

    # Retornando para o usuário o retorno da requisição que foi encaminhada:
    return JSONResponse(status_code=response.status_code, content=response.json())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
