from dataclasses import dataclass
from pydantic import BaseModel


# Objeto que representa as notas
class Nota(BaseModel):
    id: str
    nota: float
    uc_id: int
    aluno_matricula: int  # Matricula do Aluno

    def key(self):
        return "id"


# Objeto que representa um aluno
class Aluno(BaseModel):
    matricula: int
    nome: str
    notas: list[Nota]

    def key(self):
        return "matricula"


class UnidadeCurricular(BaseModel):
    id: int
    nome: str
    professor_responsavel: int
    alunos_matriculados: list[Aluno]

    def key(self):
        return "id"


class Professor(BaseModel):
    matricula: int
    nome: str
    unidades: list[UnidadeCurricular]

    def key(self):
        return "matricula"
