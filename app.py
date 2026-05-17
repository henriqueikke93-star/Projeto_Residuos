import streamlit as st
import pandas as pd
import glob
import os

st.set_page_config(page_title="Painel de Resíduos Municipais", layout="wide")

st.title("📊 Diagnóstico de Resíduos Sólidos Municipais")
st.markdown("Dados processados via **Apache Spark** dentro do cluster **Kubernetes (Kind)**.")

# 1. Encontrar o arquivo gerado pelo Spark na pasta local
# (Mais para frente vamos rodar o app mapeando essa pasta do K8s)
pasta_dados = "/dados/resultado_processado"
arquivos_csv = glob.glob(os.path.join(pasta_dados, "part-*.csv"))

if not arquivos_csv:
    st.error(f"Nenhum arquivo de resultado encontrado em {pasta_dados}. Verifique se o Spark rodou com sucesso.")
else:
    # Carrega o CSV leve
    @st.cache_data
    def carregar_dados(caminho):
        return pd.read_csv(caminho)
    
    df = carregar_dados(arquivos_csv[0])

    # 2. Criando os Filtros na Barra Lateral
    st.sidebar.header("Filtros de Pesquisa")
    
    # Filtro de Estado (UF)
    lista_ufs = sorted(df['uf'].dropna().unique())
    uf_selecionada = st.sidebar.selectbox("Selecione o Estado (UF):", lista_ufs)

    # Filtro de Município (Muda dinamicamente baseado na UF escolhida)
    df_uf = df[df['uf'] == uf_selecionada]
    lista_municipios = sorted(df_uf['municipio'].dropna().unique())
    municipio_selecionado = st.sidebar.selectbox("Selecione o Município:", lista_municipios)

    # Filtrando os dados finais para a tela
    dados_finais = df_uf[df_uf['municipio'] == municipio_selecionado]

    # 3. Exibindo os Resultados na Tela
    st.subheader(f"📍 Análise de: {municipio_selecionado} - {uf_selecionada}")

    if dados_finais.empty or dados_finais['total_toneladas'].sum() == 0:
        st.warning("Não há dados de massa (toneladas) registrados para este município neste diagnóstico.")
    else:
        # Criando métricas no topo
        total_lixo = dados_finais['total_toneladas'].sum()
        st.metric(label="Total de Massa Declarada", value=f"{total_lixo:,.2f} TON")

        # Exibindo o Gráfico de Barras do próprio Streamlit
        st.write("### Massa por Categoria de Resíduo")
        
        # Ajustando os dados para o formato que o gráfico do Streamlit espera
        dados_grafico = dados_finais.set_index('categoria')['total_toneladas']
        st.bar_chart(dados_grafico)

        # Se o usuário quiser ver a tabela bruta
        with st.expander("👁️ Ver tabela de dados brutos deste município"):
            st.dataframe(dados_finais)