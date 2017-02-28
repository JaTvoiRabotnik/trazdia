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
