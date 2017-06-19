Modelo de dados inicial, para a primeira fase do projeto Trazdia e de produção do OFICIAL.NEWS,

![ [](https://yuml.me/980f72f2) ](https://yuml.me/980f72f2)

```
[Jurisdição|-id;name;lexname;abbrev]
[Organização|-cnpj;name;abbrev;info:JSON]

[Autoridade|-id;name;lexname;abbrev]
[Fascículo| -id; oficial_id; data; seq; oficial_url; info:JSON]
[Contrato|contrato_url;contrato_valor;contrato_fracao]

[Jurisdição]1---*[Autoridade]
[Organização]^-[Editora]
[Organização]^-[Contratante]
[Autoridade]^-[Contratante]

[PubSeriada|-issn;name;abbrev;isDiario;info:JSON]
[DiarioOficial|-id;name;abbrev;info:JSON]

[Jurisdição]1..*---*[DiarioOficial]
[Contratante]1---1..*[Contrato]
[Editora]---1..*[Contrato]
[PubSeriada]++-1>[DiarioOficial]
[PubSeriada]^-[Dedicada]
[DiarioOficial]++-1..*>[Fascículo]
[Contrato]<>---1..*[Fascículo]
[Editora]<>---1..*[PubSeriada]
```

### Tradução para o inglês

Como o código e nomes de variáveis são em inglês, a base de dados também requer nomes de tabela e de campos em ingles. Para garantir consistência, usaremos sempre que possível termos do http://schema.org/ , quando não houver mais detalhado no  [padrão URN LEX](https://datatracker.ietf.org/doc/draft-spinosa-urn-lex/).


* _Jurisdição_ = `Jurisdiction` (URN LEX). Campos da tabela: já traduzidos.<br/> A jurisdição faz o papel de [areaServed](http://schema.org/areaServed) da autoridade.

* _Organização_ = [`Organization`](http://schema.org/Organization). Campos da tabela: já traduzidos.

* _Autoridade_ = `authority` (URN LEX), que pode ser duas coisas similares porém utilizadas de forma distinta:<br> 1. o responsável (autor e/ou tutelar) pelo contedo publicado em uma dada seção do diário oficial ou matéria. <br/>2. um [GovernmentService](http://schema.org/GovernmentService) que contrata a editora e/ou faz o papel de editora.

* _Fascículo_ = [`PublicationIssue`](http://schema.org/PublicationIssue). Campos da tabela: id; official_id; date; seq; official_url; info:JSON.

* _Contratante_ = [`GeneralContractor`](http://schema.org/GeneralContractor).. Campos da tabela: authority_id, organization_id, ...

* _Contrato_ = `contract`. Campos da tabela: authority_id, contrato_url;contrato_valor;contrato_fracao]

* _Editora_ = [`publisher`](http://schema.org/publisher)...

* ...


## SQL

Ver arquivos preparados em *steps*:

* [step1_lib](step1_lib.sql): atualiza a *library* de funções básicas (*snippets*) de apoio a triggers, etc.

* [step2_schema](step2_schema.sql): cria o esquema e suas tabelas. Cuidado: faz drop cascade do esquema inteiro.

* [step3_carga](step3_carga.sql): carrega datasets nas tabelas, agregando diversas fontes diferentes.


* ...


