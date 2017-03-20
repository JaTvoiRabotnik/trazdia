class Monitor():

    def __init__(self, tipo, pasta):
        self.initial_date = date_texto2(datetime.date.today())
        self.edicao_1 = 1
        self.edicao_2 = 1
        self.datas = {}
        self.tipo_jornal = tipo
        self.pasta = pasta
        self.achados = []
        self.complitude = 0

        # todos,achados,nenhum
        self.guardar = "todos"

        # Usado para parar durante uma atualização
        self.para = False

        try:
            os.mkdir(os.path.join(self.pasta, self.tipo_jornal.nome))
        except:
            pass


    def parar(self):
        self.para = True


    def salvar(self):
        arq = open(self.tipo_jornal.nome + ".dat", "w")
        pickle.dump(self, arq)


    def carregar(self):
        try:
            arq = open(self.tipo_jornal.nome + ".dat", "r")
            return pickle.load(arq)
        except:
            return self


    def calcular_complitude(self):
        um_dia = datetime.timedelta(days=1)
        dia = texto_date(self.initial_date)
        amanha = datetime.date.today() + um_dia
        calculados = 0
        total = 0
        while dia < amanha:
            if self.datas.get(date_texto(dia)):
                calculados += 1
            dia += um_dia
            total += 1
        return float(calculados) / float(total)


    def reiniciar(self):
        self.achados = []
        self.datas = {}
        self.complitude = 0
        self.salvar()


    def alterar_data(self, data):
        self.initial_date = data
        self.salvar()


    def alterar_edicao_1(self, ed):
        try:
            self.edicao_1 = int(ed)
        except:
            print "Erro int edicao", ed
            pass


    def alterar_edicao_2(self, ed):
        try:
            self.edicao_2 = int(ed)
        except:
            print "Erro int edicao", ed
            pass


    def alterar_guardar(self, tipo):
        self.guardar = tipo
        self.salvar()


    def retornar_achados(self):
        lista = []
        lista2 = []
        for linha in self.achados:
            data, dic = linha
            lista.append(data)
            for linha2 in dic:
                sec, pag = linha2
                lista.append("Seção: " + str(sec) + "  Página: " + str(pag))
                oco = dic[linha2]
                for linha3 in oco:
                    palavra, posicao = linha3
                    if palavra not in lista2:
                        lista2.append(palavra)
                ocors = ""
                for linha4 in lista2:
                    ocors += '"' + linha4 + '" '
                lista.append(ocors)
        return lista


    def atualizar(self, buscador):
        self.para = False
        if self.tipo_jornal.por_data:
            self.atualizar_por_data(buscador)
        else:
            self.atualizar_por_edicao(buscador)


    def atualizar_por_edicao(self, buscador):
        edicao_atual = self.edicao_1
        while edicao_atual <= self.edicao_2:
            if self.para:
                return None
            journal_edition = self.datas.get(edicao_atual)

            # Verifica se já não foi analisado o jornal da data
            if not journal_edition:
                documentar("Processando edicao: " + str(edicao_atual))
                diretorio = os.path.join(self.pasta, self.tipo_jornal.nome)
                try:
                    os.mkdir(diretorio)
                except:
                    pass
                journal = self.tipo_jornal(edicao_atual, diretorio, self)
                print "Baixar!"
                ocorrencias = journal.executar(buscador)
                if self.para:
                    return None
                if len(ocorrencias) != 0:
                    self.achados.append((edicao_atual, ocorrencias))
                # Remove os arquivos e diretório caso o usuário queira,
                # ou caso aquele dia não teve jornal ( tamanho da primeira seção
                # provavelmente é 0 nesse caso )
                if (self.guardar == "nenhum") or (journal.tam_secoes[0] == 0):
                    journal.remover()
                    os.rmdir(diretorio)
                elif self.guardar == "achados":
                    if len(ocorrencias) == 0:
                        journal.remover()
                        os.rmdir(diretorio)
                    else:
                        journal.remover_pdfs_nao_usados()
                        journal.remover_txts_nao_usados()
                self.datas[edicao_atual] = "a"
                self.salvar()

            edicao_atual += 1
            print edicao_atual

        for items in self.retornar_achados():
            documentar(items)


    def atualizar_por_data(self, buscador):

        um_dia = datetime.timedelta(days=1)
        dia = texto_date(self.initial_date)
        amanha = datetime.date.today() + um_dia

        while dia < amanha:

            if self.para:
                return None

            jornal_data = self.datas.get(date_texto(dia))

            # Verifica se já não foi analisado o jornal da data
            if not jornal_data:

                documentar("Processando dia: " + date_texto2(dia))

                diretorio = os.path.join(self.pasta, self.tipo_jornal.nome, \
                            date_texto(dia).replace("/", "_"))

                try:
                    os.mkdir(diretorio)
                except:
                    print "Erro dir monitor"
                    pass
                # Instantiate the journal
                journal = self.tipo_jornal(date_texto2(dia), diretorio, self)
                ocorrencias = journal.executar(buscador)

                if self.para:
                    return None

                if len(ocorrencias) != 0:
                    self.achados.append((date_texto(dia), ocorrencias))

                # Remove os arquivos e diretório caso o usuário queira,
                # ou caso aquele dia não teve jornal ( tamanho da primeira seção
                # provavelmente é 0 nesse caso )
                if (self.guardar == "nenhum") or (journal.tam_secoes[0] == 0):
                    journal.remover()
                    os.rmdir(diretorio)
                elif self.guardar == "achados":
                    if len(ocorrencias) == 0:
                        journal.remover()
                        os.rmdir(diretorio)
                    else:
                        journal.remover_pdfs_nao_usados()
                        journal.remover_txts_nao_usados()

                self.datas[date_texto(dia)] = "a"
                self.salvar()

            dia += um_dia

        for items in self.retornar_achados():
            documentar(items)
