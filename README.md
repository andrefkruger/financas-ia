# 💰 Dashboard de Automação Financeira com IA

Projeto que automatiza a categorização de transações financeiras usando um modelo de IA (Google Gemini) e apresenta os resultados em um dashboard interativo.

🔗 **[Acesse o dashboard ao vivo](https://financas-ia-7jtyutgxhvbi9mc2adnzda.streamlit.app)**

## 🛠️ Tecnologias

- Python
- Google Gemini API (categorização via IA)
- Pandas (análise de dados)
- Streamlit (dashboard interativo)
- Matplotlib (visualização de dados)

## ⚙️ Funcionalidades

- Leitura automática de transações a partir de um CSV
- Categorização das transações usando IA generativa
- Cálculo de gastos totais e percentuais por categoria
- Dashboard interativo com gráficos e métricas
- Detecção de gastos fora do padrão (anomalias) por categoria
- Upload de CSV próprio com categorização em tempo real (limitado a 20 linhas na demo pública)
- Prompt refinado com regras e exemplos (few-shot) para maior precisão na categorização
- Cadastro e remoção manual de transações, com opção de começar do zero (sem dados de exemplo)

## 🚀 Como rodar localmente

```bash
git clone https://github.com/andrefkruger/financas-ia.git
cd financas-ia
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto com sua chave da API do Gemini:

```
GEMINI_API_KEY=sua_chave_aqui
```

Depois rode:

```bash
streamlit run dashboard.py
```

## 📚 Aprendizados

Esse foi meu primeiro projeto integrando uma API de IA generativa a um pipeline de dados real, desde a leitura dos dados brutos até um dashboard publicado em produção.

## 🔮 Próximos passos

- Comparar performance entre categorização por IA e por modelo de ML treinado