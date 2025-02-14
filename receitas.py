import streamlit as st
import pandas as pd

def gerenciar_receitas(conn):
    st.header("📥 Adicionar ou Editar Receita")
    cursor = conn.cursor()
    cursor.execute("SELECT id, origem, valor, data FROM receitas")
    receitas = cursor.fetchall()

    if receitas:
        for receita in receitas:
            receita_info = f" > {receita[1]}"
            if st.checkbox(f"Editar | Excluir {receita_info}", key=f"checkbox_receita_{receita[0]}"):
                origem = st.text_input(f"Origem da Receita {receita_info}", value=receita[1], key=f"origem_{receita[0]}")
                valor_receita = st.number_input(f"Valor da Receita {receita_info}", min_value=0.01, format="%.2f", value=receita[2], key=f"valor_receita_{receita[0]}")
                data_receita = st.date_input(f"Data da Receita {receita_info}", value=pd.to_datetime(receita[3]), key=f"data_receita_{receita[0]}")

                if st.button(f"Atualizar Receita {receita_info}", key=f"atualizar_{receita[0]}"):
                    cursor.execute("UPDATE receitas SET origem = ?, valor = ?, data = ? WHERE id = ?", 
                                   (origem, valor_receita, data_receita, receita[0]))
                    conn.commit()
                    st.success(f"Receita {receita_info} Atualizada!")

                if st.button(f"Excluir Receita {receita_info}", key=f"excluir_{receita[0]}"):
                    cursor.execute("DELETE FROM receitas WHERE id = ?", (receita[0],))
                    conn.commit()
                    st.success(f"Receita {receita_info} Excluída!")
    else:
        st.info("Nenhuma receita registrada ainda.")

    st.subheader("Cadastrar Nova Receita")
    origem = st.text_input("Origem da Receita")
    valor_receita = st.number_input("Valor da Receita", min_value=0.01, format="%.2f", key="novo_valor_receita")
    data_receita = st.date_input("Data da Receita")

    if st.button("Salvar Receita"):
        cursor.execute("INSERT INTO receitas (origem, valor, data) VALUES (?, ?, ?)", 
                       (origem, valor_receita, data_receita))
        conn.commit()
        st.success("Receita Adicionada!")