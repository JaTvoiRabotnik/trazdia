import requests
import logging
from bs4 import BeautifulSoup
import json


class Journal():
    numero_de_secoes = 0
    por_data = True

    def __init__(self, date):
        self.date = date
        self.has_journal = True
        self.ocorrencias = {}
        self.tam_secoes = []

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
    def return_index(self, section):
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

    # Baixa uma pagina de uma secao de uma data de jornal e coloca em uma pasta
    def baixar_pagina(self, num_secao, num_pagina, data):
        logger = logging.getLogger('trazdia')
        # Converte o numero da secao para um dos nomes das secoes
        secao = self.section[num_secao - 1]

        ano = data[0:4]
        mes = data[4:6]
        dia = data[6:8]
        mes = self.get_month_PT(int(mes))

        pagina_jornal = \
            'http://diariooficial.imprensaoficial.com.br/doflash/prototipo/' \
            + ano + '/' + mes + '/' + dia + '/' + secao + '/pdf/pg_' \
            + str(num_pagina).zfill(4) + '.pdf'

        resultado = requests.get(pagina_jornal)
        logger.info(pagina_jornal)
        return resultado.content

    def obter_num_paginas_secao(self, num_secao, data):
        logger = logging.getLogger('trazdia')
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


    def translate_to_json(self, content, section):
        soup = BeautifulSoup(content, "xml", from_encoding="iso-8859-1")
        section_tag = soup.CADERNO
        offset = int(section_tag['pageditoriais'])
        dict_output = {'journal': self.nome,
                       'section': section,
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


    def return_index(self, section):
        logger = logging.getLogger('trazdia')

        year = self.date[0:4]
        month = self.get_month_PT(int(self.date[4:6]))
        day = self.date[6:8]

        self.base_link = 'http://diariooficial.imprensaoficial.com.br/doflash/prototipo/' \
            + year + '/' + month + '/' + day + '/' + section
        journal_index = self.base_link + '/xml/' + str(self.date) + '.xml'

        result = requests.get(journal_index)
        logger.info(journal_index)
        json_result = self.translate_to_json(result.content, section)
        return json_result


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
