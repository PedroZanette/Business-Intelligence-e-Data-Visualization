import persistence
import exception
import model

def init_db():
    persistence.load_database()

def busca_aluno(matricula):
    return persistence.busca_aluno(matricula)

def altera_aluno(matricula, aluno):
    return persistence.altera_aluno(matricula, aluno)

def busca_notas_aluno(matricula):
    return persistence.busca_notas_aluno(matricula)

def cria_aluno(aluno):
    return persistence.cria_aluno(aluno)

