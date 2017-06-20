
DROP SCHEMA IF EXISTS oficial CASCADE;
CREATE SCHEMA oficial;

CREATE TABLE oficial.ns(
  --
  -- Namespaces
  --
  nscount smallserial NOT NULL,  -- only few namespaces (32 for int id).
  nsid  int PRIMARY KEY, -- automatic cache of tlib.nsmask(nscount), see trigger
  label varchar(20) NOT NULL,
  description varchar(255) NOT NULL,
  lang char(2) NOT NULL DEFAULT 'pt', -- language of term, OR regconfig with language. Ignore it for codes (ex. ISO country).
  is_canonical boolean NOT NULL DEFAULT true,  -- flag to "canonical namespace" (not a synonymous set)
  info JSONB,     -- any other metadata.  group_unique=true or false
  created date DEFAULT now(),
  UNIQUE(nscount),
  UNIQUE(label),
  CHECK(tlib.lang2regconf(lang) IS NOT NULL), -- see tstore.input_ns()
  CHECK(nscount <= 32),  -- 32 when nsid is integer, 64 when bigint.
  CHECK(tlib.nsmask(array[nscount])=nsid) -- null or check
);


CREATE TABLE oficial.lexnames(
  --
  -- UrnLex-like formated names, used in all URNs. Only canonic names. 
  --
  id serial PRIMARY KEY,
  fk_ns int NOT NULL REFERENCES oficial.ns(nsid),
  lexname  text NOT NULL, -- main term
  name text,  -- optional, UTF8 with spaces, accents, case sensitive, etc.
  fk_source int[], -- ELEMENT REFERENCES tstore.source(id),
  is_abbrev boolean, -- NULL, use only for full-path abbreviations
  is_suspect boolean NOT NULL DEFAULT false, -- to flag potential bugs.
  created date DEFAULT now(),
  info JSONB,     -- any other metadata.
  kx_tsvector tsvector,  -- cache for to_tsvector
  UNIQUE(fk_ns,lexname)
);

---------
---------

CREATE TABLE oficial.jurisdiction(
  --
  -- UrnLex-like concept of JURISDICTION. 
  --
  id serial PRIMARY KEY,
  lexname  text NOT NULL, -- main term
  name text,  -- optional, UTF8 with spaces, accents, case sensitive, etc.
  abbrev text,  -- optional for most popular "short" name.
  info JSONB,     -- any other metadata.
  UNIQUE(lexname)
);

CREATE TABLE oficial.authority(
  --
  -- UrnLex-like concept of AUTHORITY, for each article (not the issue).
  --
-- falta avaliar como cadastrar autoridade-contratante, ver http://schema.org/GeneralContractor
  id serial PRIMARY KEY,
  lexname  text NOT NULL, -- main term
  kx_parent int REFERENCES oficial.authority(id), -- when not null, check same lexname prefix.
  name text,  -- optional, UTF8 with spaces, accents, case sensitive, etc.
  abbrev text,  -- optional for most popular "short" name.
  info JSONB,     -- any other metadata.
  UNIQUE(lexname)
);

CREATE TABLE oficial.organization(
  --
  -- http://schema.org/Organization
  --
  id serial PRIMARY KEY,
  type text NOT NULL DEFAULT 'editora', -- 'editora', 'contratante' and others, see data model.
  vatID text, -- CNPJ or equivalent
  lexname  text NOT NULL, -- organization's official full-name
  name text,  -- optional, UTF8 with spaces, accents, case sensitive, etc.
  abbrev text,  -- optional for most popular "short" name.
  info JSONB,     -- any other metadata.
  UNIQUE(lexname)
);

CREATE TABLE oficial.PublicationIssue(
  --
  -- Fascículo,  http://schema.org/PublicationIssue
  --
  id serial PRIMARY KEY,
  issueNumber text NOT NULL, -- public ID in the serial, see http://schema.org/issueNumber
  datePublished date NOT NULL, -- see http://schema.org/datePublished
  seq smallint,   -- optional "sequencial in the datePublished"
  kx_oficial_url text NOT NULL,    -- any valid URL to the publication
  info JSONB,     -- any other metadata.
  UNIQUE(issueNumber)
);

