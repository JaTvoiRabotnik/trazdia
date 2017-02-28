class atualizador(Thread):

    def __init__(self, funcao, intervalo=1, uma_vez=False, arg=None):
        Thread.__init__(self)
        self.flag = True
        self.funcao = funcao
        self.intervalo = intervalo
        self.uma_vez = uma_vez
        self.arg = arg

    def run(self):
        if self.uma_vez:
            if self.arg:
                self.funcao(self.arg)
            else:
                self.funcao()
        else:
            while self.flag:
                if self.arg:
                    self.funcao(self.arg)
                else:
                    self.funcao()

                time.sleep(self.intervalo)

    def parar(self):
        self.flag = False
