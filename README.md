# lunch-votes

Lunch vote é uma aplicação desenvolvida para resolver um problema comumente encontrado, como a definição do local do almoço de funcionários de uma empresa.

A aplicação permite votar no restaurante favorito, cada funcionário somente pode votar um única vez por dia. O restaurante com a maior quantidade votos será escolhido. Uma vez que o restaurante foi definido na semana corrente, não poderá ser repetido.

A aplicação permite apurar os votos uma única vez, uma vez que essa é feita, quem não votou pode ainda votar, porém não terá nenhum impacto no resultado. A intenção é que seja apurada uma única vez antes do meio dia.

A aplicação não possui nenhum controle de usuários, será confiado na boa índole de cada pessoa, selecionado seu próprio usuário e votando uma única vez.


## Implementação

Foi utilizado a linguagem de programação python para desenvolver o serviço de controle de votos, esta usada somente pela preferência do programador.

Vale destacar a utilização da base de dados Redis pela simplicidade em utilizar e pela eficiência ao buscar informações armazenadas em disco. Esta aplicação não tem necessidade de uma base de dados relacional, justifica-se o uso de Redis.

Outro ponto importante é a utilização do serviço de cloud Heroku, que em apenas alguns passos a aplicação está disponível para acesso externo.

Toda aplicação utiliza uma biblioteca de logs, esta pode ser configurada via arquivo de configuração sem necessidade de alterar código. Esta mesma abordagem foi utilizada para "cadastrar" restaurantes e usuários.

O projeto conta com três classes principais, são elas:

* VoteManager, 
Esta classe é o core da implementação, pois é responsável por manter todos critérios de aceitação (somente um voto diário por pessoa, o mesmo restaurante não pode ser repetido durante a semana corrente e mostrar o resultado da votação).
Toda lógica embutida nesta classe é gerenciada através da base de dados do Redis, utilizando chave - valor, por exemplo:

chave <userName>, especifica que o determinado usuário já efetuou seu voto diário.
chave restaurant.<date>.<restauranteName>,  contém a quantidade de votos para determinado restaurante.
chave restaurant.<date>,  contém o restaurante definido para a data atrelada na chave.
chave restaurant.week.<weekNumber>, contém a lista de resturantes já definidos na semana <weekNumber>

* Config, 
Classe responsável por interpretar o arquivo de configuração do projeto.

* DB, 
Classe responsável por gerenciar acesso a base de dados Redis.


Esta implementação conta com uma suite de testes unitários, com uma cobertura acima de 80%. Também conta com arquivos básicos para criação de um ambiente virtual do python.

## Melhorias
Algumas melhorias poderiam ser feitas, no sentido de performance caso o número de usuário seja muito maior.

Redis é uma boa opção pois prevê eficiência nas transações, é uma base de dados mantida em memória, gravada em disco em período de tempos pré-configurados e também pela facilidade na utilização. Porém sua desvantagem é ser single thread(bloqueante) e causar um overhead significante na persistência de dados.

Questões de melhorias na implementação seriam possíveis, como adicionar um TTL em cada chave do Redis para que as mesmas não ficassem eternamente armazenadas na base de dados, pois algumas informações não são relevantes de serem armazenadas.



