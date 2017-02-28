class Diario_Oficial_SP(jornal):

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
