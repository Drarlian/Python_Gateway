from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse


"""
Quando usar a Validação do Token utilizando o dependencies?
    • Para sistemas simples ou protótipos.
    • Quando o token é fixo ou estático.
    • Quando precisamos de uma solução rápida, sem a necessidade de integrar bibliotecas externas ou configurar fluxos OAuth2/JWT.

No geral, é uma solução customizada e mais simples, mas pode não atender a cenários mais complexos.
"""

app = FastAPI()


# Função de autenticação para uso como dependência
def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token or token != "Bearer my-secure-token":  # Validação simples de exemplo.
        raise HTTPException(status_code=401, detail="Invalid or missing token")


@app.get("/service2/home")
async def home_service2():
    return JSONResponse(status_code=200, content={"message": "Service 2 is Working!"})


@app.get("/service2/configurations", dependencies=[Depends(verify_token)])
async def configurations_service2():
    return JSONResponse(status_code=200, content={"message": "Configuration Endpoint on Service 2 is Working!"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
