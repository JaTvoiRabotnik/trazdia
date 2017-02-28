class jornal():

    numero_de_secoes = 0
    por_data = True

    def __init__(self, data, pasta, monitor):
        self.data = data
        self.pasta = pasta
        self.teve_jornal = True

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
        arq = open(os.path.join(self.pasta, "dados"), "r")
        texto = arq.read()
        arq.close()
        texto = texto.split()
        data = texto.pop(0)
        for linha in texto:
            self.tam_secoes[int(linha)] = int(linha)

    # Salva um arquivo com os tamanhos das seções
    def salvar_dados(self):
        arq = open(os.path.join(self.pasta, "dados"), "w")
        arq.write(self.data)
        for i in self.tam_secoes:
            arq.write(" " + str(i))
        arq.close()

    # Obtem informações sobre o jornal
    def obter_info(self):
        for num_secao in range(1, self.numero_de_secoes + 1):

            if self.monitor.para:
                    return None

            self.tam_secoes[num_secao - 1] = \
                self.obter_num_paginas_secao(num_secao, self.data)

    # Baixa o jornal
    def baixar(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):

                if self.monitor.para:
                    return None

                nome = montar_nome_arquivo(self.pasta, self.data, num_secao,
                                           num_pagina, 'pdf')

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


    # Extrai os textos do jornal e deixa na mesma pasta
    def extrair_textos(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):

                if self.monitor.para:
                    return None

                nome = montar_nome_arquivo(self.pasta, self.data,
                                            num_secao, num_pagina, "pdf")
                documentar(nome)
                converter_pdf(nome)

    # Aplica o buscador no texto
    def analisar(self, buscador):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):

                if self.monitor.para:
                    return None

                nome = montar_nome_arquivo(self.pasta, self.data,
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
                    os.remove(montar_nome_arquivo(self.pasta, self.data,
                                                   num_secao, num_pagina, "pdf"))

    # Remove os txt que não tiverem nenhuma ocorrencia na busca
    def remover_txts_nao_usados(self):
        for num_secao in range(1, self.numero_de_secoes + 1):
            for num_pagina in range(1, self.tam_secoes[num_secao - 1] + 1):

                if self.monitor.para:
                    return None

                if not self.ocorrencias.get((num_secao, num_pagina)):
                    os.remove(montar_nome_arquivo(self.pasta, self.data,
                                                   num_secao, num_pagina, "txt"))

    # Remove todos os arquivos do jornal
    def remover(self):
        for arq in os.listdir(self.pasta):
            os.remove(os.path.join(self.pasta, arq))

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
