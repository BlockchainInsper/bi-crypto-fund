# BI-Crypto-Fund 📈

## Sobre o projeto
A ideia desse projeto é criar uma base de dados e uma API que possam ser utilizados para fazer os registros de transações do fundo fundamentalista da Blockchain Insper e calcular seu retorno acumulado para diversos períodos.

Após sua implementação, essa ferramenta poderá ser utilizada pelos membros da entidade, que realizam a gestão do fundo, para registrar remoções e adições de ativos e o ajuste de seus pesos.

Além disso, a API desse projeto também será utilizada pelo front-end, do website da entidade, para obter o histórico de retorno do fundo e realizar seu plot em um gráfico.

## Link para a documentação da API
- https://documenter.getpostman.com/view/18584366/UVJeEvrj#intro

## Guidelines

### **Alinhamentos gerais**
- Linguagem de programação que será utilizada: **Python**
- Biblioteca que será utilizada para criar a API: **Flask**
- Estrutura de base de dados: **mongoDB**
- Plataforma de deploy: **Heroku**

#### **Semana 15/11** ✅
- Definir tema do projeto
- Definir as tecnlogias que serão utilizadas no projeto
- Responder o formulário
- Criar um modelo de DB, utilizando DB Designer
- Criar um repositório no Github
- Iniciar o projeto
- Criar funções para obter dados de ativos, através da API do Yahoo Finance 
- Criar classes Asset e Transaction para o DB

#### **Semana 22/11** ✅
- Criar Use Cases para o DB
- Criar repositórios do mongoDB
- Testar o DB localmente
- Criar função para obter dados do DB, utilizando query
- Criar API, utilizando Flask
- Conectar o DB à API e realizar testes locais

#### **Semana 29/11** ✅
- Realizar o deploy do projeto, no Heroku
- Escrever a documentação da API
- **Extra**: Criar front-end para mostrar o retorno do fundo, no site da BI
- Encerramento do projeto
