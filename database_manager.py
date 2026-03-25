import sqlite3

def criar_banco():
    conexao = sqlite3.connect('meu_banco_financeiro.db')
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes ( 
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT  NULL, 
            descricao TEXT NOT NULL, 
            categoria TEXT NOT NULL, 
            valor REAL NOT NULL
        )
''')

def  salvar_transacao (data, descricao, categoria, valor):
    conexao = sqlite3.connect('meu_banco_financeiro.db')
    cursor = conexao.cursor()

    cursor.execute('''
        INSERT INTO transacoes (data, descricao, categoria, valor)
        VALUES (?, ?, ?, ?)
    ''', (data, descricao, categoria, valor))

    conexao.commit()
    conexao.close()
    print(f"✅ Sucesso! '{descricao}' foi para o banco.")

def ver_gastos():
    conexao = sqlite3.connect('meu_banco_financeiro.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM transacoes') 
    dados = cursor.fetchall() # resultados 
    conexao.close()

    if not dados:
        print("\n📭 O histórico está vazio.")
    else:
        print("\n--- 📑 MEUS GASTOS REGISTRADOS ---") 
        for linha in dados:
            print(f"ID: {linha[0]} | Data: {linha[1]} | {linha[2]} ({linha[3]}) | R$ {linha[4]:.2f}")

def limpar_banco():
    conexao = sqlite3.connect('meu_banco_financeiro.db')
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM transacoes')
    conexao.commit()
    conexao.close()
    print("\n🧹 Todo o histórico foi apagado!")

#VISÃO MENU
if __name__ == "__main__":
    criar_banco()
    #salvar_transacao('2026-03-24', 'Livro de Ficção', 'Lazer', 59.90)
    #ver_gastos ()
    while True:
        print("\n================================")
        print("💰 GERENCIADOR FINANCEIRO - GRACE")
        print("================================")
        print("1. Cadastrar novo gasto")
        print("2. Ver histórico de gastos")
        print("3. Limpar tudo (Reset)")
        print("4. Sair")

        opcao = input('\n O que deseja fazer? (1-4): ')

        if opcao == '1':
            desc = input("O que você comprou? ")
            cat = input("Qual a categoria? (ex: Lazer, Comida, Carro): ")
            val = float(input("Qual o valor? (ex: 50.00): "))
            data_hoje = "2026-03-24" # Data de hoje
            salvar_transacao(data_hoje, desc, cat, val)

        elif opcao == '2':
            ver_gastos()

        elif opcao == '3':
            confirmar = input ("⚠️ Tem certeza que quer apagar TUDO? (s/n): ")
            if confirmar.lower() == 's':
                limpar_banco()
        elif opcao == '4':
            print("\n Até logo, Grace! Boa sorte com as finanças. 👋")
            break
        else:
            print("\n❌ Opção inválida. Tente de 1 a 4.")

            #streamlit run app_web.py 