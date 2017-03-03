class Journal():

    numero_de_secoes = 0
    por_data = True

    def __init__(self, date, folder, monitor):
        self.date = date
        self.folder = folder
        self.has_journal = True

        self.ocorrencias = {}

        self.tam_secoes = []

        self.monitor = monitor

        for i in range(self.numero_de_secoes):
            self.tam_secoes.append(-1)

        #if not verificar_se_dia_com_jornal(self.data):
            #self.teve_jornal = False
            #print "Parece q esse dia não deveria ter tido jornal..."

    def baixar_pagina(self, num_secao, num_pagina, data, nome_arquivo):
        pass

    def obter_num_paginas_secao(self, num_secao, data, nome_arquivo):
        pass

    # Obtem a data e os tamanhos das seções do jornal na pasta
    def ler_dados(self):
        arq = open(os.path.join(self.folder, "dados"), "r")
        texto = arq.read()
        arq.close()
        texto = texto.split()
        date = texto.pop(0)
        for linha in texto:
            self.tam_secoes[int(linha)] = int(linha)

    # Salva um arquivo com os tamanhos das seções
    def salvar_dados(self):
        arq = open(os.path.join(self.folder, "dados"), "w")
        arq.write(self.date)
        for i in self.tam_secoes:
            arq.write(" " + str(i))
        arq.close()

    # Obtem informações sobre o jornal
    def obter_info(self):
        for num_secao in range(1, self.numero_de_secoes + 1):

            if self.monitor.para:
                    return None

            self.tam_secoes[num_secao - 1] = \
                self.obter_num_paginas_secao(num_secao, self.date)

    # Baixa o jornal
    def baixar(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):

                if self.monitor.para:
                    return None

                nome = montar_nome_arquivo(self.folder, self.date, num_secao,
                                           num_pagina, 'pdf')

                # Isso deve fazer com que PDFs que não foram terminados de
                #baixar sejam deletados
                try:
                    arq = open(os.path.join(self.folder, "baixando"), "r")
                    nome2 = arq.read()
                    os.remove(nome2)
                    arq.close()
                    os.remove(os.path.join(self.folder, "baixando"))
                except:
                    print "Erro remover nao terminado"
                    pass

                arq = open(os.path.join(self.folder, "baixando"), "w")
                arq.write(nome)
                arq.close()

                self.baixar_pagina(num_secao, num_pagina, self.date, nome)

                os.remove(os.path.join(self.folder, "baixando"))


    # Extrai os textos do jornal e deixa na mesma pasta
    def extrair_textos(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):

                if self.monitor.para:
                    return None

                nome = montar_nome_arquivo(self.folder, self.date,
                                            num_secao, num_pagina, "pdf")
                documentar(nome)
                converter_pdf(nome)

    # Aplica o buscador no texto
    def analisar(self, buscador):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):

                if self.monitor.para:
                    return None

                nome = montar_nome_arquivo(self.folder, self.date,
                                           num_secao, num_pagina, "txt")
                documentar(nome)

                try:
                    arq = open(nome)
                    texto = arq.read()
                    arq.close()

                    ocorrencias_na_pagina = buscador.analisar(texto)

                    if len(ocorrencias_na_pagina) != 0:
                        self.ocorrencias[(num_secao, num_pagina)] = \
                            ocorrencias_na_pagina
                except:
                    documentar("----->Erro ao tentar abrir esse arquivo!<-----")

    # Remove os pdfs que não tiverem nenhuma ocorrencia na busca
    def remover_pdfs_nao_usados(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):

                if self.monitor.para:
                    return None

                if not self.ocorrencias.get((num_secao, num_pagina)):
                    os.remove(montar_nome_arquivo(self.folder, self.date,
                                                   num_secao, num_pagina, "pdf"))

    # Remove os txt que não tiverem nenhuma ocorrencia na busca
    def remover_txts_nao_usados(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):

                if self.monitor.para:
                    return None

                if not self.ocorrencias.get((num_secao, num_pagina)):
                    os.remove(montar_nome_arquivo(self.folder, self.date,
                                                   num_secao, num_pagina, "txt"))

    # Remove todos os arquivos do jornal
    def remover(self):
        for arq in os.listdir(self.folder):
            os.remove(os.path.join(self.folder, arq))

    # Executa as operações necessárias para baixar e processar um jornal
    def executar(self, buscador):
        documentar("Obtendo Dados")
        self.obter_info()
        if self.monitor.para:
            return []
        documentar("Baixando PDFs")
        self.baixar()
        if self.monitor.para:
            return []
        documentar("Extraindo Textos")
        self.extrair_textos()
        if self.monitor.para:
            return []
        documentar("Analisando Textos")
        self.analisar(buscador)
        if self.monitor.para:
            return []
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
        dados_jornal = "jornal=" + "126" + "&pagina=1&data=" + data

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

            comando = ['wget', '-nc', '--output-document=' + nome_arquivo,
                        pagina_jornal]

            out, err = comandar(comando)

            # SO FUNCIONA PARA ANO <= 2020 =P (BUG DO VINTENIO)
            # Como o mundo acaba em 2012, da nada nao
            if out.find("ERRO 404: Not Found") != -1 and ano <= 2020:
                ano += 1
                try:
                    os.remove(nome_arquivo)
                except:
                    pass
            else:
                baixou = True

    def obter_num_paginas_secao(self, num_secao, data):
        return 1

    # Extrai os textos do jornal e deixa na mesma pasta
    def extrair_textos(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):

                if self.monitor.para:
                    return None

                nome = os.path.join(self.pasta, str(self.data) + ".pdf")
                documentar(nome)
                converter_pdf(nome)

        # Remove os pdfs que não tiverem nenhuma ocorrencia na busca
    def remover_pdfs_nao_usados(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):

                if self.monitor.para:
                    return None

                if not self.ocorrencias.get((num_secao, num_pagina)):
                    os.remove(os.path.join(self.pasta, str(self.data) + ".pdf"))

    # Remove os txt que não tiverem nenhuma ocorrencia na busca
    def remover_txts_nao_usados(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):

                if self.monitor.para:
                    return None

                if not self.ocorrencias.get((num_secao, num_pagina)):
                    os.remove(os.path.join(self.pasta, str(self.data) + ".txt"))

    # Aplica o buscador no texto
    def analisar(self, buscador):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):

                if self.monitor.para:
                    return None

                nome = os.path.join(self.pasta, str(self.data) + ".pdf")

                documentar(nome)

                try:
                    arq = open(nome)
                    texto = arq.read()
                    arq.close()

                    ocorrencias_na_pagina = buscador.analisar(texto)

                    if len(ocorrencias_na_pagina) != 0:
                        self.ocorrencias[(num_secao, num_pagina)] = \
                            ocorrencias_na_pagina
                except:
                    documentar("----->Erro ao tentar abrir esse arquivo!<-----")

    # Baixa o jornal
    def baixar(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):

                if self.monitor.para:
                    return None

                nome = os.path.join(self.pasta, str(self.data) + ".pdf")

                # Isso deve fazer com que PDFs que não foram terminados de
                #baixar sejam deletados
                try:
                    arq = open(os.path.join(self.pasta, "baixando"), "r")
                    nome2 = arq.read()
                    os.remove(nome2)
                    arq.close()
                    os.remove(os.path.join(self.pasta, "baixando"))
                except:
                    print "Erro remover nao terminado"
                    pass

                arq = open(os.path.join(self.pasta, "baixando"), "w")
                arq.write(nome)
                arq.close()

                self.baixar_pagina(num_secao, num_pagina, self.data, nome)

                os.remove(os.path.join(self.pasta, "baixando"))


###############################################################################
class Diario_Oficial_do_MT(Diario_Justica_do_MT):

    nome = "Diario_Oficial_do_MT"
    numero_de_secoes = 1
    por_data = False

    # Baixa uma página de uma seção de uma data de jornal e coloca em uma pasta
    def baixar_pagina(self, num_secao, num_pagina, data, nome_arquivo):

        edicao = data

        pagina_jornal = "http://www.iomat.mt.gov.br/ler_pdf.php?download=ok&edi_id=" + str(edicao) + "&page=0"

        comando = ['wget', '-nc', '--output-document=' + nome_arquivo,
                    pagina_jornal]

        out, err = comandar(comando)

        if len(open(nome_arquivo).read()) < 100:
            try:
                os.remove(nome_arquivo)
            except:
                pass


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
