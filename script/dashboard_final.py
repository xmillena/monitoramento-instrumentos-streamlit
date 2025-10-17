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
        df['ANO'] = df['ANO'].astype(str)

        return df
    
    except Exception as e: 
        st.error(f'Erro ao ler arquivo CSV: {e}')
        return pd.DataFrame()         

def show_last_update(df):

    """Mostra a data da última atualização do dado (DATA_PROCESSAMENTO)."""

    if 'DATA_PROCESSAMENTO' in df.columns and not df.empty:

        ultima_data = df['DATA_PROCESSAMENTO'].max()

        st.sidebar.markdown("---")

        st.sidebar.info(f"**Última Atualização dos Dados:**\n\n{ultima_data}")

    else:

        st.sidebar.info("Dados de atualização não disponíveis.")                 

def create_filters(df):
    st.sidebar.header("Filtros da Análise")

    instrumento_selecionado = st.session_state.get('instrumento_selecionado', "Plano de Saúde")

    if instrumento_selecionado == "Plano de Saúde":
        periodo_coluna = 'FASE'
        periodo_label = "Fase/Período:"
    else:
        periodo_coluna = 'ANO'
        periodo_label = "Ano de Exercício:"
    
    macro_list = sorted(df['NO_MACROREGIONAL'].unique().tolist())
    macro_filtro = st.sidebar.multiselect('Macrorregião', macro_list, default=macro_list )

    regiao_list = sorted(df['REGIAO'].unique().tolist())
    regiao_filtro = st.sidebar.multiselect('Região', regiao_list, default=regiao_list)
    
    periodo_list = sorted(df[periodo_coluna].unique().tolist())
    periodo_filtro = st.sidebar.multiselect(periodo_label, periodo_list, default=periodo_list)

    
    df_filtrado = df[(df[periodo_coluna].isin(periodo_filtro)) &
                     (df['REGIAO'].isin(regiao_filtro)) &
                     (df['NO_MACROREGIONAL'].isin(macro_filtro))].copy()

    return df_filtrado

def show_df(df_filtrado):
    instrumento_selecionado = st.session_state.get('instrumento_selecionado', "Plano de Saúde")
    st.subheader(f"Status do Instrumento: {instrumento_selecionado}")
    cols = st.columns(6)

    for i, (nome, tipo) in enumerate(INSTRUMENTOS.items()):
        # Para que o botão ative a cor 'primary' se ele for o selecionado
        current_type = "primary" if nome == instrumento_selecionado else "secondary"
        
        if cols[i].button(nome, type=current_type, use_container_width=True):
            st.session_state['instrumento_selecionado'] = nome
            # O Streamlit recarrega o script aqui, e a cor do botão selecionado será atualizada.


    #Tabela Detalhada para o Instrumento Selecionado
    st.markdown("---")
    st.subheader(f"Dados Detalhados: {instrumento_selecionado}")
    
    # Filtra o DataFrame apenas para o instrumento selecionado
    df_instrumento = df_filtrado[df_filtrado['INSTRUMENTO'] == instrumento_selecionado]
    
    if df_instrumento.empty:
        st.info(f"Nenhum registro encontrado para '{instrumento_selecionado}' com os filtros aplicados.")
        return
        
    st.write(f"Total de registros encontrados (aplicando filtros): **{len(df_instrumento)}**")

    # Exibe a tabela interativa
    st.dataframe(df_instrumento, use_container_width=True, height=700)

     
def main():
    st.markdown(
    """
    <style>
        /* Aumenta a largura da barra lateral */
        [data-testid="stSidebar"] {
            width: 400px !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            width: 400px !important;
        }
        st.markdown(

        /* Oculta o campo de entrada (input) para evitar digitação */
        [data-testid="stMultiSelect"] input {
            pointer-events: none !important;
            user-select: none !important;
            color: transparent !important;
            background-color: transparent !important;
        }
        /* Mantendo os estilos para a largura da sidebar e dos chips */
        [data-testid="stSidebar"] { width: 400px !important; }
        [data-testid="stSidebar"] > div { width: 400px !important; }
        [data-testid="stMultiSelect"] { width: 380px !important; }
        [data-testid="stMultiSelect"] .st-bh { 
            width: 100% !important; 
            max-width: 380px !important; 
            white-space: normal; 
            height: auto; 
            padding-top: 5px; 
            padding-bottom: 5px;
        }
        
    </style>
    """,
    unsafe_allow_html=True
)

    st.set_page_config(
    page_title="Monitoramento de Instrumentos",
    layout="wide",
    initial_sidebar_state="expanded")

    st.title(" Monitoramento dos Instrumentos de Planejamento e Gestão em Saúde no Maranhão 📈")
    st.markdown("---")

    df_dados = load_prep_data()
    if df_dados.empty:
        st.warning("Não há dados válidos para exibição.")
        return
    
    df_dados = load_prep_data()
    if df_dados.empty:
        st.warning("Não há dados válidos para exibição.")
        return

    show_last_update(df_dados)
    
    # Inicializa o estado da sessão (necessário para os botões)
    if 'instrumento_selecionado' not in st.session_state:
        st.session_state['instrumento_selecionado'] = "Plano de Saúde"
        
    df_dados = load_prep_data()
    if df_dados.empty:
        st.warning("Não há dados válidos para exibição.")
        return
    
    df_filtrado = create_filters(df_dados)
    
    # Chama a função que exibe apenas a tabela
    show_df(df_filtrado)

if __name__ == "__main__":

    main()


