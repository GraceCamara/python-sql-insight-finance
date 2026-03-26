import streamlit as st 
import sqlite3 
import pandas as pd 
import plotly.express as px

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="ERP Light - Gestão PME", page_icon="🏢", layout="wide") 

#CONFIGURAÇÃO DE SEGURANÇA 
SENHA_MESTRE = "adm123" 

if "logado" not in st.session_state:
    st.session_state["logado"] = False

def tela_login():
    st.markdown("<h2 style='text-align: center;'>🔐 Acesso Restrito - Gestão PME</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        senha = st.text_input("Digite a Senha de Acesso", type="password")
        if st.button("Entrar no Sistema"):
            if senha == SENHA_MESTRE:
                st.session_state["logado"] = True
                st.rerun()
            else:
                st.error("❌ Senha incorreta!")

if not st.session_state["logado"]:
    tela_login()
    st.stop()

# FUNÇÕES DE BANCO DE DADOS
def conectar():
    return sqlite3.connect('meu_banco_financeiro.db')

def salvar_lancamento(data, fornecedor, centro_custo, valor, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transacoes (data, descricao, categoria, valor, status, ativo) 
        VALUES(?,?,?,?,?,1)
    ''', (data, fornecedor, centro_custo, valor, status))
    conn.commit()
    cursor.close()
    conn.close()

# INTERFACE PRINCIPAL (PÓS-LOGIN)
st.title("🏢 Nexus Finance - Gestão PME")
st.markdown("---")

# Botão barra lateral
if st.sidebar.button("🚪 Sair do Sistema"):
    st.session_state["logado"] = False
    st.rerun()

#BARRA LATERAL
st.sidebar.header("📝 Novo Lançamento") 
with st.sidebar.form("form_empresa"):
    data_venc = st.date_input("Data de Vencimento")
    fornecedor_input = st.text_input("Fornecedor / Prestador")
    centro_custo_input = st.selectbox("Centro de Custo", 
                                ["Operacional", "Marketing/Vendas", "Pessoal/RH", "Infraestrutura/Aluguel", "Impostos", "Outros"])
    valor_input = st.number_input("Valor da Nota (R$)", min_value=0.0, step=0.01)
    status_input = st.radio("Status do Pagamento", ["Pendente", "Pago"])
    btn_salvar = st.form_submit_button("Registrar no Fluxo")
    
    if btn_salvar:
        if fornecedor_input:
            salvar_lancamento(str(data_venc), fornecedor_input, centro_custo_input, valor_input, status_input)
            st.sidebar.success("✅ Lançamento registrado!")
            st.rerun()
        else:
            st.sidebar.error("❌ Preencha o Fornecedor.")

# BANCO - DATAFRAME
conn = conectar()
try:
    df = pd.read_sql_query("SELECT * FROM transacoes WHERE ativo = 1", conn)
except:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT, descricao TEXT, categoria TEXT, valor REAL, status TEXT, ativo INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    df = pd.read_sql_query("SELECT * FROM transacoes WHERE ativo = 1", conn)
conn.close()

# DASHBOARD
if not df.empty:
    st.subheader("🔍 Painel de Auditoria e Controle")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filtro_status = st.multiselect("Filtrar por Status:", options=df['status'].unique(), default=df['status'].unique())
    with col_f2:
        filtro_setor = st.multiselect("Filtrar por Setor:", options=df['categoria'].unique(), default=df['categoria'].unique())

    df_filtrado = df[df['status'].isin(filtro_status) & df['categoria'].isin(filtro_setor)]
    
    col_tabela, col_grafico = st.columns([2, 1])
    
    with col_tabela:
        st.subheader("📑 Data View: Histórico de Transações")
        if not df_filtrado.empty:
            df_visivel = df_filtrado.drop(columns=['id', 'ativo']).rename(columns={
                'data': 'Vencimento', 'descricao': 'Fornecedor', 'categoria': 'Setor', 'valor': 'Valor (R$)'
            })
            st.dataframe(df_visivel, use_container_width=True, hide_index=True)
            
            # CSV
            csv = df_visivel.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Baixar Relatório (CSV)", csv, "fluxo_caixa.csv", "text/csv")
        else:
            st.warning("Nenhum dado encontrado para os filtros.")

    with col_grafico:
        st.subheader("📊 KPIs de Performance Financeira")
        if not df_filtrado.empty:
            st.metric("Total no Período", f"R$ {df_filtrado['valor'].sum():.2f}")
            fig = px.pie(df_filtrado, values='valor', names='categoria', hole=0.4, title="Gastos por Setor")
            st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👋 Bem-vinda! O sistema está pronto. Cadastre o primeiro lançamento na barra lateral.")

# MANUTENÇÃO (ARQUIVAR)
st.markdown("---")
if st.button("🧹 Delete"):
    conn = conectar()
    conn.execute("UPDATE transacoes SET ativo = 0 WHERE ativo = 1")
    conn.commit()
    conn.close()
    st.success("Dados arquivados no histórico!")
    st.rerun()