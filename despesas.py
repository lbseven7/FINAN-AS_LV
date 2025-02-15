import streamlit as st
import pandas as pd

def gerenciar_despesas(conn):
    st.header("📤 Editar Despesa")
    cursor = conn.cursor()
    cursor.execute("SELECT id, categoria, valor, responsavel, data FROM despesas")
    despesas = cursor.fetchall()

    if despesas:
        opcoes_despesas = {f"{despesa[1]} - R$ {despesa[2]:.2f}": despesa for despesa in despesas}
        escolha = st.selectbox("Selecione uma despesa para editar:", list(opcoes_despesas.keys()))
        despesa = opcoes_despesas[escolha]
        
        categoria = st.text_input("Categoria da Despesa", value=despesa[1], key=f"categoria_{despesa[0]}")
        valor_despesa = st.number_input("Valor da Despesa", min_value=0.01, format="%.2f", value=despesa[2], key=f"valor_despesa_{despesa[0]}")
        responsavel = st.selectbox("Responsável pelo Pagamento", ["Esposo", "Esposa"], index=["Esposo", "Esposa"].index(despesa[3]), key=f"responsavel_{despesa[0]}")
        data_despesa = st.date_input("Data da Despesa", value=pd.to_datetime(despesa[4]), key=f"data_despesa_{despesa[0]}")
        
        if st.button("Atualizar Despesa"):
            cursor.execute("UPDATE despesas SET categoria = ?, valor = ?, responsavel = ?, data = ? WHERE id = ?", 
                           (categoria, valor_despesa, responsavel, data_despesa, despesa[0]))
            conn.commit()
            st.success("Despesa Atualizada!")

        if st.button("Excluir Despesa"):
            cursor.execute("DELETE FROM despesas WHERE id = ?", (despesa[0],))
            conn.commit()
            st.success("Despesa Excluída!")
    else:
        st.info("Nenhuma despesa registrada ainda.")

    st.subheader("Cadastrar Nova Despesa")
    categoria = st.text_input("Categoria da Despesa")
    valor_despesa = st.number_input("Valor da Despesa", min_value=0.01, format="%.2f", key="novo_valor_despesa")
    responsavel = st.selectbox("Responsável pelo Pagamento", ["Esposo", "Esposa"])
    data_despesa = st.date_input("Data da Despesa")

    orçamento = st.selectbox("Como será pago?", [
        "Fundo 2025", 
        "Mercado", 
        "Emergência",
        "Prioridades",
        "Ajuda Leo",
        "Caixa Viagem", 
        "Emplacamento", 
        "Ajuda Vivian", 
        "Oferta Leo", 
        "Oferta Vivian", 
        "Caixa Yan",
        "Dízimos", 
        "Extras", 
        "Outros"
        ])
    if st.button("Salvar Despesa"):
        cursor.execute("INSERT INTO despesas (categoria, valor, responsavel, data) VALUES (?, ?, ?, ?)", 
                       (categoria, valor_despesa, responsavel, data_despesa))
        conn.commit()
        st.success("Despesa Adicionada!")

def exibir_dados(conn, tabela, colunas):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {tabela}")
    dados = cursor.fetchall()
    
    # Verificar se o número de colunas corresponde
    if dados and len(dados[0]) != len(colunas):
        st.error(f"Erro: Esperado {len(colunas)} colunas, mas os dados retornaram {len(dados[0])} colunas.")
        return
    
    df = pd.DataFrame(dados, columns=colunas)
    st.dataframe(df)