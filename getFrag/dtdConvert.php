<?php
/**
 * Converte DTDs para garantir processamento no frag-resolver.php.
 */
include('frag-conf.php');  // ver ISSN

if ($argc<2) die("\n ERRO: falta parametro filename\n");

//INPUT:
$file= $argv[1];
$pathFile = "./$file";
$dom = xml2dom($pathFile,false);  // flag conforme ext, conferir.
if_dieErr($dom===false, "\nERRO: arquivo não-encontrado: '$pathFile'", 29);

$dom = domPretty($dom,true);

$xpath = new DOMXPath($dom);
$domDtd = $xpath->evaluate("string(/html/head/meta[@name='dtd']/@content)");

if ($domDtd=='html5-lex0'){  // sobe para lex1
  //print "\n convertendo $domDtd para html5-lex0";
  $entries = $xpath->query('//p|//ul|//ol|//table|//blockquote');
  $group='error';
  foreach ($entries as $e) {
    $id = $e->getAttribute('id');
    $cl = $e->getAttribute('class');
    if (!$cl && !$id)  fwrite(STDERR, "\n\t-- WARNING at line ".$e->getLineNo()." '{$e->nodeValue}'");
    if ($cl=='art') $e->setAttribute('class','art-caput');
    if ($id>'') $group=$id;
    $e->setAttribute('data-group',$group);
	}
  groupTags_xs($dom, 'data-group', 'div');
  // falta remover id de p class="art-caput
  $xpath = new DOMXPath($dom);
  foreach ($xpath->query('//p[@id and @class="art-caput"]') as $e) $e->removeAttribute('id');
  domPrettyPrint($dom,false);

} elseif ($domDtd=='html5-lex0pre') {

  domXsltProc_idT($dom,'
    <xsl:template match="p[@class=\'art\']" priority="2">
        <div class="art" id="{@id}">
          <p class="art-caput"><xsl:apply-templates select="node()"/></p>
        </div>
    </xsl:template>
  ');
  domPrettyPrint($dom,true);
// remover o </p> e recarregar como html


} else dieErr("DTD DESCONHECIDA",4);



// // // // // // // //
// // // // // // // //
// LIB

function dieMsg($msg,$cod=0,$stderr=false) {
	global $is_json;
	global $is_cli;
	global $file;
	global $fullFragId;
	$out = $cod? "<h2>ERRO $cod</h2>: $msg": $msg;

	if ($is_cli) fwrite($stderr? STDERR: STDOUT, "\n\t$out\n");
	elseif ($is_json) {
		header("Content-Type: application/json; charset=utf-8");
		print $cod? "{\"error_code\":$cod,\"error_msg\":\"$msg\"}": $msg;
	} else {
		header("Content-Type: application/xml");
		print "\n<html data-source='$file' data-source-filter='getfrag/$fullFragId'>$out</html>\n";
	}
	die("\n");
}
function dieErr($msg,$cod=0) { dieMsg($msg,$cod,true); }
function if_dieErr($cond,$msg,$cod=0) { if ($cond) dieMsg($msg,$cod,true); }

/**
 * Obtain DOMDocument from an arbitrary input (dom, XML filename or XML string).
 * @param $input string of filename or markup code.
 * @param $isHtml boolean (default false).
 * @param $flenLimit integer 0 or limit of filename length.
 * @param $keyStr string '<' for XML, "\n" for CSV.
 * @return boolean true when is filename or path string, false when markup.
 * @see https://github.com/ppKrauss/php-little-utils
 */
function xml2dom(
  $input,
  $isHtml=false,
  $flenLimit=1000,
  $opts = LIBXML_NOCDATA | LIBXML_NOENT
) {
	if (is_object($input))
    return ($input instanceof DOMDocument)? $input: NULL;
	else {
		return isFile($input,$flenLimit)?
			( $isHtml? DOMDocument::loadHTMLfile($input,$opts): DOMDocument::load($input,$opts)    ):
			( $isHtml? DOMDocument::loadHTML($input,$opts):     DOMDocument::loadXML($input,$opts) );
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


/////////////

/**
 * Pretty output with saveXML().
 */
function domPretty($dom,$cleanHtm=false){
  if ($cleanHtm) {
    $dom->preserveWhiteSpace = false;
    $dom->formatOutput = true;
    $xml = $dom->saveXML($dom->documentElement);
    $xml = preg_replace('|\s*</p>|s', '</p>', $xml);
    $xml = preg_replace('|\s*<p|s', "\n<p", $xml);
    $dom = DOMDocument::loadXML($xml);
  }
  $dom->preserveWhiteSpace = false;
  $dom->formatOutput = true;
  return $dom;
}

function domPrettyPrint($dom,$cleanHtm=true){
  $dom = domPretty($dom,$cleanHtm);
  print $dom->saveXML($dom->documentElement);
}


/**
 * Changes DOM by an XSLT.
 */
function domXsltProc(&$dom,$xsltStr) {
  $xsdom = new DOMDocument;
  $xsdom->loadXML($xsltStr);

  $proc = new XSLTProcessor;
  if ($proc->importStyleSheet($xsdom))
    $dom = $proc->transformToDoc($dom);
  else
    return false;
  return true;
}


/**
 * Transforma por Identity Transform e acrescenta algo.
 */
function domXsltProc_idT(&$dom,$TEMPLATE_ADD) {
$xslt = <<<EndOfXSLT
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:strip-space elements="*" />
  <xsl:output indent="yes" />
  <xsl:template match="@*|node()" name="identity">
    <xsl:copy><xsl:apply-templates select="@*|node()"/></xsl:copy>
  </xsl:template>
  $TEMPLATE_ADD
</xsl:stylesheet>
EndOfXSLT;
return domXsltProc($dom,$xslt);
}


/**
 * Group tags with same attribute,
 * @see https://stackoverflow.com/a/18312193/287948
 */
function groupTags_xs(&$dom, $attName, $newTag='fold',$attDel=false) {
$xslt = <<<EndOfXSLT
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:strip-space elements="*" />
  <xsl:output indent="yes" />
  <xsl:key name="elementsByGr" match="*[@attName_place]" use="@attName_place" />

  <xsl:template match="@*|node()" name="identity">
    <xsl:copy><xsl:apply-templates select="@*|node()"/></xsl:copy>
  </xsl:template>

  <xsl:template match="@attName_place" priority="1"></xsl:template><!-- del -->

  <xsl:template match="*[@attName_place][generate-id() = generate-id(key('elementsByGr', @attName_place)[1])]" priority="2">
      <foldTag_place class="art" id="{@attName_place}">
        <xsl:for-each select="key('elementsByGr', @attName_place)">
          <xsl:call-template name="identity" />
        </xsl:for-each>
      </foldTag_place>
  </xsl:template>

  <xsl:template match="*[@attName_place]" priority="1" />
</xsl:stylesheet>
EndOfXSLT;
  $xslt = str_replace(['attName_place','foldTag_place'], [$attName,$newTag], $xslt);
  return domXsltProc($dom,$xslt);
}

?>
