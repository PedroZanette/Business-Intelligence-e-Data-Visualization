import requests
import model
import json

# Url base da API. No meu caso, localhost na porta 8000
base_url = 'http://127.0.0.1:8000'

def busca_aluno(base_url, matricula):
    # Usamos o módulo requests para gerar a requisição GET
    response = requests.get(f"{base_url}/aluno/{matricula}")
    # Resposta de sucesso. Nesse caso, a API retorna um JSON
    if response.status_code == 200:
        aluno_dict = json.loads(response.text) 
        aluno = model.Aluno(**aluno_dict)
        print(f"Aluno retornado:\n\t{aluno}")
    elif response.status_code == 404:
        print(f"ERRO: Aluno {matricula} não encontrado!")

def cria_aluno(base_url, aluno):
    # Usamos o módulo requests para gerar a requisição POST
    response = requests.post(f"{base_url}/aluno", json=json.dumps(aluno.__dict__))
    # Resposta de sucesso. Nesse caso, a API retorna um JSON
    if response.status_code == 200:
        print(f"Sucesso:\n\t{response.text}")
    else:
        print(f"ERRO {response.status_code}: {response.text}")

# Aluno que existe
print(f"Buscando aluno {2023001}:")
busca_aluno(base_url, 2023001)
# Aluno que não existe
print(f"Buscando aluno {2023009}:")
busca_aluno(base_url, 2023009)

# Crio um novo alunos
novo_aluno = model.Aluno(matricula=2023009, nome='Felix', notas=[])
cria_aluno(base_url, novo_aluno)
# Aluno que não existe
print(f"Buscando aluno {2023009}:")
busca_aluno(base_url, 2023009)

