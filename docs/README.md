Hub da Documentação

## Identificador ou URN do documento

As matérias dos fascículos dos diários oficiais quando publicadas na forma de separatas, podem ser caracterizadas como documentos independetes, e cada uma requer seu identificador, que pode ser o ID da matéria dentro do fascículo, ou um identificador transparente universal, baseado nos metadados básicos do documento, inspirado na [URN LEX](https://en.wikipedia.org/wiki/Lex_(URN)).

... maiores detalhes.... criar arquivo `docId.md` ...

## Identificador de fragmento e API `getfrag`

Para obter o conteúdo de um fragmento de documento, ou seja, uma porção fixada por sua estrutura, basta designar o identificador do fragmento desejado. Como os documentos normativos (eg. normas técnicas e legislação) e os contratos são todos formatados da mesma forma (usando HTML5 simplificado) e com uma estrutura similar, pode-se designar os elementos estruturais como identificadores padronizados.

A API `api.oficial.news/getfrag` faz esse "meio de campo", interpretando identificadores expressos dentro de uma sintaxe padronizada (são oferecidos um padrão canônico compacto e um padrão alternativo baseado no LexML), e extraindo o fragmento desejado de dentro do documento indicado.

A especificação completa da API se encontra em [getfrag-v1.0.0-swagger.yaml](getfrag-v1.0.0-swagger.yaml) (visualizar em [swaggerhub.com/ppKrauss/getfrag/1.0.0](https://app.swaggerhub.com/apis/ppKrauss/getfrag/1.0.0)). A especificação completa da sintaxe está em **[fragId.md](fragId.md)**.

## ...
...
