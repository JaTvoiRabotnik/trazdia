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

## SQL

Ver arquivos preparados em *steps*:

* [step1_lib](step1_lib.sql): atualiza a *library* de funções básicas (*snippets*) de apoio a triggers, etc.

* [step2_schema](step2_schema.sql): cria o esquema e suas tabelas. Cuidado: faz drop cascade do esquema inteiro.

* [step3_carga](step3_carga.sql): carrega datasets nas tabelas, agregando diversas fontes diferentes.

* ...


