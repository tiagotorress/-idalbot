from datetime import datetime

def pegalogins():
    arquivo = open('usuarios.csv', 'r')
    logins = {}
    linhas = arquivo.readlines()
    arquivo.close()
    for linha in linhas:
        usuario, senha = linha.split(',')
        senha = senha.replace('\n', '')
        logins[usuario] = senha
    print(logins)
    return logins

def gerarRelatorio():
    usuariosArq = open('usuarios.csv', 'r')
    relatorio = open('relatorio.txt', 'w')
    relatorio.write('USUARIO | SENHA | SERIE | EPISODIO | CRIACAO | ATUALIZACAO\n')
    usuarios = usuariosArq.readlines()
    usuariosArq.close()
    for linha in usuarios:
        usuario, senha = linha.split(',')
        senha = senha.replace('\n', '')
        seriesArq = open('users/' + usuario + '.csv', 'r')
        series = seriesArq.readlines()
        seriesArq.close()
        for serie in series:
            nome, episodio, criacao, atualizacao = serie.split(',')
            s = usuario + ' | ' + senha + ' | ' + nome + ' | ' + episodio + ' | ' + criacao + ' | ' + atualizacao + '\n'
            relatorio.write(s)


class Chatbot():

    def __init__(self, nome):
        self.dicionario = {}
        self.historico = []
        self.logins = pegalogins()
        self.titulo = ''
        self.temporada = ''
        self.episodio = ''
        self.login = ''

    def gerarlog(self, frase):
        arq = open('historico.log', 'a+')
        log = self.login + ' ' + datetime.now().strftime('%d/%m/%Y %H:%M') + ' ' + frase + '\n'
        arq.write(log)
        arq.close()
        
    def escuta(self, frase = None):
        if frase == None:
            frase = input('')
        frase = str(frase)
        return frase
    
    def pensa(self, frase):
        if frase == '/login':
            if self.login == '':
                self.login = 'logando'
                return 'Qual seu login?'
            else:
                return 'Você precisa fazer /logout antes de um novo login.'

        if self.login == '':
            return 'Você não está logado. Digite /login'

        if self.historico[-1] == 'Qual seu login?':
            self.login = frase
            self.gerarlog('/login')
            return 'Qual sua senha?'
        
        if frase == '/add' or frase == '/att':
            self.gerarlog(frase)
            return 'Qual o nome da serie?'

        if frase == '/rmv':
            self.gerarlog(frase)
            return 'Qual o nome da serie a ser removida?'
        
        if frase == '/rs':
            self.gerarlog(frase)
            return 'Qual o nome da serie a ser retornada?'

        if frase == '/rss':
            self.gerarlog(frase)
            return self.dicionario

        if frase == '/rsa':
            self.gerarlog(frase)
            return sorted(self.dicionario.items(), key = lambda x: x[0])

        if frase == '/zer':
            self.gerarlog(frase)
            if self.login == 'admin':
                return 'Qual o usuário que será zerado?'
            else:
                return 'Você não tem permissão para isso'
        
        if frase == '/rel':
            self.gerarlog(frase)
            if self.login == 'admin':
                gerarRelatorio()
                return 'Relatório gerado.'
            else:
                return 'Você não tem permissão para isso'


        if frase == '/help' or frase  == '/start':
            self.gerarlog(frase)
            return "/login -> Siga os passos e faça login!\n /logout -> Siga os passos e faça logout\n /add -> Siga os passos e adicione uma série!\n /att -> Siga os passos e atualize uma série!\n /rmv -> Siga os passos e remova uma série\n /rs -> Siga os passos e saiba onde você parou em alguma série\n /rss -> Saiba onde você está em todas as séries\n /help -> Veja os comandos!"

        if frase == '/logout':
            arquivo = open('users/' + self.login + '.csv', 'w')
            linha = ''
            for serie in self.dicionario:
                linha = linha + serie+","+self.dicionario[serie][0]+','+self.dicionario[serie][1]+','+self.dicionario[serie][2]+'\n'                
            arquivo.write(linha)
            arquivo.close()
            self.login = ''
            self.dicionario = {}
            return 'Logout bem sucedido'

        if self.historico[-1] == 'Qual o usuário que será zerado?':
            if frase in self.logins:
                arq = open('users/' + frase + '.csv', 'w')
                arq.close()
                return 'Usuário zerado.'
            else:
                return 'Usuário não existe.'

        if self.historico[-1] == 'Qual o nome da serie?':
            self.titulo = frase
            return 'Qual temporada você está?'

        if self.historico[-1] == 'Qual temporada você está?':
            self.temporada = frase
            return 'Qual episodio você está?'

        if self.historico[-1] == 'Qual episodio você está?':
            self.episodio = frase
            if self.titulo in self.dicionario:
                horario_criacao = self.dicionario[self.titulo][2]
                self.dicionario[self.titulo] = ('T' + self.temporada + 'E' +  self.episodio, horario_criacao, datetime.now().strftime('%d/%m/%Y %H:%M'))
                return self.titulo + ' atualizado!'
            else:
                self.dicionario[self.titulo] = ('T' + self.temporada + 'E' +  self.episodio, datetime.now().strftime('%d/%m/%Y %H:%M'), datetime.now().strftime('%d/%m/%Y %H:%M'))
                return self.titulo + ' adicionado!'

        if self.historico[-1] == 'Qual o nome da serie a ser removida?':
            del self.dicionario[frase]
            return frase + ' foi removido!'

        if self.historico[-1] == 'Qual o nome da serie a ser retornada?':
            return str(self.dicionario[frase])

        if self.historico[-1] == 'Qual sua senha?':
            if self.login in self.logins:
                if self.logins[self.login] == frase:
                    arquivo = open('users/' + self.login + '.csv', 'r')
                    linhas = arquivo.readlines()
                    self.dicionario = {}
                    for linha in linhas:
                        if linha != '' and linha != ' ' and linha != '\n':
                            titulo, episodio, horario_criacao, horario_alteracao = linha.split(',')
                            horario_alteracao = horario_alteracao.replace('\n', '')
                            self.dicionario[titulo] = (episodio, horario_criacao, horario_alteracao)
                    return 'Login bem sucedido'
                else:
                    return 'Senha errada. Tente novamente.'
            else:
                self.logins[self.login] = frase
                arquivo = open('users/' + self.login + '.csv', 'w')
                arquivo.close()
                usuarios = open('usuarios.csv', 'a')
                linha = self.login+','+frase+'\n'
                usuarios.write(linha)
                return 'Usuário cadastrado'


    def fala(self, frase):
        print(self.logins)
        self.historico.append(frase)
        print(frase)


