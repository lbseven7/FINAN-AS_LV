import streamlit as st
import pandas as pd
import plotly.express as px
from database import conectar_banco, criar_tabelas, atualizar_valores
from receitas import gerenciar_receitas
from despesas import gerenciar_despesas, exibir_dados
from graficos import exibir_grafico_pizza

def main():
    st.set_page_config(page_title="Gerenciador de Orçamento", layout="wide")

    st.sidebar.title("📌 Menu de Navegação")
    opcao = st.sidebar.radio("Selecione uma opção:", 
                             ["Visão Geral", "Gerenciar Receitas", "Gerenciar Despesas", "📊 Gráfico de Pizza"])

    with conectar_banco() as conn:
        criar_tabelas(conn)
        atualizar_valores(conn)

        if opcao == "Visão Geral":
            st.title("📊 Visão Geral do Orçamento")
            st.subheader("Receitas Cadastradas")
            exibir_dados(conn, "receitas", ["ID", "Origem", "Valor", "Data", "Mês"])
            
            st.subheader("Despesas Cadastradas")
            exibir_dados(conn, "despesas", ["ID", "Categoria", "Valor", "Responsável", "Data", "Mês"])

        elif opcao == "Gerenciar Receitas":
            st.title("💰 Gerenciar Receitas")
            gerenciar_receitas(conn)

        elif opcao == "Gerenciar Despesas":
            st.title("📉 Gerenciar Despesas")
            gerenciar_despesas(conn)

        elif opcao == "📊 Gráfico de Pizza":
            exibir_grafico_pizza(conn)

if __name__ == "__main__":
    main()
