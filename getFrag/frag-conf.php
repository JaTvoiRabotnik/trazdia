<?php
/**
 * Basic and default configurations.
 */

// global settings:
setlocale(LC_ALL, 'pt_BR'); //  CUIDADO SE FOR OUTRA LINGUA! minimo LC_CTYPE
mb_internal_encoding('UTF-8');


$PG_CONSTR = 'pgsql:host=localhost;port=5432;dbname=issnl';
$PG_USER = 'postgres';
$PG_PW   = 'postgres';

$is_cli = (php_sapi_name() === 'cli');  // true when is client (terminal).

$outFormatMime = ['j'=>'application/json', 'x'=>'application/xml', 't'=>'text/plain'];
$status = 200;
  // 404 - has not found the input issn.
  // 416 - issn format is invalid.


// mapeando e validando estrutura da DTD esperada:
$dtd2tag = [  // cache aqui ou busca no banco de dados das DTDs
	'html5-lex1'=>[  // com div e caput
		'art_rgx'=>'/^(artigo|art|a)(\d+)(?:(caput|item|it|al[ií]nea|alin|par[aá]grafo|i|a|p)(.+))?/u',
		'art'=>['a'=>'div'], // (p|div)
		'artIdPrefix'=>'art',
		'item'=>["i"=>'li',"a"=>'li',"p"=>'p'],

		'sec_rgx'=>'/^(s)(\d[\d\.]*)|^(se[cç][aã]o|cap[íi]tulo|t[íi]tulo|sec|cap|tit)-?(\d+|[ivx]+)(.*)/u',
		'sec'=>['s'=>'section', 'se'=>'section', 'ca'=>'section', 'ti'=>'section'],
		'secIdPrefix'=>'sec',
	],
	'html5-lex0pre'=>[ // sem caput sem div
		'art_rgx'=>'/^(artigo|art|a)(\d+)(?:(item|it|al[ií]nea|alin|par[aá]grafo|i|a|p)(.+))?/u',
		'art'=>['a'=>'p'],  // aqui só que muda!
		'artIdPrefix'=>'art',
		'item'=>["i"=>'li',"a"=>'li',"p"=>'p'],

		'sec_rgx'=>'/^(s)(\d[\d\.]*)|^(se[cç][aã]o|cap[íi]tulo|t[íi]tulo|sec|cap|tit)-?(\d+|[ivx]+)(.*)/u',
		'sec'=>['s'=>'section', 'se'=>'section', 'ca'=>'section', 'ti'=>'section'],
		'secIdPrefix'=>'sec',
	]
];
$dtds = array_keys($dtd2tag);


?>
