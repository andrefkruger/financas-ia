import os
import pandas as pd
from dotenv import load_dotenv
from google import genai
import time

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

df = pd.read_csv("transacoes.csv")
print(df)

def categorizar(descricao):
    prompt = f"""Categorize a transação financeira abaixo em UMA única palavra, escolhendo entre: 
Mercado, Transporte, Lazer, Assinatura, Moradia, Saude, Educacao, Salario, Outros.

Transação: {descricao}

Responda APENAS com a categoria, nada mais."""

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )
    time.sleep(13)
    return response.text.strip()

df["categoria"] = df["descricao"].apply(categorizar)
print(df)

df.to_csv("transacoes_categorizadas.csv", index=False)