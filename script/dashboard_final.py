import streamlit as st
import pandas as pd
from etl import run_pipeline 
import os


# Configuração de saída

OUTPUT_DIR = 'script'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'dados_final.csv')

# Configuração da fonte (input)
RAW_DATA_DIR = 'raw_data'
INPUT_FILE1 = os.path.join(RAW_DATA_DIR, 'extracao_2025-10-16 (1).csv')
INPUT_FILE2 = os.path.join(RAW_DATA_DIR, 'extracao_2025-10-16.csv')


# Definição dos instrumentos
INSTRUMENTOS = {
    "Plano de Saúde": "primary", 
    "Programação Anual de Saúde": "secondary", 
    "1º RDQA": "secondary", 
    "2º RDQA": "secondary",
    "3º RDQA": "secondary",
    "RAG": "secondary"
}

@st.cache_data
def load_prep_data():
    """Carregando os dados"""
    # Carrega o CSV final
    if not os.path.exists(OUTPUT_FILE):
        # Se o arquivo não existe, roda o ETL antes de tentar carregar
        with st.spinner("Carregando arquivos..."):
            try:
                run_pipeline(INPUT_FILE1, INPUT_FILE2, OUTPUT_FILE)
            except Exception as e:
                st.error(f'Falha no carregamento: {e}')
                return pd.DataFrame() # Retorna um dataframe vazio se a execução falhar
            
            
    try:
        df = pd.read_csv(OUTPUT_FILE, sep=';', encoding='utf-8-sig')
        #df['ANO'] = df['ANO'].astype(str)

        return df
    
    except Exception as e: 
        st.error(f'Erro ao ler arquivo CSV: {e}')
        return pd.DataFrame()         


def show_df(df):
    instrumento_selecionado = st.session_state.get('instrumento_selecionado', "Plano de Saúde")
    st.subheader(f"Status do Instrumento: {instrumento_selecionado}")
    cols = st.columns(6)

    for i, (nome, tipo) in enumerate(INSTRUMENTOS.items()):
        current_type = "primary" if nome == instrumento_selecionado else "secondary"
        
        if cols[i].button(nome, type=current_type, use_container_width=True):
            st.session_state['instrumento_selecionado'] = nome
            st.rerun()


    #Tabela Detalhada para o Instrumento Selecionado
    st.markdown("---")
    st.subheader(f"Dados Detalhados: {instrumento_selecionado}")
    
    # Filtra o DataFrame apenas para o instrumento selecionado
    df_instrumento = df[df['INSTRUMENTO'] == instrumento_selecionado].copy()
    
    if df_instrumento.empty:
        st.info(f"Nenhum registro encontrado para '{instrumento_selecionado}' com os filtros aplicados.")
        return
    
    if instrumento_selecionado == "Plano de Saúde" and "ANO" in df_instrumento.columns:
        df_instrumento = df_instrumento.drop(columns=["ANO"])

    df_instrumento= df_instrumento.drop(columns = ["DATA_PROCESSAMENTO"])
    st.dataframe(df_instrumento, use_container_width=True,height=700,)

     
def main():
    
    df_dados = load_prep_data()
    if df_dados.empty:
        st.warning("Não há dados válidos para exibição.")
        return
    st.markdown(
    """
    <style>
        [data-testid="stMultiSelect"] {
            width: 100% !important;
        }

        /* container dos chips */
        [data-testid="stMultiSelect"] .st-bh {
            flex-wrap: wrap !important;
            row-gap: 4px !important;
        }

        /* chip individual */
        [data-testid="stMultiSelect"] .st-bh .st-bu {
            display: flex !important;
            align-items: center !important;
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
            max-width: none !important;
            height: auto !important;
            min-width: fit-content !important;
        }

        /* texto dentro do chip */
        [data-testid="stMultiSelect"] .st-bh .st-bu div {
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
            max-width: none !important;
            line-height: 1.2 !important;
        }

        /* botão de remover (x) */
        [data-testid="stMultiSelect"] .st-bh .st-bu button {
            flex-shrink: 0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
    lista_municipios = sorted(df_dados['MUNICIPIO'].dropna().unique().tolist())
    
    municipios_selecionados = st.sidebar.multiselect(
    "Selecione o(s) município(s):",
    options=lista_municipios,
    default=lista_municipios
)
    
    df_filtrado = df_dados[df_dados['MUNICIPIO'].isin(municipios_selecionados)]

    st.set_page_config(
    page_title="Monitoramento de Instrumentos",
    layout="wide",
    initial_sidebar_state="expanded")

    st.title(" Monitoramento dos Instrumentos de Planejamento e Gestão em Saúde no Maranhão 📈")
    st.markdown("---")
    
    # Inicializa o estado da sessão (necessário para os botões)
    if 'instrumento_selecionado' not in st.session_state:
        st.session_state['instrumento_selecionado'] = "Plano de Saúde"

    if 'DATA_PROCESSAMENTO' in df_dados.columns and not df_dados.empty:
        data_atualizacao = pd.to_datetime(df_dados['DATA_PROCESSAMENTO'], errors='coerce').max()
        data_atualizacao = data_atualizacao.strftime("%d/%m/%Y")
        st.info(f"**📅 Última atualização da planilha:** {data_atualizacao}")
        
    df_dados = load_prep_data()
    if df_dados.empty:
        st.warning("Não há dados válidos para exibição.")
        return
    
    show_df(df_filtrado)


if __name__ == "__main__":

    main()


