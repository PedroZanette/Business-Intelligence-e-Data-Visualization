from typing import Union
from fastapi import FastAPI, HTTPException
import service
import exception
import model

# Create a FastAPI app instance
app = FastAPI()
#Inicializa "base de dados" de alunos
service.init_db()

# Define a GET path operation at the root URL ("/")
@app.get("/")
def read_root():
    return {"Hello": "World"}


# GET para buscar alunos
@app.get("/aluno/{matricula}")
def busca_aluno(matricula: int, q: Union[str, None] = None):
    try:
        aluno = service.busca_aluno(matricula)
        return aluno
    except exception.NotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


# GET para buscar notas
@app.get("/aluno/{matricula}/notas")
def busca_notas_aluno(matricula: int, q: Union[str, None] = None):
    try:
        aluno = service.busca_notas_aluno(matricula)
        return aluno
    except exception.NotFound as e:
        raise HTTPException(status_code=404, detail=e.message)


# POST para criar um aluno
@app.post("/aluno")
def cria_aluno(aluno: model.Aluno, q: Union[str, None] = None):
    try:
        aluno = service.cria_aluno(aluno)
        return aluno
    except exception.InvalidOperation as e:
        raise HTTPException(status_code=400, detail=e.message)


# PUT para alterar um aluno
@app.put("/aluno/{matricula}")
def altera_aluno(matricula: int, aluno: model.Aluno, q: Union[str, None] = None):
    try:
        aluno = service.altera_aluno(matricula, aluno)
        return aluno
    except exception.InvalidOperation as e:
        raise HTTPException(status_code=400, detail=e.message)
    except exception.NotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
