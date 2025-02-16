import streamlit as st
import pandas as pd
import sqlite3
import os

# Função para manter a conexão única com o banco de dados
@st.cache_resource
def get_connection():
    DB_PATH = os.path.join(os.path.dirname(__file__), "orcamento.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)

conn = get_connection()

def gerenciar_receitas(conn):
    st.header("📥 Editar ou Cadastrar uma Receita")
    cursor = conn.cursor()
    
    # Buscar receitas do banco
    cursor.execute("SELECT id, origem, valor, data, strftime('%m', data) AS mes FROM receitas")
    receitas = cursor.fetchall()

    if receitas:
        for receita in receitas:
            receita_info = f" > {receita[1]}"
            if st.checkbox(f"Editar | Excluir {receita_info}", key=f"checkbox_receita_{receita[0]}"):
                origem = st.text_input(f"Origem da Receita {receita_info}", value=receita[1], key=f"origem_{receita[0]}")
                valor_receita = st.number_input(f"Valor da Receita {receita_info}", min_value=0.01, format="%.2f", value=receita[2], key=f"valor_receita_{receita[0]}")
                data_receita = st.date_input(f"Data da Receita {receita_info}", value=pd.to_datetime(receita[3]), key=f"data_receita_{receita[0]}")

                if st.button(f"Atualizar Receita {receita_info}", key=f"atualizar_{receita[0]}"):
                    try:
                        cursor.execute("UPDATE receitas SET origem = ?, valor = ?, data = ? WHERE id = ?", 
                                       (origem, valor_receita, data_receita, receita[0]))
                        conn.commit()
                        st.success(f"Receita {receita_info} Atualizada!")
                        st.rerun()  # 🔄 Recarrega a página
                    except Exception as e:
                        st.error(f"Erro ao atualizar: {e}")

                if st.button(f"Excluir Receita {receita_info}", key=f"excluir_{receita[0]}"):
                    try:
                        cursor.execute("DELETE FROM receitas WHERE id = ?", (receita[0],))
                        conn.commit()
                        st.success(f"Receita {receita_info} Excluída!")
                        st.rerun()  # 🔄 Recarrega a página
                    except Exception as e:
                        st.error(f"Erro ao excluir: {e}")
    else:
        st.info("Nenhuma receita registrada ainda.")

    # Seção para cadastrar nova receita
    st.subheader("Cadastrar Nova Receita")
    origem = st.text_input("Origem da Receita")
    valor_receita = st.number_input("Valor da Receita", min_value=0.01, format="%.2f", key="novo_valor_receita")
    data_receita = st.date_input("Data da Receita", key="nova_data_receita")

    if st.button("Salvar Receita"):
        if origem and valor_receita and data_receita:
            try:
                # Obtendo o mês a partir da data da receita
                mes_receita = str(data_receita.month).zfill(2)
                cursor.execute("INSERT INTO receitas (origem, valor, data, mes) VALUES (?, ?, ?, ?)", 
                               (origem, valor_receita, data_receita, mes_receita))
                conn.commit()
                st.success("Receita Adicionada!")
                st.rerun()  # 🔄 Recarrega a página
            except Exception as e:
                st.error(f"Erro ao salvar receita: {e}")
        else:
            st.warning("Preencha todos os campos antes de salvar!")
