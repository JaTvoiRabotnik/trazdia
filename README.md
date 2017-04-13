[![Build Status](https://travis-ci.org/JaTvoiRabotnik/trazdia.svg?branch=master)](https://travis-ci.org/JaTvoiRabotnik/trazdia)

# trazdia
Trazdia, o trazedor de Diarios Oficiais. Ele baixa os Diarios Oficiais brasileiros direto dos sites do governo.

### Como contribuir:
Esse é um projeto Open Source, toda contribuição é bem vinda. Usamos um processo de review, ou seja, ninguem pode fazer commit direto ao Master. Crie um branch e um Pull Request a ser aprovado por outro membro do projeto. Todo Pull Request deve ser adicionado a um Projeto. Igualmente os Issues. Por favor colabore para manter o projeto bem organizado, isso ajuda a manter nosso trabalho profissional, e tambem serve como treinamento de best practices.

**Instruções:**
*Recomendamos desenvolver em um sistema Linux. Se tua máquina é Windows, instale um VM Ubuntu*
* Clone o repositório na sua máquina
* Crie um virtualenv dentro do diretório do repositório e instale as dependências:
  * instale virtualenv `pip install virtualenv`
  * dentro do diretório crie um virtual environment: `virtualenv venv`. Isso cria um diretório chamado venv que vai conter todas as dependências necessárias.
  * ative o virtual environment: `source venv/bin/activate`
  * instale as dependências: `pip install -r requirements.txt`

Toda vez que você criar um pull request no repositório da okfn-brasil, um job no Travis vai começar e rodar todos os testes. Acompanhe o resultado direto na página: [Travis pull requests](https://travis-ci.org/okfn-brasil/trazdia/pull_requests).

Uma vez que o pull request foi aprovado e fundido com o Master, outro teste vai rodar e se tudo correr bem, [automaticamente implantado no Heroku](https://dashboard.heroku.com/apps/trazdia "Heroku build page")

### Linguagem:
Por favor comunique-se em Português na descrição dos Issues, Milestones, etc. Mas dentro do código, incluindo testes e mensagens de commit, use o Inglês. A razão disso é que o aplicativo tem que ser auto-documentável e acessível internacionalmente, e o Inglês é a língua franca da programação.
