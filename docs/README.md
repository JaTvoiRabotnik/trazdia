Hub da Documentação

## URN do diário oficial

Um Diário Oficial é um tipo de publicação periódica, podendo inclusive estar registrado sob ISSN. Neste caso terá tanto uma denominação como um [ISSN-L](https://github.com/okfn-brasil/ISSN-L-Resolver) &mdsh;  por exemplo "Diário Oficial da União" e  _1676-2339_.

O identificador canônico é a URN, por ser transparente e auxiliar na organização. O ISSN-L, quando existir, vale para a versão curta da URN canônica.

A sintaxe da URN do diário, inspiarada nos padrões [URN LEX](https://en.wikipedia.org/wiki/Lex_(URN)) e  [ELI](https://en.wikipedia.org/wiki/European_Legislation_Identifier), é detalhada em **[urnDiario.md](urnDiario.md)**.

## Identificador ou URN do documento

As matérias dos fascículos dos diários oficiais quando publicadas na forma de separatas, podem ser caracterizadas como documentos independetes, e cada uma requer seu identificador, que pode ser o ID da matéria dentro do fascículo, ou um identificador transparente universal, baseado nos metadados básicos do documento, inspirado na [URN LEX](https://en.wikipedia.org/wiki/Lex_(URN)).


... maiores detalhes.... criar arquivo `docId.md` ...


O identificador de matéria do diário oficial é um número sequencia fornecido pela autoridade competente. A recomendação é que a cada data de publicação seja reiniciado o contador, mas pode-se reiniciar por fascículo, por ano ou por diário &mdash; caso, por exemplo, do município do  Rio de  Janeiro.

A especificação completa da sintaxe está em **[fragId.md](fragId.md)**.

## APIs para resolução de nomes de diários e de separatas



## Identificador de fragmento e API `getfrag`

Para obter o conteúdo de um fragmento de documento, ou seja, uma porção fixada por sua estrutura, basta designar o identificador do fragmento desejado. Como os documentos normativos (eg. normas técnicas e legislação) e os contratos são todos formatados da mesma forma (usando HTML5 simplificado) e com uma estrutura similar, pode-se designar os elementos estruturais como identificadores padronizados.

A API `api.oficial.news/getfrag` faz esse "meio de campo", interpretando identificadores expressos dentro de uma sintaxe padronizada (são oferecidos um padrão canônico compacto e um padrão alternativo baseado no LexML), e extraindo o fragmento desejado de dentro do documento indicado.

A especificação completa da API se encontra em [getfrag-v1.0.0-swagger.yaml](getfrag-v1.0.0-swagger.yaml) (visualizar em [swaggerhub.com/ppKrauss/getfrag/1.0.0](https://app.swaggerhub.com/apis/ppKrauss/getfrag/1.0.0)). A especificação completa da sintaxe está em **[fragId.md](fragId.md)**.

## ...
...
