from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import models
from database import engine, get_db
from auth import verificar_senha, criar_token, get_usuario_atual, usuarios_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TarefaSchema(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    concluida: bool = False


@app.get("/app")
def frontend():
    return FileResponse("index.html")

@app.get("/")
def inicio():
    return {"mensagem": "API de Tarefas com autenticacao!"}

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    usuario = usuarios_db.get(form.username)
    if not usuario or not verificar_senha(form.password, usuario["senha_hash"]):
        raise HTTPException(status_code=401, detail="Usuario ou senha incorretos")
    token = criar_token({"sub": form.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/tarefas")
def listar_tarefas(
    db: Session = Depends(get_db),
    usuario: str = Depends(get_usuario_atual)
):
    return db.query(models.Tarefa).all()

@app.post("/tarefas")
def criar_tarefa(
    tarefa: TarefaSchema,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_usuario_atual)
):
    nova = models.Tarefa(**tarefa.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@app.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(
    tarefa_id: int,
    tarefa: TarefaSchema,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_usuario_atual)
):
    existente = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not existente:
        raise HTTPException(status_code=404, detail="Tarefa nao encontrada")
    for campo, valor in tarefa.model_dump().items():
        setattr(existente, campo, valor)
    db.commit()
    db.refresh(existente)
    return existente

@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_usuario_atual)
):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa nao encontrada")
    db.delete(tarefa)
    db.commit()
    return {"mensagem": "Tarefa deletada"}