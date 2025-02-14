import streamlit as st
import pandas as pd
import plotly.express as px

def exibir_grafico_pizza(conn):
    st.title("📊 Distribuição de Receitas e Despesas")

    # 🔹 Carregar dados das tabelas
    df_receitas = pd.read_sql("SELECT origem, valor FROM receitas", conn)
    df_despesas = pd.read_sql("SELECT categoria, valor FROM despesas", conn)

    # 🔹 Criar gráfico de pizza para receitas
    if not df_receitas.empty:
        st.subheader("💰 Receitas por Origem")
        fig_receitas = px.pie(df_receitas, values="valor", names="origem", title="Receitas por Origem")
        st.plotly_chart(fig_receitas)

    # 🔹 Criar gráfico de pizza para despesas
    if not df_despesas.empty:
        st.subheader("📉 Despesas por Categoria")
        fig_despesas = px.pie(df_despesas, values="valor", names="categoria", title="Despesas por Categoria")
        st.plotly_chart(fig_despesas)