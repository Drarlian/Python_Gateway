from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer


"""
Quando usar a Validação do Token utilizando o OAuth2?
    • Quando o sistema exige autenticação robusta com tokens JWT ou integração OAuth2.
    • Quando desejamos escalabilidade e reusabilidade nas regras de autenticação.
    • Quando o projeto deve seguir padrões amplamente aceitos.
    
No geral, essa solução é mais moderna, flexível e escalável.

É recomendado para sistemas com requisitos de segurança avançados, com OAuth2PasswordBearer e validação JWT.
"""

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")


def verify_token(token: str):
    return True


@app.get("/service1/home")
async def home_service1():
    return JSONResponse(status_code=200, content={"message": "Service 1 is Working!"})


@app.get("/service1/configurations")
async def configurations_service1(token: str = Depends(oauth2_scheme)):
    token_validado: bool = verify_token(token)

    if not token_validado:
        return JSONResponse(status_code=401, content={"message": "Invalid Token"})
    else:
        return JSONResponse(status_code=200, content={"message": "Configuration Endpoint on Service 1 is Working!"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
