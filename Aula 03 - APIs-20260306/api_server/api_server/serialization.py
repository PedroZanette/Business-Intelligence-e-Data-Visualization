import pandas as pd
from dataclasses import asdict
import model  # Importa seus modelos originais

# ==========================================
# Métodos Genéricos (Opcional, mas útil)
# ==========================================
def to_series(obj) -> pd.Series:
    """
    Converte qualquer dataclass para uma pd.Series.
    Como 'asdict' é recursivo, ele já trata as listas aninhadas.
    """
    return pd.Series(asdict(obj))

def series_to_nota(series: pd.Series, matricula: int) -> model.Nota:
    data = series.to_dict()
    return model.Nota(
        nota=float(data.get('nota', 0.0)),
        id=str(data.get('id', '')),
        uc_id=int(data.get('uc', 0)),
        aluno_matricula=matricula
    )


def series_to_aluno(aluno: pd.Series, notas: pd.DataFrame) -> model.Aluno:
    '''
    Transforma as series em objeto Aluno. Separamos em 2 séries pois o objeto é hierárquico
    enquanto os dados no dataframe pandas são tabulares
    
    :param aluno: Series pandas com os dados do aluno
    :type aluno: pd.Series
    :param notas: Series contendo as notas do aluno
    :type notas: pd.Series
    :return: Description
    :rtype: Aluno
    '''
    aluno_dict = aluno.to_dict()
    matricula = aluno.name
    #Sintaxe de compreensão de listas (https://pythonacademy.com.br/blog/list-comprehensions-no-python)
    lista_notas = [series_to_nota(row, matricula) for index, row in notas.iterrows()]

    # Cada aluno tem N notas, portanto temos que tratar a lista
    return model.Aluno(
        matricula=int(matricula),
        nome=str(aluno_dict.get('nome', '')),
        notas=lista_notas
    )
