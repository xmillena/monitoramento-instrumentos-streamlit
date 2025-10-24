

# Monitoramento dos Instrumentos de Planejamento e Gestão em Saúde no Maranhão 

Este projeto utiliza Python e a biblioteca **Streamlit** para criar um dashboard interativo. Seu objetivo é monitorar o status dos Instrumentos de Planejamento e Gestão em Saúde no Maranhão, aplicando um processo de ETL (Extração, Transformação e Carga) antes da visualização.

## Estrutura e Tecnologia

O projeto está dividido em dois módulos principais:

  * **`etl.py`**: Responsável por unificar os dados de duas fontes (`extracao_2025-10-16 (1).csv` e `extracao_2025-10-16.csv`), renomear colunas (`UF` para `ESTADO`, `EXERCICIO` para `ANO`), e normalizar campos como a coluna `ANO`. O resultado é salvo em `script/dados_final.csv`.
  * **`dashboard_final.py`**: O aplicativo Streamlit que carrega os dados processados e oferece a interface do usuário.

## Funcionalidades do Dashboard

O dashboard oferece as seguintes funcionalidades principais:

  * **Carregamento Inteligente:** O pipeline ETL é executado automaticamente (`run_pipeline`) se o arquivo final processado (`dados_final.csv`) não for encontrado.
  * **Seleção de Instrumentos:** Botões interativos permitem alternar rapidamente a visualização entre seis instrumentos de gestão, como "Plano de Saúde" e "Programação Anual de Saúde".
  * **Filtros Otimizados:** Todos os filtros estão localizados na barra lateral (`st.sidebar`) para melhor experiência em mobile e organização:
      * **Seleção Única:** O filtro de **Município** e **Período** utiliza `st.selectbox` para seleção única para economizar espaço e evitar a longa lista de *chips*.
  * **Data de Atualização:** A data da última atualização dos dados é exibida na barra lateral.

## Visualização

Aqui está uma prévia do dashboard em execução:

<br>
<img width="1897" height="773" alt="image" src="https://github.com/user-attachments/assets/33dbcd70-b7de-4810-b6ac-d9dac0b7428f" />
<br>
