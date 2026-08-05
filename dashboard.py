import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from google import genai
import time

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def categorizar(descricao):
    prompt = f"""Categorize a transação financeira abaixo em UMA única palavra, escolhendo entre: 
Mercado, Transporte, Lazer, Assinatura, Moradia, Saude, Educacao, Salario, Outros.

Transação: {descricao}

Responda APENAS com a categoria, nada mais."""

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )
    time.sleep(5)
    return response.text.strip()


st.title("💰 Dashboard de Finanças")

st.subheader("📤 Envie seu próprio CSV (opcional)")
st.caption("Colunas necessárias: data, descricao, valor. Limite de 20 linhas nesta demo.")

arquivo = st.file_uploader("Escolha um arquivo CSV", type="csv")

if arquivo is not None:
     df_novo = pd.read_csv(arquivo)
     if len(df_novo) > 20:
        st.error("Arquivo muito grande para esta demo (máximo 20 linhas). Usando dados de exemplo.")
        df = pd.read_csv("transacoes_categorizadas.csv")
     else:
        if "categoria" not in df_novo.columns:
            barra = st.progress(0, text="Categorizando transações com IA...")
            categorias = []
            total = len(df_novo)
            for i, descricao in enumerate(df_novo["descricao"]):
                categorias.append(categorizar(descricao))
                barra.progress((i + 1) / total, text=f"Categorizando... ({i + 1}/{total})")
            df_novo["categoria"] = categorias
            barra.empty()
        df = df_novo
else:
    df = pd.read_csv("transacoes_categorizadas.csv")

st.subheader("Transações")
st.dataframe(df)

gastos = df[df["valor"] < 0].copy()
gastos["valor"] = gastos["valor"].abs()

por_categoria = gastos.groupby("categoria")["valor"].sum().sort_values(ascending=False)

st.subheader("Gastos por categoria")
st.bar_chart(por_categoria)

total_gasto = gastos["valor"].sum()
st.metric("Total gasto no período", f"R$ {total_gasto:,.2f}")

media_por_categoria = gastos.groupby("categoria")["valor"].transform("mean")
desvio_por_categoria = gastos.groupby("categoria")["valor"].transform("std")

gastos["anomalia"] = gastos["valor"] > (media_por_categoria + 1.5 * desvio_por_categoria)

anomalias = gastos[gastos["anomalia"]]

st.subheader("⚠️ Gastos fora do padrão")

if len(anomalias) > 0:
    st.dataframe(anomalias[["data", "descricao", "valor", "categoria"]])
else:
    st.write("Nenhuma anomalia detectada nos gastos.")