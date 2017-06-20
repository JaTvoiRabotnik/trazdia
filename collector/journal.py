import requests
import logging
#from bs4 import BeautifulSoup
import json
from bs4 import BeautifulSoup


class Journal():
    numero_de_secoes = 0
    por_data = True

    def __init__(self, date):
        self.date = date
        self.has_journal = True
        self.ocorrencias = {}
        self.tam_secoes = []

    # Brings the whole edition for a given date, returns in JSON
    def bring_edition(self):
        pass

    def baixar_pagina(self, num_secao, num_pagina, data):
        pass

    def obter_num_paginas_secao(self, num_secao, data):
        pass

    # Obtem informacoes sobre o jornal
    def obter_info(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            self.tam_secoes[num_secao - 1] = \
                self.obter_num_paginas_secao(num_secao, self.date)

    # Baixa o jornal
    def baixar(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):
                return self.baixar_pagina(num_secao, num_pagina, self.date)

    # Executa as operacoes necessarias para baixar e processar um jornal
    def executar(self):
        self.obter_info()
        return self.baixar()

    # Get JSON with list of links to pages of a given DO
    def return_index(self):
        pass

    def get_month_PT(self, month):
        switcher = {
            1: "Janeiro",
            2: "Fevereiro",
            3: "Marco",
            4: "Abril",
            5: "Maio",
            6: "Junho",
            7: "Julho",
            8: "Agosto",
            9: "Setembro",
            10: "Outubro",
            11: "Novembro",
            12: "Dezembro"
        }
        return switcher.get(month, "nothing")

    def read_hostile_text(self, encoded_text):
        pass


###############################################################################
class Diario_da_Justica(Journal):
    nome = "Diario_da_Justica"
    numero_de_secoes = 1

    # Baixa uma pagina de uma secao de uma data de jornal e coloca em uma pasta
    def baixar_pagina(self, num_secao, num_pagina, data):
        dados_jornal = "jornal=" + "126" + "&pagina=" + str(num_pagina) \
                       + "&data=" + data

        # Essa e a pagina que deve ser baixada para conseguir os cookies
        # para depois baixar o pdf desejado
        pagina_referencia = "http://www.in.gov.br/imprensa/visualiza/index.jsp?" \
                            + dados_jornal

        referencia = requests.get(pagina_referencia)

        # Essa e a pagina com o pdf desejado
        pagina_jornal = "http://www.in.gov.br/imprensa/servlet/INPDFViewer?" \
                        + dados_jornal + "&captchafield=firistAccess"

        resultado = requests.get(pagina_jornal, cookies=referencia.cookies)
        return resultado.content

    def obter_num_paginas_secao(self, num_secao, data):
        dados_jornal = "jornal=" + "126" + "&pagina=1&data=" + data

        # Pagina que tem o numero de paginas da secao
        pagina_referencia = \
            "http://www.in.gov.br/imprensa/visualiza/index.jsp?" + dados_jornal

        referencia = requests.get(pagina_referencia)
        texto = referencia.text
        print(pagina_referencia)

        # Extrai do arquivo baixado a parte q fala sobre o numero de paginas
        x1, x2, x3 = texto.partition("totalArquivos=")

        if x3:
            num_paginas_secao, x4, x5 = x3.partition('"')
        else:
            num_paginas_secao = 0

        print(int(num_paginas_secao))
        return int(num_paginas_secao)


###############################################################################
class Diario_Justica_do_MT(Journal):
    nome = "Diario_Justica_do_MT"
    numero_de_secoes = 1
    por_data = False

    # Baixa uma pagina de uma secao de uma data de jornal e coloca em uma pasta
    def baixar_pagina(self, num_secao, num_pagina, data):

        edicao = data
        ano = 2007

        baixou = False

        while not baixou:
            pagina_jornal = 'http://dje.tj.mt.gov.br/PDFDJE/' \
                            + str(edicao) + '-' + str(ano) + '.pdf'

            resultado = requests(pagina_jornal)

            # SO FUNCIONA PARA ANO <= 2020 =P (BUG DO VINTENIO)
            # Como o mundo acaba em 2012, da nada nao
            if (resultado.status_code == 404) and (ano <= 2020):
                ano += 1
            else:
                baixou = True

        return resultado.content

    def obter_num_paginas_secao(self, num_secao, data):
        return 1


###############################################################################
class Diario_Oficial_do_MT(Diario_Justica_do_MT):
    nome = "Diario_Oficial_do_MT"
    numero_de_secoes = 1
    por_data = False

    # Baixa uma pagina de uma secao de uma data de jornal e coloca em uma pasta
    def baixar_pagina(self, num_secao, num_pagina, data):
        edicao = data
        pagina_jornal = "http://www.iomat.mt.gov.br/ler_pdf.php?download=ok&edi_id=" + str(edicao) + "&page=0"
        resultado = requests.get(pagina_jornal)
        return resultado.content


###############################################################################
class Diario_Oficial_SP(Journal):
    logger = logging.getLogger(__name__)
    nome = "Diario_Oficial_SP"
    base_link = ''
    numero_de_secoes = 2
    section = ''


    # Baixa uma pagina de uma secao de uma data de jornal
    def baixar_pagina(self, num_secao, num_pagina, data):
        logger = logging.getLogger('trazdia')

        ano = data[0:4]
        mes = data[4:6]
        dia = data[6:8]
        mes = self.get_month_PT(int(mes))

        pagina_jornal = \
            'http://diariooficial.imprensaoficial.com.br/doflash/prototipo/' \
            + ano + '/' + mes + '/' + dia + '/' + self.section + '/pdf/pg_' \
            + str(num_pagina).zfill(4) + '.pdf'

        resultado = requests.get(pagina_jornal)
        logger.info(pagina_jornal)
        return resultado.content



    def obter_num_paginas_secao(self, num_secao, data):
        ano = data[0:4]
        mes = data[4:6]
        dia = data[6:8]
        reverse_date = dia + '/' + mes + '/' + ano
        pagina_referencia = \
            "http://diariooficial.imprensaoficial.com.br/nav_v4/header.asp?txtData=" \
            + reverse_date + "&cad=" + str(num_secao + 3) + "&cedic=" + ano + mes + dia \
            + "&pg=1&acao=&edicao=&secao="
        # logger.info(pagina_referencia)
        resultado = requests.get(pagina_referencia)
        texto = resultado.text

        x1, x2, x3 = texto.partition('<span class="tx_10 tx_bold">I de ')

        if x3:
            num_paginas_secao, x4, x5 = x3.partition('<')
        else:
            num_paginas_secao = -4

        return int(num_paginas_secao) + 4



    def link_for_id(self, id):
        return self.base_link + '/pdf/pg_' + str(id).zfill(4) + '.pdf'



    def translate_to_json(self, content):
        soup = BeautifulSoup(content, "xml", from_encoding="iso-8859-1")
        if(soup.TITLE):
            title = soup.TITLE.string
            if(title == 'The page cannot be found'):
                return None
        section_tag = soup.CADERNO
        offset = int(section_tag['pageditoriais'])
        dict_output = {'journal': self.nome,
                       'date': section_tag['ano'] + section_tag['mes'] + section_tag['dia'],
                       'pages': section_tag['paginas'],
                       'editorialpages': section_tag['pageditoriais']}
        group_tags = section_tag.find_all('GRUPO')
        groups = {}
        for group_tag in group_tags:
            subsections = {}
            subsection_tags = group_tag.find_all('SECAO')
            for subsection_tag in subsection_tags:
                id = int(subsection_tag['inicio']) + offset
                subsections[subsection_tag['nome']] = self.link_for_id(id)
            groups[group_tag['nome']] = subsections
        dict_output['groups'] = groups
        return json.dumps(dict_output, sort_keys=True, ensure_ascii=False, indent=4, \
                          separators=(',', ': ')).encode("utf-8")



    def return_index(self):
        logger = logging.getLogger(__name__)
        year = self.date[0:4]
        month = self.get_month_PT(int(self.date[4:6]))
        day = self.date[6:8]

        self.base_link = 'http://diariooficial.imprensaoficial.com.br/doflash/prototipo/' \
            + year + '/' + month + '/' + day + '/' + self.section
        journal_index = self.base_link + '/xml/' + str(self.date) + '.xml'

        result = requests.get(journal_index)
        logger.info(journal_index)
        json_result = self.translate_to_json(result.content)
        return json_result


###############################################################################
class DO_SP_saopaulo_executivo(Diario_Oficial_SP):
    section = 'cidade'
    nome = "Diario Oficial do municipio de Sao Paulo, estado de Sao Paulo, executivo"


###############################################################################
class DO_SP_saopaulo_legislativo(Diario_Oficial_SP):
    section = 'legislativo'
    nome = "Diario Oficial do municipio de Sao Paulo, estado de Sao Paulo, legislativo"


###############################################################################
class DO_SP_executivo(Diario_Oficial_SP):
    section = 'exec1'
    nome = "Diario Oficial do estado de Sao Paulo, executivo"



###############################################################################
###############################################################################
class Diario_Oficial_RJ(Journal):
    logger = logging.getLogger(__name__)
    nome = "Diario_Oficial_RJ"
    base_link = ''
    numero_de_secoes = 2


    # Decode an input and return utf-8 #
    def read_hostile_text(self, encoded_text):
        logger = logging.getLogger('trazdia')
        encodings = [
            'latin_1',
            'utf_16',
            'cp1250',
            'iso-8859-1',
        ]
        for encoding in encodings:
            try:
                decoded_text = encoded_text.decode(encoding)
                return decoded_text.encode('utf-8')
            except UnicodeDecodeError:
                logger.info(encoding, 'did not work. Trying another encoding for', encoded_text)
        logger.error('Could not decode', encoded_text)
        return None


    def getedition(self, ediParam):

        HTMPARAM    = 'http://doweb.rio.rj.gov.br/do/navegadorhtml/' \
                      'load_tree.php?edi_id={0}'
        LNKPARAM    = 'http://doweb.rio.rj.gov.br/do/navegadorhtml/' \
                      'mostrar.htm?id={0}&edi_id={1}'

        # Keep a dictionary of folders and documents
        folders     = []
        materias    = []

        # http response
        response    = requests.get(HTMPARAM.format(ediParam))
        respList    = response.content.split('\n')
        #respList    = open('3168_response.txt')

        for row in respList:
            # Index of a folder
            if 'gFld(' in row:
                fldKey      = row[0:row.find(' = ')]
                fldVal      = self.read_hostile_text(row[row.find('gFld(')+5:row.find(');')] \
                              .split(', ')[0][1:-1])
                folders.append(dict(fldKey=fldKey, fldVal=fldVal))
            # Index of a document
            elif 'addChild(' in row:
                materia     = row[row.find('([')+2:row.find('])')].split('", "')
                matId       = materia[1][materia[1].find('?id=')+4: \
                              materia[1].find('&edi')]
                # TODO CAREFUL: we might have a hidden comma here, which will cause havoc on the conversion to CSV
                matTitulo   = self.read_hostile_text(materia[0][1:])
                matPaiKey   = row[0:row.find('.addChild')]
                materias.append(dict(matPathKey=[matPaiKey],
                                     matPathVal='',
                                     matTitulo=matTitulo,
                                     matId=matId,
                                     matEdi=ediParam,
                                     matLink=LNKPARAM.format(matId,ediParam)))
            elif 'addChildren(' in row:
                paiKey      = row[0:row.find('.addChildren')]
                childVals   = row[row.find('([')+2:row.find('])')].split(',')
                for val in childVals:
                    for materia in materias:
                        if materia['matPathKey'][0] == val:
                            materia['matPathKey'].insert(0, paiKey)

        for materia in materias:
            for n,i in enumerate(materia['matPathKey']):
                for keyVal in folders:
                    if keyVal['fldKey'] == i:
                        materia['matPathVal'] += keyVal['fldVal']
                        if n < len(materia['matPathKey']) - 1:
                            materia['matPathVal'] += ' | '
        return materias


    def get_edition_id_from_date(self, date):
        with open('collector/rio_dictionary.json') as data_file:
            edition_dict = json.load(data_file)
            return edition_dict[date]


    # Brings the whole edition for a given date, returns in JSON
    def bring_edition(self):
        logger = logging.getLogger('trazdia')

        ediParams = self.get_edition_id_from_date(self.date)
        raw_docs = []
        for edition in ediParams:
            raw_docs.append(self.getedition(edition))

        # TODO enrich output with more details of section, subsection, etc.
        dict_output = {'journal': self.nome,
                       'date': self.date}
        documents = []
        for raw_doc in raw_docs[0]:
            response    = requests.get(raw_doc['matLink'])
            rawtext     = response.content
            # We use BeautifulSoup to convert to utf-8
            soup        = BeautifulSoup(rawtext)
            soup.head.extract()
            if soup.style is None:
                print(soup.get_text())
                sys.exit()
            else:
                soup.style.extract()
                soup.style.extract()
            raw_html = soup.prettify()
            documents.append(raw_html)
            #documents.append(rawtext)
        dict_output['documents'] = documents

        return json.dumps(dict_output, sort_keys=True, ensure_ascii=False, indent=4, \
                          separators=(',', ': '))


###############################################################################
class Diario_Oficial_Uniao(Journal):
    nome = "Diario_Oficial_Uniao"
    numero_de_secoes = 3

    # Baixa uma pagina de uma secao de uma data de jornal e coloca em uma pasta
    def baixar_pagina(self, num_secao, num_pagina, data):
        dados_jornal = "jornal=" + str(num_secao) + "&pagina=" + str(num_pagina) \
                       + "&data=" + data

        # Essa e a pagina com o pdf desejado
        pagina_jornal = "http://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?" \
                        + dados_jornal + "&captchafield=firistAccess"

        resultado = requests.get(pagina_jornal)

        return resultado.content

    def obter_num_paginas_secao(self, num_secao, data):
        dados_jornal = "jornal=" + str(num_secao) + "&pagina=1&data=" + data

        # Pagina que tem o numero de paginas da secao
        pagina_referencia = \
            "http://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?" + dados_jornal

        resultado = requests(pagina_referencia)

        texto = resultado.text

        # Extrai do arquivo baixado a parte q fala sobre o numero de paginas
        x1, x2, x3 = texto.partition("totalArquivos=")

        if x3:
            num_paginas_secao, x4, x5 = x3.partition('"')
        else:
            num_paginas_secao = 0

        return int(num_paginas_secao)


###############################################################################
class Diario_TRF(Journal):
    nome = "Diario_TRF"
    numero_de_secoes = 1

    # Baixa uma pagina de uma secao de uma data de jornal e coloca em uma pasta
    def baixar_pagina(self, num_secao, num_pagina, data):
        dados_jornal = "jornal=" + "20" + "&pagina=" + str(num_pagina) \
                       + "&data=" + data

        # Essa e a pagina que deve ser baixada para conseguir os cookies
        # para depois baixar o pdf desejado
        pagina_referencia = \
            "http://www.in.gov.br/imprensa/visualiza/index.jsp?" + dados_jornal

        referencia = requests.get(pagina_referencia)

        # Essa e a pagina com o pdf desejado
        pagina_jornal = "http://www.in.gov.br/imprensa/servlet/INPDFViewer?" \
                        + dados_jornal + "&captchafield=firistAccess"

        resultado = requests.get(pagina_jornal, cookies=referencia.cookies)

        return resultado.content

    def obter_num_paginas_secao(self, num_secao, data):
        dados_jornal = "jornal=" + "20" + "&pagina=1&data=" + data

        # Pagina que tem o numero de paginas da secao
        pagina_referencia = \
            "http://www.in.gov.br/imprensa/visualiza/index.jsp?" + dados_jornal

        resultado = requests.get(pagina_referencia)

        texto = resultado.text

        # Extrai do arquivo baixado a parte q fala sobre o numero de paginas
        x1, x2, x3 = texto.partition("totalArquivos=")

        if x3:
            num_paginas_secao, x4, x5 = x3.partition('"')
        else:
            num_paginas_secao = 0

        return int(num_paginas_secao)
