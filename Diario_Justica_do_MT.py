class Diario_Justica_do_MT(jornal):

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
