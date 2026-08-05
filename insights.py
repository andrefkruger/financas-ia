import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("transacoes_categorizadas.csv")

gastos = df[df["valor"] < 0].copy()
gastos["valor"] = gastos["valor"].abs()

print(gastos)

por_categoria = gastos.groupby("categoria")["valor"].sum().sort_values(ascending=False)

print("\nGastos por categoria:")
print(por_categoria.to_string())

total_gasto = gastos["valor"].sum()
percentual = (por_categoria / total_gasto * 100).round(1)

print("\nPercentual por categoria:")
print(percentual.to_string())

por_categoria.plot(kind="bar", color="steelblue")
plt.title("Gastos por categoria")
plt.ylabel("Valor (R$)")
plt.xlabel("")
plt.tight_layout()
plt.savefig("grafico_gastos.png")
plt.show()