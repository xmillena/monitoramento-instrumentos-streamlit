import pandas as pd
from typing import Dict, List, Optional
import os
#pesquisar sobre os 


SCHEMA_MAPPING = {
    'UF': 'ESTADO',
    'TIPO_INSTRUMENTO': 'INSTRUMENTO',
    'MACRORREGIAO': 'NO_MACROREGIONAL',
    'REGIAO': 'REGIAO',
    'MUNICIPIO': 'MUNICIPIO',
    'SITUACAO': 'STATUS',
    'FASE': 'FASE',
    'EXERCICIO': 'ANO',
    }

COLUNAS_NOVAS = [
    ('DATA_PROCESSAMENTO', pd.to_datetime('today').strftime('%Y-%m-%d'))
]
def extract_data(file_path1, file_path2):
    try:
        df1 = pd.read_csv(file_path1, sep = ';', encoding='utf-8-sig')
        df2 = pd.read_csv(file_path2, sep = ';', encoding='utf-8-sig')
        print(f"Colunas de df1 após extração: {df1.columns.tolist()}")
        return df1, df2
    except Exception as e:
        print(f"Erro na extração: {e}")
        return None, None
    
        

def unify_data(df_list):
    """Unifica horizontalmente dos dados em EXERCÍCIO, FASE, SITUAÇÃO"""
    df_concat= pd.concat(df_list, ignore_index=True)
    return df_concat

"""Limpeza dos dados"""
def transform(df: pd.DataFrame, col_mapping: Dict[str, str], new_cols: Optional[List[tuple]] = None) -> pd.DataFrame:
    if df is None:
        return None
    
    # Renomeação das colunas
    df_transformed = df.rename(columns=col_mapping)

    # Adicionar novas colunas com valor padrao
    if new_cols:
        for col_name, default_value in new_cols:
            if col_name not in df_transformed.columns:
                df_transformed[col_name] = default_value
                print(f"Adicionada coluna '{col_name}' com valor padrão/mapeado.")


    final_columns = list(col_mapping.values())
    valid_final_columns = [col for col in final_columns if col in df_transformed.columns]

    if new_cols:
        new_names = [name for name, _ in new_cols]
        # Adiciona novas colunas que foram criadas, garantindo que não estejam duplicadas
        final_columns.extend([n for n in new_names if n not in final_columns])
    
    df_final = df_transformed[valid_final_columns]
    
    print("Transformação de esquema genérica concluída.")
    print(df_transformed.columns)
    return df_final


def load_data(df, output_path):

    if df is None:
        return
    df.to_csv(output_path, sep=';', index=False, encoding='utf-8-sig')

def run_pipeline(file_path1, file_path2, output_file):
    print("Iniciando pipeline ETL")

    #Extração
    df1, df2 = extract_data(file_path1, file_path2)

    #Transformação
    df_unified = unify_data([df1, df2])
    df_transformed = transform(df=df_unified, col_mapping=SCHEMA_MAPPING, new_cols=COLUNAS_NOVAS)

    #Gerando Arquivo
    load_data(df_transformed, output_file)

    print("Pipeline ETL Concluído")

    return output_file

