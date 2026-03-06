import typing
from dataclasses import asdict
from fastapi import FastAPI
import pandas as pd

import model
import serialization
import exception

# Inicializa os dataframes com séries vazias
df_alunos: pd.DataFrame = pd.DataFrame()
df_ucs: pd.DataFrame = pd.DataFrame()
df_professores: pd.DataFrame = pd.DataFrame()
df_notas: pd.DataFrame = pd.DataFrame()
df_completo: pd.DataFrame = pd.DataFrame()

def load_database():
    """
    Carrega a "base de dados" utilizada para o exemplo.
    Em uma aplicação real, os dados seriam persistidos em um SGBD (postgres, mysql, sqlite, etc...)
    """
    global df_alunos
    global df_notas
    global df_ucs
    global df_professores

    df_alunos = pd.read_json("data/alunos.json").set_index("matricula")
    df_notas = pd.read_json("data/notas.json").set_index("id")
    df_ucs = pd.read_json("data/ucs.json").set_index("id")
    df_professores = pd.read_json("data/professores.json").set_index("matricula")

    merge_data()


def merge_data():
    global df_completo
    # Left join garante que todas as notas apareçam, mesmo se faltar dados do aluno
    df_completo = df_notas.merge(
        df_alunos, left_on="aluno_matricula", right_on="matricula", how="left"
    )
    # Agora junta com as UCs
    df_completo = df_completo.merge(
        df_ucs, left_on="uc_id", right_on="id", suffixes=("_aluno", "_uc")
    )

    print(df_completo[["nome_aluno", "nome_uc", "nota"]])


def save_databases():
    df_alunos.to_json("data/alunos.json", orient="records", indent=4)
    df_ucs.to_json("data/ucs.json", orient="records", indent=4)
    df_professores.to_json("data/professores.json", orient="records", indent=4)
    df_notas.to_json("data/notas.json", orient="records", indent=4)


def busca_aluno(matricula: int) -> model.Aluno:
    try:
        # Matricula é chave do dataframe, portanto retorna 1 única linha ou exception
        aluno = df_alunos.loc[matricula]
        # Busco as notas associadas ao aluno
        notas = df_notas[df_notas["aluno_matricula"] == 2023001]
        # notas_aluno = busca no df_completo
        # Monta modelo com os dados do dataframe
        return serialization.series_to_aluno(aluno, notas)
    # ERRO de chave não encontrada do pandas. Transformo em um erro padrão no meu app
    except KeyError as e:
        raise exception.NotFound(f"Aluno com matrícula {matricula} não encontrado!")


def altera_aluno(matricula: int, dados: model.Aluno) -> model.Aluno:
    try:
        if matricula != dados.matricula:
            raise exception.InvalidOperation(
                f"Matrícula não corresponde aos dados informados!"
            )
        # Uso para validar que a matrícula já existe.
        # Caso não exista, gera exception e não faz modificação
        aluno = busca_aluno(matricula)
        nova_serie = pd.Series(asdict(dados))
        df_alunos.loc[matricula] = nova_serie
        #Persistência (na vida real, seria um UPDATE no banco de dados)
        save_databases()
        return dados
    except exception.NotFound:
        raise exception.NotFound(f"Aluno com matrícula {matricula} não encontrado!")


def cria_aluno(dados: model.Aluno) -> model.Aluno:
    # Outra forma de verificar se a matrícula existe no dataframe, sem gerar Exception
    # Se ainda não existe, posso criar o novo
    if dados.matricula not in df_alunos.index:
        nova_serie = pd.Series(asdict(dados))
        df_alunos.loc[dados.matricula] = nova_serie
        #Persistência (na vida real, seria um UPDATE no banco de dados)
        save_databases()
        return dados
    else:
        raise exception.InvalidOperation(f"O aluno {dados.matricula} já existe!")


def busca_notas_aluno(matricula: int) -> list[model.Nota]:
    aluno = busca_aluno(matricula)
    return aluno.notas
