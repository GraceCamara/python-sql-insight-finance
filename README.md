## 🏢 ERP Light - Gestão Financeira para PMEs

O objetivo é automatizar o fluxo de dados financeiros, eliminando processos manuais de planilhas e utilizando SQL para persistência e análise de dados em tempo real.Este é um sistema de Fluxo de Caixa desenvolvido em Python, focado em resolver limitações comuns do uso de planilhas de Excel em PMEs. Diferente das planilhas convencionais, este projeto oferece uma plataforma centralizada que permite múltiplos acessos simultâneos com integridade de dados, além de uma estrutura preparada para o registro e rastreabilidade de modificações(versão 2.0), garantindo maior controle sobre quem realiza cada operação no sistema.

## 🚀 Funcionalidades

- Autenticação Segura: Tela de login com sessão protegida..
- Gestão de Lançamentos: Cadastro de despesas com data, fornecedor, categoria e status de pagamento.
- Banco de Dados Robusto: Persistência de dados utilizando SQLite3.
- Arquivamento Inteligente: Função de reset que preserva o histórico no SQL, apenas ocultando os dados da interface do usuário.
- Dashboard Interativo: Filtros dinâmicos por status e setor com gráficos de pizza gerados via Plotly Express.
- Exportação de Dados: Geração de relatórios em formato CSV para integração com Excel.

## 🛠️ Tecnologias Utilizadas

- Linguagem: Python 3.10+
- Framework Web: 
- Manipulação de Dados: Pandas
- Banco de Dados: SQLite3
- Visualização: Plotly

## 🧠 Desafios e Aprendizados

Durante o desenvolvimento deste projeto, enfrentei e superei desafios técnicos que consolidaram meu conhecimento em Back-end:

- Segurança e Estado da Sessão: Implementei o controle de acesso garantindo que o st.stop() interrompesse a execução do script caso o usuário não estivesse autenticado, protegendo as camadas ao banco de dados.
- Lógica de Soft Delete: Em vez de utilizar o comando DROP TABLE, optei por uma coluna ativo no SQL. Isso permite que o usuário "limpe" a tela sem causar a perda permanente de dados históricos, seguindo boas práticas de auditoria.
- Tratamento de Exceções no SQLite: Desenvolvi uma lógica de try/except para a criação automática da tabela e colunas necessárias na primeira execução, garantindo que o sistema seja "plug-and-play".
- Renderização Dinâmica: Ajustei a ordem de execução do Streamlit para evitar erros de variáveis não definidas durante a filtragem em tempo real.

## 📋 Como Executar o Projeto

1º - Clone este repositório;
2º - Instale as dependências;
3º - Execute a aplicação: