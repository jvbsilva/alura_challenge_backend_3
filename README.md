

<p align="center">
  <h1>Análise de Transações Financeiras</h1>
  <br>
<img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge"/>
</p>

Projeto desenvolvido durante o Terceiro desafio de Back-End realizado pela [Alura](https://www.alura.com.br/).

#alurachallengebackend3

## Descrição
O projeto cosiste em uma aplicação web onde é possível fazer o upload de transações financeiras e posteriormente essas transações serão analisadas com o intuito de identificar possíveis fraudes.

## :hammer: Funcionalidades do projeto

Até o presente momento o projeto conta com as seguintes funcionalidades:

- `Sistema de Login e Cadastro`: Para acessar a a aplicação é preciso fazer login fornecendo um email e senha.
- `Validação das importações`: Cada arquivo importado passa por uma validação onde as transações inválidas são descartadas e apenas as transações no formato correte são salvas no bando de dados.
- `Histórico das importações`: A cada importação realizada é armazenada e a informação sobre a data a que as transações pertencem, a data e hora em que a importação foi realizada e qual o usuário efetuou a importação.
- `CRUD de usuários`: E possível realizar a consulta, alteração e remoção dos usuários sendo que para um usuário ser removido primeiro ele deve ter seu status alterado para 'Inativo' o que faz com que um usuário não possa se auto remover uma vez que ao alterar seu status para 'Inativo' este perde o acesso à aplicação.<br>Antes de realizar a exclusão de um usuário um modal de confirmação é acionado mostrando o nome do usuário que será excluído caso a exclusão de concretize.
- `Sistema de alertas e mensagens`: Para todas as funcionalidade presentes existe um sistema de mensagens que comunica ao usuário o sucesso ou falha ao executar as ações. No caso das falhas é informado os motivos que cocasionaram a falha.
-  `Menu de navegação`: O menu de navegação está presente nas áreas de acesso restrito da aplicação (apenas para usuários autenticados). Esse menu possibilita a navegação entre as áreas da aplicação bem como realizar o logout. Nele também é exibida a informação sobre a identidade do usuário logado no momento.

## ✔️ Técnicas e tecnologias utilizadas

- ``Python``
- ``Django``
- ``PostgreSQL``
