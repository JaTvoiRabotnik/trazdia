class Diario_Oficial_Uniao(jornal):

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
