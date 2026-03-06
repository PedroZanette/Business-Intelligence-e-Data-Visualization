import pandas as pd
import os

# Cria o diretório de dados se não existir
os.makedirs("data", exist_ok=True)

# --- 1. Dados de Professores ---
professores_data = [
    {"matricula": 101, "nome": "Alan Turing"},
    {"matricula": 102, "nome": "Ada Lovelace"},
    {"matricula": 103, "nome": "Grace Hopper"}
]
df_professores = pd.DataFrame(professores_data)
df_professores.to_json("data/professores.json", orient="records", indent=4)
print("Gerado: data/professores.json")

# --- 2. Dados de Unidades Curriculares (UCs) ---
# Possui chave estrangeira 'professor_responsavel' para praticar merge com Professores
ucs_data = [
    {"id": 1, "nome": "Algoritmos e Estrutura de Dados", "professor_responsavel": 101},
    {"id": 2, "nome": "Banco de Dados", "professor_responsavel": 102},
    {"id": 3, "nome": "Inteligência Artificial", "professor_responsavel": 101},
    {"id": 4, "nome": "Engenharia de Software", "professor_responsavel": 103}
]
df_ucs = pd.DataFrame(ucs_data)
df_ucs.to_json("data/ucs.json", orient="records", indent=4)
print("Gerado: data/ucs.json")

# --- 3. Dados de Alunos ---
alunos_data = [
    {"matricula": 2023001, "nome": "João da Silva"},
    {"matricula": 2023002, "nome": "Maria Oliveira"},
    {"matricula": 2023003, "nome": "Pedro Santos"},
    {"matricula": 2023004, "nome": "Ana Souza"}
]
df_alunos = pd.DataFrame(alunos_data)
df_alunos.to_json("data/alunos.json", orient="records", indent=4)
print("Gerado: data/alunos.json")

# --- 4. Tabela de Notas (Intersecção) ---
# Esta é a tabela principal para praticar MERGE.
# Ela liga Aluno (matricula) com UC (uc_id) e atribui um valor (nota).
notas_data = [
    # João faz Algoritmos e Banco de Dados
    {"id": "N1", "aluno_matricula": 2023001, "uc_id": 1, "nota": 8.5},
    {"id": "N2", "aluno_matricula": 2023001, "uc_id": 2, "nota": 7.0},
    
    # Maria faz apenas Algoritmos
    {"id": "N3", "aluno_matricula": 2023002, "uc_id": 1, "nota": 9.0},
    
    # Pedro faz IA e Engenharia de Software
    {"id": "N4", "aluno_matricula": 2023003, "uc_id": 3, "nota": 6.5},
    {"id": "N5", "aluno_matricula": 2023003, "uc_id": 4, "nota": 10.0},
    
    # Ana faz Banco de Dados e IA
    {"id": "N6", "aluno_matricula": 2023004, "uc_id": 2, "nota": 8.0},
    {"id": "N7", "aluno_matricula": 2023004, "uc_id": 3, "nota": 9.5}
]
df_notas = pd.DataFrame(notas_data)
df_notas.to_json("data/notas.json", orient="records", indent=4)
print("Gerado: data/notas.json")