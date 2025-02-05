import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Conectar ao banco de dados
conn = sqlite3.connect("orcamento.db")
cursor = conn.cursor()

# Criar tabelas se não existirem
cursor.execute("""
CREATE TABLE IF NOT EXISTS receitas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origem TEXT NOT NULL,
    valor REAL NOT NULL,
    data TEXT NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS despesas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL,
    valor REAL NOT NULL,
    responsavel TEXT NOT NULL,
    data TEXT NOT NULL
)
""")
conn.commit()

# Título principal
st.title("💰 Gerenciador de Orçamento Familiar")

### 📥 Seção para adicionar ou editar receitas
st.header("📥 Adicionar ou Editar Receita")

# Exibir receitas registradas para edição ou exclusão
cursor.execute("SELECT id, origem, valor, data FROM receitas")
receitas = cursor.fetchall()

# Se houver receitas registradas, mostrar para edição
if receitas:
    for receita in receitas:
        receita_info = f" > {receita[1]}"
        
        if st.checkbox(f"Editar | Excluir {receita_info}", key=f"checkbox_receita_{receita[0]}"):
            # Exibir dados para edição
            origem = st.text_input(f"Origem da Receita {receita_info}", value=receita[1], key=f"origem_{receita[0]}")
            valor_receita = st.number_input(f"Valor da Receita {receita_info}", min_value=0.01, format="%.2f", value=receita[2], key=f"valor_receita_{receita[0]}")
            data_receita = st.date_input(f"Data da Receita {receita_info}", value=pd.to_datetime(receita[3]), key=f"data_receita_{receita[0]}")

            # Atualizar receita
            if st.button(f"Atualizar Receita {receita_info}", key=f"atualizar_{receita[0]}"):
                cursor.execute("UPDATE receitas SET origem = ?, valor = ?, data = ? WHERE id = ?", 
                               (origem, valor_receita, data_receita, receita[0]))
                conn.commit()
                st.success(f"Receita {receita_info} Atualizada!")

            # Excluir receita
            if st.button(f"Excluir Receita {receita_info}", key=f"excluir_{receita[0]}"):
                cursor.execute("DELETE FROM receitas WHERE id = ?", (receita[0],))
                conn.commit()
                st.success(f"Receita {receita_info} Excluída!")
else:
    st.info("Nenhuma receita registrada ainda.")

# Se não houver receitas, permitir a inserção
st.subheader("Cadastrar Nova Receita")
origem = st.text_input("Origem da Receita")
valor_receita = st.number_input("Valor da Receita", min_value=0.01, format="%.2f", key="novo_valor_receita")
data_receita = st.date_input("Data da Receita")

if st.button("Salvar Receita"):
    cursor.execute("INSERT INTO receitas (origem, valor, data) VALUES (?, ?, ?)", 
                   (origem, valor_receita, data_receita))
    conn.commit()
    st.success("Receita Adicionada!")

### 📤 Seção para adicionar ou editar despesas
st.header("📤 Adicionar ou Editar Despesa")

# Exibir despesas registradas para edição ou exclusão
cursor.execute("SELECT id, categoria, valor, responsavel, data FROM despesas")
despesas = cursor.fetchall()

if despesas:
    opcoes_despesas = {f"{despesa[1]} - R$ {despesa[2]:.2f}": despesa for despesa in despesas}
    escolha = st.selectbox("Selecione uma despesa para editar:", list(opcoes_despesas.keys()))
    despesa = opcoes_despesas[escolha]
    
    categoria = st.text_input("Categoria da Despesa", value=despesa[1], key=f"categoria_{despesa[0]}")
    valor_despesa = st.number_input("Valor da Despesa", min_value=0.01, format="%.2f", value=despesa[2], key=f"valor_despesa_{despesa[0]}")
    responsavel = st.selectbox("Responsável pelo Pagamento", ["Léo", "Vivian"], index=["Léo", "Vivian"].index(despesa[3]), key=f"responsavel_{despesa[0]}")
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

# Se não houver despesas, permitir a inserção
st.subheader("Cadastrar Nova Despesa")
categoria = st.text_input("Categoria da Despesa")
valor_despesa = st.number_input("Valor da Despesa", min_value=0.01, format="%.2f", key="novo_valor_despesa")
responsavel = st.selectbox("Responsável pelo Pagamento", ["Léo", "Vivian"])
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

# Fechar conexão com o banco
conn.close()