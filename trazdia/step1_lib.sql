--
-- Module of commom basic functions.
-- This schema can be dropped (DROP SCHEMA tlib CASCADE) without direct side effect.
--
-- Copyright by ppkrauss@gmail.com 2016, MIT license.
--
-- NOTES: usual user adaptations occurs in jrpc.*(), normalizeterm() and score() functions.
-- To rebuild system with functional changes (preserving data), use
--     psql -h localhost -U postgres postgres < step1_lib.sql
--

DROP SCHEMA IF EXISTS lib CASCADE;
DROP SCHEMA IF EXISTS jrpc CASCADE;
DROP SCHEMA IF EXISTS tlib CASCADE;
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch; -- for metaphone() and levenshtein()

CREATE SCHEMA lib;  -- general commom library.
CREATE SCHEMA jrpc; -- lib for JSON-RPC utility, see http://www.jsonrpc.org/specification
CREATE SCHEMA tlib; -- lib for all Terminological schemas.


--- --- ---
-- Namespace functions

CREATE FUNCTION tlib.nsmask(
	--
	-- Build mask for namespaces (ns). See nsid at term1.ns. Also builds nsid from nscount by array[nscount].
	-- Ex. SELECT  tlib.nsmask(array[2,3,4])::bit(32);
	-- Range 1..32.
	--
	int[]  -- List of namespaces (nscount of each ns)
) RETURNS int AS $f$
	SELECT sum( (1::bit(32) << (x-1) )::int )::int
	FROM unnest($1) t(x)
	WHERE x>0 AND x<=32;
$f$ LANGUAGE SQL IMMUTABLE;


CREATE FUNCTION tlib.lang2regconf(text) RETURNS regconfig AS $f$
	--
	-- Convention to convert iso2 into regconfig for indexing words. See kx_regconf.
	-- See SELECT * FROM pg_catalog.pg_ts_config
	SELECT  (('{"pt":"portuguese","en":"english","es":"spanish","":"simple","  ":"simple","fr":"french","it":"italian","de":"german","nl":"dutch"}'::jsonb)->>$1)::regconfig
$f$ LANGUAGE SQL IMMUTABLE;



-- PRIVATE FUNCTIONS --

CREATE FUNCTION jrpc.jparams(
	--
	-- Converts JSONB or JSON-RPC request (with reserved word "params") into JSOB+DEFAULTS.
	--
	-- Ex.SELECT tlib.jparams('{"x":12}'::jsonb, '{"x":5,"y":34}'::jsonb)
	--
	JSONB,			-- the input request (direct or at "params" property)
	JSONB DEFAULT NULL	-- (optional) default values.
) RETURNS JSONB AS $f$
	SELECT CASE WHEN $2 IS NULL THEN jo ELSE $2 || jo END
	FROM (SELECT CASE WHEN $1->'params' IS NULL THEN $1 ELSE $1->'params' END AS jo) t;
$f$ LANGUAGE SQL IMMUTABLE;


CREATE FUNCTION lib.unpack(
	--
	-- Remove a sub-object and merge its contents.
	-- Ex. SELECT tlib.unpack('{"x":12,"sub":{"y":34}}'::jsonb,'sub');
	--
	JSONB,	-- full object
	text	-- pack name
) RETURNS JSONB AS $f$
	SELECT ($1-$2)::JSONB || ($1->>$2)::JSONB;
$f$ LANGUAGE SQL IMMUTABLE;


CREATE FUNCTION jrpc.error(
	--
	-- Converts input into a JSON RPC error-object.
	--
	-- Ex. SELECT jrpc.error('ops error',123,'i2');
	--
	text,         		-- 1. error message
	int DEFAULT -1,  	-- 2. error code
	text DEFAULT NULL	-- 3. (optional) calling id (when NULL it is assumed to be a notification)
) RETURNS JSONB AS $f$
	SELECT jsonb_build_object(
		'error',jsonb_build_object('code',$2, 'message', $1),
		'id',$3,
		'jsonrpc','2.0'
	);
$f$ LANGUAGE SQL IMMUTABLE;


CREATE FUNCTION jrpc.ret(
	--
	-- Converts input into a JSON RPC result scalar or single object.
	--
	-- Ex. SELECT jrpc.ret(123,'i1');      SELECT jrpc.ret('123'::text,'i1');
	--     SELECT jrpc.ret(123,'i1','X');  SELECT jrpc.ret(array['123']);
	--     SELECT jrpc.ret(array[1,2,3],'i1','X');
	-- Other standars, see Elasticsearch output at http://wayta.scielo.org/
	--
	anyelement,		-- 1. the result value
	text DEFAULT NULL, 	-- 2. (optional) calling id (when NULL it is assumed to be a notification)
	text DEFAULT NULL 	-- 3. (optional) the result sub-object name
) RETURNS JSONB AS $f$
	SELECT jsonb_build_object(
		'result', CASE WHEN $3 IS NULL THEN to_jsonb($1) ELSE jsonb_build_object($3,$1) END,
		'id',$2,
		'jsonrpc','2.0'
		);
$f$ LANGUAGE SQL IMMUTABLE;

CREATE FUNCTION jrpc.ret(
	--
	-- jrpc_ret() overload to convert to a dictionary (object with many names).
	--
	-- Ex. SELECT jrpc.ret(array['a'],array['123']);
	--     SELECT jrpc.ret(array['a','b','c'],array[1,2,3],'i1');
	--
	text[],		  	-- 1. the result keys
	anyarray, 	  	-- 2. the result values
	text DEFAULT NULL 	-- 3. (optional) calling id (when NULL it is assumed to be a notification)
) RETURNS JSONB AS $f$
	SELECT jsonb_build_object(
		'result', (SELECT jsonb_object_agg(k,v) FROM (SELECT unnest($1), unnest($2)) as t(k,v)),
		'id',$3,
		'jsonrpc',' 2.0'
		);
$f$ LANGUAGE SQL IMMUTABLE;


CREATE FUNCTION jrpc.ret(
	--
	-- Adds standard tlib structure to RPC result.
	-- See https://github.com/ppKrauss/sql-term/issues/5
	--
	JSON,      		-- 1. full result (all items) before to pack
	int,       		-- 2. items COUNT of the full result
	text DEFAULT NULL, 	-- 3. id of callback
	text DEFAULT NULL, 	-- 4. sc_func or null for use 5
	JSONB DEFAULT NULL      -- 5. json with sc_func and other data, instead of 4.
) RETURNS JSONB AS $f$
	SELECT jsonb_build_object(
		'result', CASE
			WHEN $5 IS NOT NULL THEN jsonb_build_object('items',$1, 'count',$2) || $5
			WHEN $4 IS NULL THEN jsonb_build_object('items',$1, 'count',$2)
			ELSE jsonb_build_object('items',$1, 'count',$2, 'sc_func',$4)
			END,
		'id',$3,
		'jsonrpc',' 2.0'
	);
$f$ LANGUAGE SQL IMMUTABLE;


-- -- -- -- --
-- PRIVATE and inter-shema

CREATE FUNCTION tlib.nsget_lang(int,boolean DEFAULT false) RETURNS char(2) AS $f$
	--
	-- Get lang from a namespace.
	-- Dynamic query, low performance (!). Use it only for caches and inserts.
	--
        DECLARE
	  x char(2);
	BEGIN
	  EXECUTE format(
	    'SELECT lang FROM tstore.ns WHERE %L',
	    CASE WHEN $2 THEN 'nscount='||$1 ELSE 'nsid='||$1 END
	  ) INTO x;
	  RETURN x;
	END;
$f$ LANGUAGE PLpgSQL IMMUTABLE;


-- -- -- -- -- -- -- --
--- PUBLIC FUNCTIONS

CREATE FUNCTION tlib.normalizeterm(
	--
	-- Converts string into standard sequence of lower-case words.
	--
	text,       		-- 1. input string (many words separed by spaces or punctuation)
	text DEFAULT ' ', 	-- 2. output separator
	int DEFAULT 255,	-- 3. max lenght of the result (system limit)
	p_sep2 text DEFAULT ' , ' -- 4. output separator between terms
) RETURNS text AS $f$
  SELECT  substring(
	LOWER(TRIM( regexp_replace(  -- for review: regex(regex()) for ` , , ` remove
		trim(regexp_replace($1,E'[\\n\\r \\+/,;:\\(\\)\\{\\}\\[\\]="\\s ]*[\\+/,;:\\(\\)\\{\\}\\[\\]="]+[\\+/,;:\\(\\)\\{\\}\\[\\]="\\s ]*|[\\s ]+[–\\-][\\s ]+',
				   p_sep2, 'g'),' ,'),   -- s*ps*|s-s
		E'[\\s ;\\|"]+[\\.\'][\\s ;\\|"]+|[\\s ;\\|"]+',    -- s.s|s
		$2,
		'g'
	), $2 )),
  1,$3
  );
$f$ LANGUAGE SQL IMMUTABLE;


CREATE FUNCTION tlib.multimetaphone(
	--
	-- Converts string (spaced words) into standard sequence of metaphones.
	-- Copied from tlib.normalizeterm(). Check optimization with
	--
	text,       		-- 1. input string (many words separed by spaces or punctuation)
	int DEFAULT 6, 		-- 2. metaphone length
	text DEFAULT ' ', 	-- 3. separator
	int DEFAULT 255		-- 4. max lenght of the result (system limit)
) RETURNS text AS $f$
	SELECT 	 substring(  trim( string_agg(metaphone(w,$2),$3) ,$3),  1,$4)
	FROM regexp_split_to_table($1, E'[\\+/,;:\\(\\)\\{\\}\\[\\]="\\s\\|]+[\\.\'][\\+/,;:\\(\\)\\{\\}\\[\\]="\\s\\|]+|[\\+/,;:\\(\\)\\{\\}\\[\\]="\\s\\|]+') AS t(w);  -- s.s|s  -- já contemplado pelo espaço o \s[–\\-]\s
$f$ LANGUAGE SQL IMMUTABLE;





