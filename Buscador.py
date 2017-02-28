# Realiza a pesquisa
class buscador():

    def __init__(self, nome):
        self.palavras_procuradas = []
        self.nome = nome


    def adicionar(self, pal):
        self.palavras_procuradas.append(pal)


    def trocar(self, palavras):
        self.palavras_procuradas = palavras


    def salvar(self, nome_arquivo=None):
        if not nome_arquivo:
            nome_arquivo = self.nome

        try:
            arq = open(nome_arquivo, "w")
            for linha in self.palavras_procuradas:
                arq.write(linha + "\n")
            arq.close()
        except:
            print("Não foi possível salvar o arquivo do buscador!")


    def carregar(self, nome_arquivo=None):
        if not nome_arquivo:
            nome_arquivo = self.nome

        try:
            arq = open(nome_arquivo, "r")
            texto = arq.read()
            arq.close()
            texto = texto.splitlines()
            for linha in texto:
                self.adicionar(linha)
        except:
            print("Arquivo do buscador não encontrado!")


    def analisar(self, texto):

        ocorrencias = []

        for palavra in self.palavras_procuradas:

            posicao = 0
            while posicao != -1:
                posicao = texto.find(palavra, posicao)

                if posicao != -1:
                    ocorrencias.append((palavra, posicao))
                    posicao += 1

        return ocorrencias
