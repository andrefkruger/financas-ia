import streamlit as st
import pandas as pd

st.title("💰 Dashboard de Finanças")

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