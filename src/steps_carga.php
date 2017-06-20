<?php
/**
 * Carga das fontes de dados do TrazDia e OFICIAL.NEWS.
 *
 * Rodar direto no terminal.  php steps_carga.php -a
 */

// Configs:
$pasta = './tmp/traz/';
$scope = [
  'dout'=>'Doutrina',   'exe'=>'Executivo', 	'jud'=>'Judiciário',  'mdl'=>'Modelo de Contrato',
  'leg'=>'Legislativo', 'orig'=>'Original', 	'org'=>'Organização', 'mil'=>'Militar'
];

$sources = [
	'https://raw.githubusercontent.com/datasets-br/state-codes/master/data/br-state-codes.csv',
	'https://raw.githubusercontent.com/datasets/country-codes/master/data/country-codes.csv',
	'...'
];

if (!file_exists($pasta)) mkdi($pasta);


?>


