from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "sua-chave-secreta-troque-em-producao"
ALGORITHM = "HS256"
EXPIRACAO_MINUTOS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

usuarios_db = {
    "gustavo": {
        "username": "gustavo",
        "senha_hash": pwd_context.hash("senha123")
    }
}

def verificar_senha(senha, senha_hash):
    return pwd_context.verify(senha, senha_hash)

def criar_token(dados: dict):
    dados_copia = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=EXPIRACAO_MINUTOS)
    dados_copia.update({"exp": expiracao})
    return jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)

def get_usuario_atual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")