import pandas as pd
from typing import Dict, List, Optional



SCHEMA_MAPPING = {
    'TIPO_INSTRUMENTO': 'INSTRUMENTO',
    'MACRORREGIAO': 'MACRORREGIAO',
    'REGIAO': 'REGIAO',
    'MUNICIPIO': 'MUNICIPIO',
    'SITUACAO': 'STATUS',
    'FASE': 'FASE',
    'EXERCICIO': 'ANO',
    }

COLUNAS_NOVAS = [
    ('DATA_PROCESSAMENTO', pd.to_datetime('today').strftime('%Y-%m-%d'))
]
def extract_data(file_path1):
    try:
        df = pd.read_csv(file_path1, sep = ';', encoding='utf-8-sig')
        print(f"Colunas de df1 após extração: {df.columns.tolist()}")
        return df
    except Exception as e:
        print(f"Erro na extração: {e}")
        return None, None
    

"""Limpeza dos dados"""
def transform(df: pd.DataFrame, col_mapping: Dict[str, str], new_cols: Optional[List[tuple]] ) -> pd.DataFrame:
    if df is None:
        return None
    
    # Renomeação das colunas
    df_transformed = df.rename(columns=col_mapping)
    df_transformed['ANO'] = df_transformed['ANO'].astype(str)
    df_transformed['ANO'] = df_transformed['ANO'].str.replace(r'\.0$', '', regex=True)
    df_transformed['ANO'] = df_transformed['ANO'].replace('nan', '')
    
    if new_cols:
        for col_name, default_value in new_cols:
            if col_name not in df_transformed.columns:
                df_transformed[col_name] = default_value
                print(f"Adicionada coluna '{col_name}' com valor padrão/mapeado.")


    final_columns = list(col_mapping.values())


    if new_cols:
        new_names = [name for name, _ in new_cols]
        # Adiciona novas colunas que foram criadas
        final_columns.extend([n for n in new_names if n not in final_columns])
    
    df_final = df_transformed[final_columns]
    
    print(df_transformed.columns)
    return df_final


def load_data(df, output_path):

    if df is None:
        return
    df.to_csv(output_path, sep=';', index=False, encoding='utf-8-sig')

def run_pipeline(file_path, output_file):
    print("Iniciando pipeline ETL")

    #Extração
    df = extract_data(file_path)

    #Transformação
    df_transformed = transform(df=df, col_mapping=SCHEMA_MAPPING, new_cols=COLUNAS_NOVAS)

    #Gerando Arquivo
    load_data(df_transformed, output_file)

    print("Pipeline ETL Concluído")

    return output_file
