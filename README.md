
# Monitoramento dos Instrumentos de Planejamento e Gestão em Saúde no Maranhão

Este projeto consiste em um aplicativo web construído com Streamlit para monitorar o status dos Instrumentos de Planejamento e Gestão em Saúde no estado do Maranhão (MA).

A aplicação utiliza um processo ETL (Extração, Transformação e Carga) para unificar e limpar dados de diferentes fontes antes de exibi-los em um dashboard interativo.

**Estrutura do Projeto**

O projeto é composto por dois arquivos principais:

1.  **`etl.py`**: Contém a lógica de processamento dos dados (ETL).
2.  **`dashboard_final.py`**: Define a interface do usuário e a lógica de exibição do dashboard Streamlit.

A estrutura de diretórios esperada é a seguinte:

```
.
├── raw_data/
│   ├── extracao_2025-10-16 (1).csv  # Input File 1
│   └── extracao_2025-10-16.csv     # Input File 2
├── script/
│   └── dados_final.csv             # Output File (Gerado pelo ETL)
├── etl.py
└── dashboard_final.py
```

## 1\. Módulo ETL (`etl.py`)

Este módulo é responsável por unificar e transformar os dados brutos.

### 🔄 Pipeline de ETL (`run_pipeline`)

O pipeline executa as seguintes etapas:

1.  **Extração (`extract_data`)**: Lê dois arquivos CSV de entrada (`extracao_2025-10-16 (1).csv` e `extracao_2025-10-16.csv`) localizados no diretório `raw_data/`. Os arquivos são lidos com separador **`;`** e codificação **`utf-8-sig`**.
2.  **Unificação (`unify_data`)**: Concatena os DataFrames horizontalmente, mantendo a estrutura de colunas original para a fase de transformação.
3.  **Transformação (`transform`)**:
      * **Renomeação de Colunas**: Mapeia os nomes das colunas de origem para nomes padronizados, conforme o dicionário `SCHEMA_MAPPING`
      * **Adição de Colunas**: Adiciona a coluna `DATA_PROCESSAMENTO` com a data atual de execução do pipeline (`%Y-%m-%d`).
      * **Seleção Final**: Seleciona apenas as colunas renomeadas e a nova coluna de processamento.
4.  **Carga (`load_data`)**: Salva o DataFrame transformado no arquivo `script/dados_final.csv`, também utilizando o separador **`;`** e codificação **`utf-8-sig`**.

## 2\. Dashboard Streamlit (`dashboard_final.py`)

A aplicação Streamlit oferece uma interface para explorar os dados processados.

### 🚀 Funcionalidades Principais
  * **Carregamento de Dados (`load_prep_data`)**:
      * Verifica a existência do arquivo `script/dados_final.csv`.
      * Se o arquivo não existir, executa o pipeline ETL (`etl.py`) para gerá-lo.
  * **Última Atualização (`show_last_update`)**: Exibe na barra lateral a data de processamento mais recente (`DATA_PROCESSAMENTO`) encontrada nos dados.
  * **Seleção de Instrumentos**:
      * Apresenta seis botões de instrumentos no corpo principal da aplicação, sendo o selecionado realçado com a cor `primary`.
  * **Filtros na Barra Lateral (`create_filters`)**:
      * Disponibiliza filtros *multiselect* para refinar os dados por **Macrorregião** (`NO_MACROREGIONAL`), **Região** (`REGIAO`) e **Período/Ano**.
      * A coluna de filtro para o período é dinâmica: **`FASE`** para "Plano de Saúde" e **`ANO`** para os demais instrumentos.
  * **Visualização de Dados (`show_df`)**:
      * Filtra e exibe os dados detalhados em uma tabela interativa (`st.dataframe`) mostrando o total de registros encontrados.

### 📸 Visualização

Aqui está uma prévia do dashboard em execução:

<br> 
 <img width="1897" height="928" alt="image" src="https://github.com/user-attachments/assets/a6171086-3508-4302-9649-f229c23228e4" />
<br>


## Melhorias futuras

Abaixo estão as melhorias para aprimorar a usabilidade e a qualidade dos dados do projeto:

* **Normalizar o Campo 'ANO' (Exercício):** Implementar lógica na fase de `transform()` para padronizar os valores da coluna `ANO`. Isso inclui converter valores decimais (e.g., `2020.0`) para formato inteiro ou string (`2020`) e tratar registros com valores nulos (`nan`), seja preenchendo-os ou removendo-os, garantindo que o filtro de **Ano de Exercício** funcione de forma consistente.
* **Melhorar a Exibição de Macrorregiões:** O filtro de **Macrorregião** na barra lateral exibe nomes truncados (e.g., `MACRORREGIAO...`). No `dashboard_final.py`, é necessário ajustar os estilos CSS ou a forma de apresentação para garantir que o nome completo da macrorregião seja visível e legível.
* **Corrigir a Exibição da Data de Atualização:** A função `show_last_update` é chamada duas vezes dentro da função `main()` do `dashboard_final.py`. É preciso remover uma das chamadas para evitar a duplicação ou inconsistência da informação na barra lateral, garantindo que a data de atualização seja exibida de forma singular e correta.
