# Versão do Gateway sem o uso de Token para as rotas:

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

"""
Explicação sobre o uso de {path:path}

No caso do Gateway, isso permite capturar o restante do caminho da requisição (após http://localhost:8000) para:
    1. Determinar qual serviço mapeado no ROUTE_MAP deve atender à requisição.
    2. Construir a URL final para redirecionar a requisição ao serviço correto.

Se acessarmos:
    • http://localhost:8000/service1/resource/123, o valor de path será "service1/resource/123".
    • http://localhost:8000/qualquer/coisa/aqui, o valor de path será "qualquer/coisa/aqui".

Ou seja:
    • O {path:path} captura tudo após a barra inicial e envia para o parâmetro path da função.
    • Se você usasse apenas {path}, o FastAPI limitaria a captura a um segmento do caminho (até a próxima barra /).
"""

app = FastAPI()

# Mapear serviços e endpoints
ROUTE_MAP = {
    "/service1": "http://localhost:8001",  # Serviço 1
    "/service2": "http://localhost:8002",  # Serviço 2
}


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(request: Request, path: str):
    service_url = None

    # Loop nos serviços existentes para encontrar o serviço correspondente ao caminho recebido:
    for route, url in ROUTE_MAP.items():
        if path.startswith(route.strip("/")):
            service_url = url
            break

    # Se a url recebida não existir retorna um error:
    if not service_url:
        return JSONResponse(status_code=404, content={"message": "Serviço não encontrado"})

    # Recriando a requisição original: (Basicamente encaminhando o usuário para o serviço solicitado)
    async with httpx.AsyncClient() as client:
        # response = await client.request(method, url, json=body, headers=headers)
        response = await client.request(
            method=request.method,
            url=f"{service_url}/{path}",
            headers=request.headers,
            content=await request.body()
        )

    # Retornando para o usuário o retorno da requisição que foi encaminhada:
    return JSONResponse(status_code=response.status_code, content=response.json())


# Lógica para implementar um middleware para validação de token em todas as rotas da aplicação:
# @app.middleware("http")
# async def verify_auth(request: Request, call_next):
#     auth_header = request.headers.get("Authorization")
#     if not auth_header or not auth_header.startswith("Bearer "):
#         return JSONResponse(status_code=401, content={"message": "Unauthorized"})
#
#     token = auth_header.split(" ")[1]
#     # Verificando o token (JWT ou outro método)
#     if not verify_token(token):  # Lógica de verificação do token.
#         return JSONResponse(status_code=403, content={"message": "Forbidden"})
#
#     return await call_next(request)
#
#
# def verify_token(token: str):
#     return True


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
