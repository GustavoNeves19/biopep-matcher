import streamlit as st
import pandas as pd

# Carrega os dados
@st.cache_data
def carregar_dados(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo)
    df['Monois. mass'] = pd.to_numeric(df['Monois. mass'], errors='coerce')
    return df.dropna(inplace=True)

# Calcula os matches
def encontrar_candidatas(df, mz_origem, tolerancia=1.0):
    df = df.copy()
    df['Delta'] = (df['Monois. mass'] - mz_origem).abs()
    df_filtrado = df[df['Delta'] <= tolerancia].sort_values(by='Delta')
    return df_filtrado

# Interface Streamlit
st.set_page_config(page_title="BIOPEP Matcher", layout="centered")
st.title("🔬 BIOPEP Matcher")
st.write("Insira um valor de **m/z** para encontrar possíveis moléculas candidatas.")

# Entrada do usuário
mz_input = st.number_input("Digite o valor m/z:", min_value=100.0, max_value=5000.0, step=0.1)

# Carregamento dos dados
df_biopep = carregar_dados("./data/biopep_corrigido.xlsx")

# Quando o botão for clicado
if st.button("Buscar candidatas"):
    if mz_input:
        resultado = encontrar_candidatas(df_biopep, mz_input)

        st.subheader(f"🔎 {len(resultado)} candidatas encontradas para m/z = {mz_input}")
        st.dataframe(resultado.reset_index(drop=True), use_container_width=True)
        
        # Download opcional
        csv = resultado.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar resultados (.csv)", csv, "candidatas_mz.csv", "text/csv")
    else:
        st.warning("Por favor, insira um valor de m/z.")
