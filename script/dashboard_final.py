import streamlit as st
import pandas as pd
from etl import run_pipeline 
import os


# Configuração de saída


OUTPUT_DIR = 'script'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'dados_final.csv')

# Configuração da fonte (input)
RAW_DATA_DIR = 'raw_data'
INPUT_FILE = os.path.join(RAW_DATA_DIR, 'extracao_2025-10-31.csv')


# Definição dos instrumentos

@st.cache_data
def load_prep_data():
    # Carrega o CSV final
    if not os.path.exists(OUTPUT_FILE):
        # Se o arquivo não existe, roda o ETL antes de tentar carregar
        with st.spinner("Carregando arquivos..."):
            try:
                run_pipeline(INPUT_FILE, OUTPUT_FILE)
            except Exception as e:
                st.error(f'Falha no carregamento: {e}')
                return pd.DataFrame() # Retorna um dataframe vazio se a execução falhar
            
            
    try:
        df = pd.read_csv(OUTPUT_FILE, sep=';', encoding='utf-8-sig')
        return df
    
    except Exception as e: 
        st.error(f'Erro ao ler arquivo CSV: {e}')
        return pd.DataFrame()         

def create_filters(df):

    municipio_list = ['SAO LUIS'] + sorted(df['MUNICIPIO'].dropna().unique().tolist())
    municipio_selecionado = st.sidebar.selectbox('Município', municipio_list)

    periodo_list = sorted(df['FASE'].dropna().unique().tolist())
    periodo_selecionado = st.sidebar.selectbox('Período', periodo_list)

    if municipio_selecionado != 'Todos':
        df = df[df['MUNICIPIO'] == municipio_selecionado].copy()
    
    if periodo_selecionado:
        df = df[df['FASE'] == periodo_selecionado].copy()
    
    st.subheader(f"Resultado para {municipio_selecionado} - Período {periodo_selecionado}")
    st.markdown("---")

    return df



def show_df(df):
    col_header_inst, col_header_periodo, col_header_status = st.columns([1, 1, 1])
    col_header_inst.markdown("**INSTRUMENTO**")
    col_header_periodo.markdown("**ANO**")
    col_header_status.markdown("**STATUS**")

    plano_saude = df[df['INSTRUMENTO'] == 'Plano de Saúde']
    
    if not plano_saude.empty:
        plano_status = plano_saude.iloc[0]['STATUS']
        plano_periodo = plano_saude.iloc[0]['FASE']

        col_inst, col_ano, col_status = st.columns([1, 1, 1])
        col_inst.markdown(f"**Plano de Saúde**")
        col_ano.markdown(plano_periodo)
        col_status.markdown(f"{plano_status}")
    
    st.markdown("---")

    df_sem_plano = df[df['INSTRUMENTO'] != 'Plano de Saúde'].copy()


    
    # Converter ANO para inteiro
    df_sem_plano['ANO'] = df_sem_plano['ANO'].astype(float).astype(int)
    
    anos = sorted(df_sem_plano['ANO'].unique())
    
    for idx, ano in enumerate(anos):
        df_ano = df_sem_plano[df_sem_plano['ANO']==ano].sort_values(by=['INSTRUMENTO'])
       
        for i, row in df_ano.iterrows():
            instrumento_nome = row['INSTRUMENTO']
            instrumento_status = row['STATUS']
            instrumento_ano = row['ANO'] 
            
            col_inst, col_ano, col_status = st.columns([1, 1, 1])
            
            
            col_inst.markdown(f"**{instrumento_nome}**")
            col_ano.markdown(f"{instrumento_ano}")
            col_status.markdown(f"{instrumento_status}")
        
        
        if idx < len(anos) - 1:
            st.markdown("---")

        



def main():
    
    df_dados = load_prep_data()
    if df_dados.empty:
        st.warning("Não há dados válidos para exibição.")
        return

    st.set_page_config(
    page_title="Monitoramento de Instrumentos",
    layout="wide",
    initial_sidebar_state="expanded")

    st.title(" Monitoramento dos Instrumentos de Planejamento e Gestão em Saúde no Maranhão 📈")

    if 'DATA_PROCESSAMENTO' in df_dados.columns and not df_dados.empty:
        data_atualizacao = pd.to_datetime(df_dados['DATA_PROCESSAMENTO'], errors='coerce').max()
        data_atualizacao = data_atualizacao.strftime("%d/%m/%Y")
        st.sidebar.info(f"**📅 Última atualização da planilha:** {data_atualizacao}")
 
    
    df_filtrado = create_filters(df_dados)

    show_df(df_filtrado)


if __name__ == "__main__":

    main()


