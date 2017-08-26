<?php
/**
 * Resolve o identificador LexCondo e confere sua presença no XML indicado.
 * Exemplo: php resolver.php estatuto2009-dtdLex a17i2
 *    http://teste.oficial.news/frag-resolver.php?file=estatuto2009-dtdLex1&fullFragId=a17i2
 */

define ('TEST',true);
include('frag-conf.php');  // ver ISSN
$is_json = false;

// INPUT:
if ($is_cli) {
	if ($argc==2 && $argv[1]) {
		if (preg_match('#^([^/]+)/(.+)$#',$argv[1],$m)) {
                $file = $m[1];
                $fullFragId = $m[2];
		} else die("\nERROR 22, uri invalida\n\t$argv[1]\n");
        } elseif ($argc!=3 || !$argv[1])
                die("\nERRRO 1, falta argumento\n");
	else {
		$file = $argv[1];
		$fullFragId = $argv[2];
	}
} else {
        $URI = $_REQUEST['uri'];
        $file = $_REQUEST['file'];
        $fullFragId = $_REQUEST['fullFragId'];
        if ( trim($URI) && preg_match('#^/?getfrag/([^/]+)/(.+)$#',$URI,$m) ) {
		$file = $m[1];
		$fullFragId = $m[2];
	}
// ex. getfrag/estatuto2009-dtdLex1/a17i2
  // used with API Gateway pre-parsing:
  //$fullFragId = $_REQUEST['fullFragId'];
  //$fullFragId = $_REQUEST['fullFragId'];
}

if (!$file || !$fullFragId) dieMsg("
Use por exemplo, para pegar fragmentos do documento <a href='estatuto2009-dtdLex1.htm'>estatuto2009-dtdLex1</a>,
<br/> &nbsp; <a href='/getfrag/estatuto2009/a17i2'><code>/getfrag/estatuto2009/a17i2</code></a>
<br/> &nbsp; <a href='/getfrag/estatuto2009/a17'><code>/getfrag/estatuto2009/a17</code></a>
<br/> &nbsp; <a href='/getfrag/estatuto2009/s1.2'><code>/getfrag/estatuto2009/s1.2</code></a>

<p>Maiores detalhes em <a href='http://api.ok.org.br#getfrag'><big>api.ok.org.br#getfrag</big></a>.
<hr>
LIXO ANTIGO!
<p>Para GET com argumentos (NAO RECOMENDADO),
<br/> &nbsp; <a href='/frag-resolver.php?file=estatuto2009-dtdLex1&fullFragId=a17i2'><code>?file=estatuto2009-dtdLex</code>&<code>fullFragId=a17i2</code></a>.
<br/> &nbsp; <a href='/frag-resolver.php?file=estatuto2009-dtdLex1&fullFragId=a17'><code>?file=estatuto2009-dtdLex</code>&<code>fullFragId=a17</code></a>
<br/> &nbsp; <a href='/frag-resolver.php?file=estatuto2009-dtdLex1&fullFragId=s1.2'><code>?file=estatuto2009-dtdLex</code>&<code>fullFragId=s1.2</code></a>
<br/>  documento do exemplo em <a href='estatuto2009-dtdLex1.htm'>estatuto2009-dtdLex1</a>.
</p>

<h2>Sintaxe do fullFragId</h2>
<p><h3>Articulação:</h3>
<ol>
<li>a, art, artigo
<li>número decimal inteiro
</ol>
Exemplos: <code>a2</code>,  <code>art2</code>,  <code>artigo2</code>
</p>

<p><h3>Sub-articulação: item, parágrafo ou alínea</h3>
<ul>
item|it|al[ií]nea|alin|par[aá]grafo|i|a|p
<li>p, par, ou parágrafo ('único', ou 1, ou 2, ou 3, ou ...)
<li>i, it, item (decimal ou romano)
<li>a, alin, alínea (letra) .. em construção
</ul>
Exemplos: <code>a2.3</code>,  <code>art2i3</code>,  <code>a2iII</code>,  <code>artigo-2-item-II</code>, ...
</p>

<p><h3>Blocos: títulos, capítulos ou seções</h3>
Opções:
<ol>
<li>s
<li>número decimal inteiro
<li>(opcional) ponto e outro número
</ol>
<br/>Exemplos: <code>s2</code>,  <code>s2.1</code>.
<br/>Ou:

<ol>
<li>ti, ca, se, título, capítulo, seção, ...
<li>número romano ou decimal
<li>(opcional) outro termo, subseção.
</ol>
Exemplos: <code>ti2</code>,  <code>ti2.1</code>, <code>tiII.I</code>, <code>titulo-II-capitulo-I</code>.
</p>
");

$translate = ['estatuto'=>'estatuto2009-dtdLex1', 'estatuto2009'=>'estatuto2009-dtdLex1'];
$aux = strtolower($file); if (isset($translate[$aux])) $file=$translate[$aux];

$pathFile = TEST? "/tmp/$file.htm" :"/var/www/api.ok.org.br/$file.htm";

$dom = xml2dom($pathFile);
if ($dom===false) dieMsg("arquivo não-encontrado: '$pathFile'",29);
$xpath = new DOMXPath($dom);

$domDtd = $xpath->evaluate("string(/html/head/meta[@name='dtd']/@content)");
if (!$domDtd)
  dieMsg("UNDEFINED DTD",4);
elseif (!in_array($domDtd,$dtds))   // see conf.php
  dieMsg("DTD desconhecida",5);

if (substr($fullFragId,0,8)=='info-toc') {
	// info-toc=default com tudo,  info-toc-tree= em avore, info-toc-label=só basico
	$is_json = true;
	$OUT = [];
	$lastId = '';
  $entries = $xpath->query('//p[@class="art"] | //section[h1 or h2 or h3 or h4] | //ol/li');
  foreach ($entries as $e) {
    $id    = $e->getAttribute('id');
		if ($id) $lastId = $id;
		$type  = $e->localName;
		$npath = $e->getNodePath();
		$npath = preg_replace('#^/html/body/article#i','//article[1]',$npath);  // depende de dtdLex1

    $s = mb_substr($e->nodeValue,0,100);
    $xpath->query('span',$e);
		$q = ($type=='section')? "string(./h1[1] | ./h2[1] | ./h3[1])" : "string(./span[1])";
    $label = trim( $xpath->evaluate($q,$e) );
    if ($id || $type=='li') {
			if (!$id) {
				$style = $e->parentNode->getAttribute('style');
				//$id=$lastId.(preg_replace('/^.+?li\[(\d+)\]$/i','.i$1',$npath));
				$id = $id2 = $lastId;
				$cont = 0;
				if ( preg_match('/^.+?li\[(\d+)\]$/i',$npath,$m) ) {
					$id2 .= ".i$m[1]";
					$cont = (integer) $m[1];
				}
				$q2 = preg_replace('#/li\[(\d+)\]$#i','',$npath);
				if (preg_match('/(?:list-)?style-type:\s*([^\s;]+)/is',$style,$m)) {
					$type = "$type-$m[1]";
					$label = getLabelOf($type,$cont);
				}
			} else
				$id2 = $id;
			$id2 = preg_replace('/^(article|artigo|art)/s','a',$id2);
			$id2 = preg_replace('/^(section|seção|sec)/us','s',$id2);
			// criar árvore de artigos dentro de seções etc. quando do flag toc-tree
			// e simplificar para id2-label quando flag simple
			if ($fullFragId=='info-toc-label')
				$OUT[]= "\n \"$id2\":\"$label\"";
			else {
				$out = ['_id'=>$id, '_label'=>$label, '_nodeType'=>$type, '_nodePath'=>$npath,];
				$OUT[] = "\n \"$id2\":".json_encode($out,JSON_FORCE_OBJECT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
			}
		} // if id
  } // foreach
  dieMsg("{". join(',',$OUT) ."\n}");
}
$xpQuery = pointer2xPath($fullFragId,$domDtd,0); // check errors
$entries = $xpath->query($xpQuery);
if ($entries->length==1) {
	$e = $entries[0];
	//dieMsg( "! veja: {$e->nodeValue}\n=".$dom->saveXML($e) );
        dieMsg( "<meta charset='utf-8'/>\n".$dom->saveXML($e) );
} elseif ($entries->length>1)
	dieMsg("múltiplos elementos com '$fullFragId' encontrados, unicidade requerida.",10);
else
	dieMsg("item '$fullFragId' não encontrado.",12);


// // // // // // // //
// // // // // // // //
// LIB

function dieMsg($msg,$cod=0) {
	global $is_json;
	global $is_cli;
	global $file;
	global $fullFragId;
	$out = $cod? "<h2>ERRO $cod</h2>: $msg": $msg;

	if ($is_cli) print "\n\t$out\n";
	elseif ($is_json) {
		header("Content-Type: application/json; charset=utf-8");
		print $cod? "{\"error_code\":$cod,\"error_msg\":\"$msg\"}": $msg;
	} else {
		header("Content-Type: application/xml");
		print "\n<html data-source='$file' data-source-filter='getfrag/$fullFragId'>$out</html>\n";
	}
	die("\n");
}

/**
 * When exists, converts the first occurence of "x(a|b)y" into "xay | xby".
 */
function xPath_expand($x,$checkN=0) {
	if (preg_match( '/^(.+?)\(([^\|]+)\|(.+?)\)(.+?)$/', $x, $m )) {
		return "$m[1]$m[2]$m[4] | $m[1]$m[3]$m[4]";
	} else return $x;
}

function pointer2xPath($ptr,$dtd='html5-lex1',$debug=1) {
  global $dtd2tag; // see conf.php

	if (isset($dtd2tag[$dtd])) { // existe a DTD na base de dados.
		$artRegex = $dtd2tag[$dtd]['art_rgx'];
		$artIdPrefix = $dtd2tag[$dtd]['artIdPrefix'];
		$art2tag  = $dtd2tag[$dtd]['art'];
		$item2tag = $dtd2tag[$dtd]['item'];
		$secRegex = $dtd2tag[$dtd]['sec_rgx'];
		$sec2tag  = $dtd2tag[$dtd]['sec'];
		$secIdPrefix = $dtd2tag[$dtd]['secIdPrefix'];
	} else
		die("\nERRO 33, DTD '$dtd' desconhecida.");

	$xp = '';
	$ptr    = trim(trim($ptr),'#-./;,');  // desacent() a cargo do preg_match().
	$ptr_lo = strtolower($ptr);
	if (preg_match($artRegex,$ptr_lo,$m)) {  // parse de ID de articulação
		$artId = $m[2];
		$artType = substr($m[1],0,1);
		$xp = "//{$art2tag[$artType]}[@id='$artIdPrefix$artId']";
		if (isset($m[4]) && $m[4]) {
			$resto_type = substr($m[3],0,2);  // i|a|p int, it|al|pa str
			$resto_id = $m[4];
			if (!ctype_digit($resto_id)) { // faz resto do parsing
				die("\nem construção! debug 232\n");
			}
			$xp .= '//'. $item2tag[substr($resto_type,0,1)] ."[position()=$resto_id]";
			// se strlen($resto_type)>1 pode ser romano, senao é normal
		} elseif ($m[0] != $ptr_lo)
			echo "\n\tWARNING: reconhecendo apenas '$m[0]' do ID '$ptr_lo'.\n";

	} elseif (preg_match($secRegex,$ptr_lo,$m)) {   // parse de ID de bloco (nível de seção)
		if (isset($m[1]) && $m[1]) {
			$secType = mb_substr($m[1],0,1);
			$secId = $m[2];
			$xp = "//{$sec2tag[$secType]}[@id='$secIdPrefix$secId']";
		} elseif (isset($m[4]) && $m[4]) {
			$secType = desacent( mb_substr($m[3],0,2) );
			$secIds = []; // FALTA converter romanos
			$checkM5 = isset($m[5]) && $m[5];
			$aux = [ $m[4] ];
			if ($checkM5 && mb_substr($m[5],0,1)=='.')
				$aux = $m[4].$m[5];
			elseif ($checkM5) {
				$aux = $m[4] .'.'. preg_replace('/cap[ií]tulo|título|se[çc][ãa]o|cap|tit|sec/u','.',$m[5]);
				$aux = preg_replace('/[\.\-]+/','.',$aux);
			}
			$aux = explode('.', $aux);
			foreach( $aux as $idpart )
					$secIds[] = ctype_digit($idpart)? $idpart: roman2dec($idpart);
			$secId = join('.',$secIds);
			$xp = "//{$sec2tag[$secType]}[@id='$secIdPrefix$secId']";
			echo "Bloco ($secId): $xp\n\t";
			//var_dump($m);
			//die("\n em construcao caso de capitulo e cia explicitos\n");
		} else {
			die("\n em construcao ERRO 3343\n");
		}
		// die("\nEM CONSTRUCAO 344\n.");
	} else
		die("\nERRO 343\n");
	if ($debug) echo "\n\t---debug xpath=$xp (from $ptr)";
	return xPath_expand($xp);
} //func


/**
 * Obtain DOMDocument from an arbitrary input (dom, XML filename or XML string).
 * @param $input string of filename or markup code.
 * @param $isHtml boolean (default false).
 * @param $flenLimit integer 0 or limit of filename length.
 * @param $keyStr string '<' for XML, "\n" for CSV.
 * @return boolean true when is filename or path string, false when markup.
 * @see https://github.com/ppKrauss/php-little-utils
 */
function xml2dom($input,$isHtml=false,$flenLimit=1000,$opts = LIBXML_NOCDATA |LIBXML_NOENT) {
	if (is_object($input))
    return ($input instanceof DOMDocument)? $input: NULL;
	else {
		return isFile($input,$flenLimit)?
			( $isHtml? DOMDocument::loadHTML_file($input,$opts): DOMDocument::load($input,$opts)    ):
			( $isHtml? DOMDocument::loadHTML($input,$opts):      DOMDocument::loadXML($input,$opts) );
	}
}


/**
 * Check if is a filename string, not a CSV/XML/HTML/markup string.
 * @param $input string of filename or markup code.
 * @param $flenLimit integer 0 or limit of filename length.
 * @param $keyStr string '<' for XML, "\n" for CSV.
 * @return boolean true when is filename or path string, false when markup.
 * @see https://github.com/ppKrauss/php-little-utils
 */
function isFile($input,$flenLimit=600,$keyStr='<') {
	return strrpos($input,$keyStr)==false && (!$flenLimit || strlen($input)<$flenLimit);
}

function desacent($str){ // ugly but reliable, from https://pt.stackoverflow.com/a/49655/4186
	return iconv('UTF-8', 'ASCII//TRANSLIT', $str);

}

/**
 * Roman to Decimal integers convertion.
 * NOTE: VIV=IX and LXL=XC, etc. are not error, so roman2dec(dec2roman($x)) can correct invalid romans.
 * @param $roman a valid (case insensitive) roman number.
 * @return the roman decimal value, or error as false (input decimal) or 0 (non-roman).
 */
function roman2dec($roman) {
	$romans = array(
			'M' => 1000, 'CM' => 900, 'D' => 500, 'CD' => 400, 'C' => 100,  'XC' => 90,
			'L' => 50,   'XL' => 40,  'X' => 10,  'IX' => 9,   'V' => 5,    'IV' => 4,
			'I' => 1,
	);
	if(is_numeric($roman)) return false; // regex valid?
	$dec = 0;
	$roman = strtoupper( trim($roman) ); // sanitize input, ignore case
	foreach ($romans as $key => $value)
		while (strpos($roman, $key) === 0) {
			$dec += $value;
			$roman = substr($roman, strlen($key));  // nao precisa mb
		}
	return $dec;
}

// falta dec2roman

/**
 * Roman to Decimal integers convertion.
 * NOTE: VIV=IX and LXL=XC, etc. are not error, so roman2dec(dec2roman($x)) can correct invalid romans.
 * @param $roman a valid (case insensitive) roman number.
 * @return the roman decimal value, or error as false (input decimal) or 0 (non-roman).
 */
function getLabelOf($type,$x) {
	$x2 = (integer) $x;
	$ref = '';
	if (!$x2) return $x;
	switch (strtolower(trim($type))) {
		case 'li-upper-alpha':  $ref = 64;
		case 'li-lower-alpha':  if (!$ref) $ref=96;
			if ($x2>27) return $x;
			return chr($ref+$x2);
		case 'li-upper-roman':  $isUpper = true;
		case 'li-lower-roman': if ($isUpper) $isUpper=false;
			if ($x2>27) return $x;
			return int2roman($x2,$isUpper);
	}
}


/**
* int2roman
* Convert any positive value of a 32-bit signed integer to its roman.
*
* @param $integer integer between 1 and 99999
* @return $upcase boolean true for upper case.
*/
function int2roman($integer, $upcase = true) {
    $table = array('M'=>1000, 'CM'=>900, 'D'=>500, 'CD'=>400, 'C'=>100, 'XC'=>90, 'L'=>50, 'XL'=>40, 'X'=>10, 'IX'=>9, 'V'=>5, 'IV'=>4, 'I'=>1);
    $return = '';
    while($integer > 0) {
        foreach($table as $rom=>$arb) if($integer >= $arb) {
                $integer -= $arb;
                $return .= $rom;
                break;
        } // for-if
    } // while
    return $return;
} //func

?>
