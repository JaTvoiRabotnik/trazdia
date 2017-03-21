import requests

class Journal():

    numero_de_secoes = 0
    por_data = True

    def __init__(self, date, folder, monitor):
        self.date = date
        self.folder = folder
        self.has_journal = True
        self.ocorrencias = {}
        self.tam_secoes = []

        for i in range(self.numero_de_secoes):
            self.tam_secoes.append(-1)



    def baixar_pagina(self, num_secao, num_pagina, data, nome_arquivo):
        pass


    def obter_num_paginas_secao(self, num_secao, data, nome_arquivo):
        pass


    # Obtem informações sobre o jornal
    def obter_info(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            self.tam_secoes[num_secao - 1] = \
                self.obter_num_paginas_secao(num_secao, self.date)


    # Baixa o jornal
    def baixar(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):
                self.baixar_pagina(num_secao, num_pagina, self.date, nome)


    # Executa as operações necessárias para baixar e processar um jornal
    def executar(self):
        self.obter_info()
        self.baixar()
        return self.ocorrencias


###############################################################################
class Diario_da_Justica(Journal):

    nome = "Diario_da_Justiça"
    numero_de_secoes = 1

    # Baixa uma página de uma seção de uma data de jornal e coloca em uma pasta
    def baixar_pagina(self, num_secao, num_pagina, data, nome_arquivo):
        dados_jornal = "jornal=" + "126" + "&pagina=" + str(num_pagina)\
                        + "&data=" + data

        # Essa é a página que deve ser baixada para conseguir os cookies
        # para depois baixar o pdf desejado
        pagina_referencia = "http://www.in.gov.br/imprensa/visualiza/index.jsp?"\
                        + dados_jornal

        referencia = request.get(pagina_referencia)

        # Essa é a página com o pdf desejado
        pagina_jornal = "http://www.in.gov.br/imprensa/servlet/INPDFViewer?"\
                        + dados_jornal + "&captchafield=firistAccess"

        resultado = request.get(pagina_jornal, cookies = referencia.cookies)
        return resultado.content


    def obter_num_paginas_secao(self, num_secao, data):
        dados_jornal = "jornal=" + "126" + "&pagina=1&data=" + data

        # Página que tem o número de páginas da seção
        pagina_referencia = \
            "http://www.in.gov.br/imprensa/visualiza/index.jsp?" + dados_jornal

        referencia = request.get(pagina_referencia)
        texto = referencia.text

        # Extrai do arquivo baixado a parte q fala sobre o número de páginas
        x1, x2, x3 = texto.partition("totalArquivos=")

        if x3:
            num_paginas_secao, x4, x5 = x3.partition('"')
        else:
            num_paginas_secao = 0

        return int(num_paginas_secao)


###############################################################################
class Diario_Justica_do_MT(Journal):

    nome = "Diario_Justica_do_MT"
    numero_de_secoes = 1
    por_data = False

    # Baixa uma página de uma seção de uma data de jornal e coloca em uma pasta
    def baixar_pagina(self, num_secao, num_pagina, data, nome_arquivo):

        edicao = data
        ano = 2007

        baixou = False

        while not baixou:
            pagina_jornal = 'http://dje.tj.mt.gov.br/PDFDJE/'\
                            + str(edicao) + '-' + str(ano) + '.pdf'

            resultado = request(pagina_jornal)

            out, err = comandar(comando)

            # SO FUNCIONA PARA ANO <= 2020 =P (BUG DO VINTENIO)
            # Como o mundo acaba em 2012, da nada nao
            if (resultado.status_code ==  404) and (ano <= 2020):
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

    # Baixa uma página de uma seção de uma data de jornal e coloca em uma pasta
    def baixar_pagina(self, num_secao, num_pagina, data, nome_arquivo):
        edicao = data
        pagina_jornal = "http://www.iomat.mt.gov.br/ler_pdf.php?download=ok&edi_id=" + str(edicao) + "&page=0"
        resultado = request.get(pagina_jornal)
        return resultado.content


###############################################################################
class Diario_Oficial_SP(Journal):

    nome = "Diario_Oficial_SP"
    numero_de_secoes = 2

    secoes = ["exec1", "exec2"]
    meses = ["Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho", "Julho",
            "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    # Baixa uma página de uma seção de uma data de jornal e coloca em uma pasta
    def baixar_pagina(self, num_secao, num_pagina, data, nome_arquivo):

        # Converte o número da seção para um dos nomes das seções
        secao = self.secoes[num_secao - 1]

        dia, mes, ano = data.split("/")
        mes = self.meses[int(mes) - 1]

        pagina_jornal = \
            'http://diariooficial.imprensaoficial.com.br/doflash/prototipo/'\
            + ano + '/' + mes + '/' + dia + '/' + secao + '/pdf/pg_'\
            + str(num_pagina).zfill(4) + '.pdf'

        comando = ['wget', '-nc', '--output-document=' + nome_arquivo,
                    pagina_jornal]

        comandar(comando)

    def obter_num_paginas_secao(self, num_secao, data):

        dia, mes, ano = data.split("/")
        pagina_referencia = \
            "http://diariooficial.imprensaoficial.com.br/nav_v4/header.asp?txtData="\
            + data + "&cad=" + str(num_secao + 3) + "&cedic=" + ano + mes + dia\
            + "&pg=1&acao=&edicao=&secao="

        comando = ['wget',
                '--output-document=' + os.path.join(self.pasta, 'refer.html'),
                pagina_referencia]
        comandar(comando)

        arq = open(os.path.join(self.pasta, 'refer.html'))
        texto = arq.read()
        arq.close()
        os.remove(os.path.join(self.pasta, 'refer.html'))

        x1, x2, x3 = texto.partition('<span class="tx_10 tx_bold">I de ')

        if x3:
            num_paginas_secao, x4, x5 = x3.partition('<')
        else:
            num_paginas_secao = -4

        return int(num_paginas_secao) + 4


###############################################################################
class Diario_Oficial_Uniao(Journal):

    nome = "Diario_Oficial_Uniao"
    numero_de_secoes = 3

    # Baixa uma página de uma seção de uma data de jornal e coloca em uma pasta
    def baixar_pagina(self, num_secao, num_pagina, data, nome_arquivo):
        dados_jornal = "jornal=" + str(num_secao) + "&pagina=" + str(num_pagina)\
                        + "&data=" + data

        ## Essa é a página que deve ser baixada para conseguir os cookies
        ## para depois baixar o pdf desejado
        #pagina_referencia = \
        #    "http://www.in.gov.br/imprensa/visualiza/index.jsp?" + dados_jornal
        #
        #comando = ["wget", '--output-document='\
        #            + os.path.join(self.pasta, 'refer.html'), '--cookies=on',
        #            '--keep-session-cookies', '--save-cookies=cookies.txt',
        #            pagina_referencia]
        #
        ## Baixa a página para conseguir os cookies
        #comandar(comando)
        #
        #os.remove(os.path.join(self.pasta, 'refer.html'))

        # Essa é a página com o pdf desejado
        pagina_jornal = "http://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?"\
                        + dados_jornal + "&captchafield=firistAccess"

        #comando = ['wget', '-nc', '--output-document=' + nome_arquivo,
        #            '--referer="' + pagina_referencia, '--cookies=on',
        #            "--load-cookies=cookies.txt", "--keep-session-cookies",
        #            "--save-cookies=cookies.txt", pagina_jornal]

        comando = ['wget', '-nc', '--output-document=' + nome_arquivo,
                    pagina_jornal]

        # Baixa o PDF
        comandar(comando)

    def obter_num_paginas_secao(self, num_secao, data):
        dados_jornal = "jornal=" + str(num_secao) + "&pagina=1&data=" + data

        # Página que tem o número de páginas da seção
        pagina_referencia = \
            "http://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?" + dados_jornal

        comando = ["wget", '--output-document='\
                + os.path.join(self.pasta, 'refer.html'), pagina_referencia]
        print comando

        # Baixa a página
        comandar(comando)

        arq = open(os.path.join(self.pasta, 'refer.html'))
        texto = arq.read()
        arq.close()
        os.remove(os.path.join(self.pasta, 'refer.html'))

        # Extrai do arquivo baixado a parte q fala sobre o número de páginas
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

    # Baixa uma página de uma seção de uma data de jornal e coloca em uma pasta
    def baixar_pagina(self, num_secao, num_pagina, data, nome_arquivo):
        dados_jornal = "jornal=" + "20" + "&pagina=" + str(num_pagina)\
                        + "&data=" + data

        # Essa é a página que deve ser baixada para conseguir os cookies
        # para depois baixar o pdf desejado
        pagina_referencia = \
            "http://www.in.gov.br/imprensa/visualiza/index.jsp?" + dados_jornal

        comando = ["wget", '--output-document='\
                    + os.path.join(self.pasta, 'refer.html'), '--cookies=on',
                    '--keep-session-cookies', '--save-cookies=cookies.txt',
                    pagina_referencia]

        # Baixa a página para conseguir os cookies
        comandar(comando)

        os.remove(os.path.join(self.pasta, 'refer.html'))

        # Essa é a página com o pdf desejado
        pagina_jornal = "http://www.in.gov.br/imprensa/servlet/INPDFViewer?"\
                        + dados_jornal + "&captchafield=firistAccess"

        comando = ['wget', '-nc', '--output-document=' + nome_arquivo,
                    '--referer="' + pagina_referencia, '--cookies=on',
                    "--load-cookies=cookies.txt", "--keep-session-cookies",
                    "--save-cookies=cookies.txt", pagina_jornal]

        # Baixa o PDF
        comandar(comando)

    def obter_num_paginas_secao(self, num_secao, data):
        dados_jornal = "jornal=" + "20" + "&pagina=1&data=" + data

        # Página que tem o número de páginas da seção
        pagina_referencia = \
            "http://www.in.gov.br/imprensa/visualiza/index.jsp?" + dados_jornal

        comando = ["wget", '--output-document='\
                + os.path.join(self.pasta, 'refer.html'), pagina_referencia]

        # Baixa a página
        comandar(comando)

        arq = open(os.path.join(self.pasta, 'refer.html'))
        texto = arq.read()
        arq.close()
        os.remove(os.path.join(self.pasta, 'refer.html'))

        # Extrai do arquivo baixado a parte q fala sobre o número de páginas
        x1, x2, x3 = texto.partition("totalArquivos=")

        if x3:
            num_paginas_secao, x4, x5 = x3.partition('"')
        else:
            num_paginas_secao = 0

        return int(num_paginas_secao)
