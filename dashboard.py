import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from google import genai
import time

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if "transacoes_manuais" not in st.session_state:
    st.session_state.transacoes_manuais = pd.DataFrame(columns=["data", "descricao", "valor", "categoria"])


def categorizar(descricao):
    prompt = f"""Categorize a transação financeira abaixo em UMA única palavra, escolhendo entre: 
Mercado, Transporte, Lazer, Assinatura, Moradia, Saude, Educacao, Salario, Transferencia, Compras, Outros.

Regras importantes:
- PIX ou transferência enviada/recebida entre pessoas = Transferencia
- Compras em lojas de variedades, roupas ou eletrônicos = Compras
- Supermercado, padaria, açougue = Mercado
- Fatura de cartão de crédito = Outros

Exemplos:
"PIX recebido - Mariana Alves" -> Transferencia
"Loja Havan" -> Compras
"Supermercado Angeloni" -> Mercado
"Uber" -> Transporte

Transação: {descricao}

Responda APENAS com a categoria, nada mais."""

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )
    time.sleep(5)
    return response.text.strip()


st.title("💰 Dashboard de Finanças")

st.subheader("➕ Adicionar transação manualmente")

with st.form("nova_transacao"):
    data_input = st.date_input("Data")
    descricao_input = st.text_input("Descrição")
    valor_input = st.number_input("Valor (negativo para gasto, positivo para receita)", step=0.01)
    enviar = st.form_submit_button("Adicionar")

if enviar and descricao_input:
    with st.spinner("Categorizando..."):
        categoria_nova = categorizar(descricao_input)
        
    nova_linha = pd.DataFrame([{
        "data": data_input.strftime("%Y-%m-%d"),
        "descricao": descricao_input,
        "valor": valor_input,
        "categoria": categoria_nova
    }])
    
    st.session_state.transacoes_manuais = pd.concat([st.session_state.transacoes_manuais, nova_linha], ignore_index=True)
    st.success(f"Transação adicionada! Categoria: {categoria_nova}")
    
comecar_do_zero = st.checkbox("Começar do zero (sem os dados de exemplo)", key="comecar_do_zero")
    
if len(st.session_state.transacoes_manuais) > 0:
    st.caption(f"{len(st.session_state.transacoes_manuais)} transação(ões) adicionada(s) nesta sessão")

    opcoes = [
        f"{i}: {row['descricao']} (R$ {row['valor']})"
        for i, row in st.session_state.transacoes_manuais.iterrows()
    ]
    item_selecionado = st.selectbox("Selecione um item para remover", opcoes)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Remover item selecionado"):
            indice = int(item_selecionado.split(":")[0])
            st.session_state.transacoes_manuais = st.session_state.transacoes_manuais.drop(index=indice).reset_index(drop=True)
            st.rerun()
    with col2:
        if st.button("🗑️ Limpar todas"):
            st.session_state.transacoes_manuais = pd.DataFrame(columns=["data", "descricao", "valor", "categoria"])
            st.rerun()



st.subheader("📤 Envie seu próprio CSV (opcional)")
st.caption("Colunas necessárias: data, descricao, valor. Limite de 20 linhas nesta demo.")

arquivo = st.file_uploader("Escolha um arquivo CSV", type="csv")

if arquivo is not None:
     df_novo = pd.read_csv(arquivo)
     if len(df_novo) > 20:
        st.error("Arquivo muito grande para esta demo (máximo 20 linhas). Usando dados de exemplo.")
        if comecar_do_zero:
            df = pd.DataFrame(columns=["data", "descricao", "valor", "categoria"])
        else:
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
    if comecar_do_zero:
        df = pd.DataFrame(columns=["data", "descricao", "valor", "categoria"])
    else:
        df = pd.read_csv("transacoes_categorizadas.csv")
if len(st.session_state.transacoes_manuais) > 0:
    df = pd.concat([df, st.session_state.transacoes_manuais], ignore_index=True)

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