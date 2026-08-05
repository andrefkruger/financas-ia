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