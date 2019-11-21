from datetime import datetime
import telepot

def pegalogins():
    arquivo = open('usuarios.csv', 'r')
    logins = {}
    linhas = arquivo.readlines()
    arquivo.close()
    for linha in linhas:
        usuario, senha = linha.split(',')
        senha = senha.replace('\n', '')
        logins[usuario] = senha
    return logins

dicionario = {}
historico = []
logins = pegalogins()
titulo = ''
temporada = ''
episodio = ''
login = ''

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

def gerarlog(frase):
    global login
    arq = open('historico.log', 'a+')
    log = login + ' ' + datetime.now().strftime('%d/%m/%Y %H:%M') + ' ' + frase + '\n'
    arq.write(log)
    arq.close()

def bubblesort(dicionario):
    keys = dicionario.keys()
    lista = []
    for i in keys:
        lista.append(i)
        print(lista)
    elementos = len(lista)-1
    ordenado = False
    while not ordenado:
        ordenado = True
        for i in range(elementos):
            if lista[i] > lista[i+1]:
                lista[i], lista[i+1] = lista[i+1],lista[i]
                ordenado = False        
    dicionariorsa = {}
    for i in lista:
        dicionariorsa[i] = dicionario[i]   
    return dicionariorsa

def escuta(frase = None):
    if frase == None:
        frase = input('')
    frase = str(frase)
    return frase

def pensa(frase):
    global dicionario
    global historico
    global logins
    global titulo
    global temporada
    global episodio
    global login

    if frase == '/login':
        if login == '':
            login = 'logando'
            return 'Qual seu login?'
        else:
            return 'Você precisa fazer /logout antes de um novo login.'

    if login == '':
        return 'Você não está logado. Digite /login'

    if historico[-1] == 'Qual seu login?':
        login = frase
        gerarlog('/login')
        return 'Qual sua senha?'
    
    if frase == '/add' or frase == '/att':
        gerarlog(frase)
        return 'Qual o nome da serie?'

    if frase == '/rmv':
        gerarlog(frase)
        return 'Qual o nome da serie a ser removida?'
    
    if frase == '/rs':
        gerarlog(frase)
        return 'Qual o nome da serie a ser retornada?'

    if frase == '/rss':
        gerarlog(frase)
        return dicionario

    if frase == '/rsa':
        gerarlog(frase)
        return bubblesort(dicionario)

    if frase == '/zer':
        gerarlog(frase)
        if login == 'admin':
            return 'Qual o usuário que será zerado?'
        else:
            return 'Você não tem permissão para isso'
    
    if frase == '/rel':
        gerarlog(frase)
        if login == 'admin':
            gerarRelatorio()
            return 'Relatório gerado.'
        else:
            return 'Você não tem permissão para isso'


    if frase == '/help' or frase  == '/start':
        gerarlog(frase)
        return "/login -> Siga os passos e faça login!\n /logout -> Siga os passos e faça logout\n /add -> Siga os passos e adicione uma série!\n /att -> Siga os passos e atualize uma série!\n /rmv -> Siga os passos e remova uma série\n /rs -> Siga os passos e saiba onde você parou em alguma série\n /rss -> Saiba onde você está em todas as séries\n /help -> Veja os comandos!"

    if frase == '/logout':
        arquivo = open('users/' + login + '.csv', 'w')
        linha = ''
        for serie in dicionario:
            linha = linha + serie+","+dicionario[serie][0]+','+dicionario[serie][1]+','+dicionario[serie][2]+'\n'                
        arquivo.write(linha)
        arquivo.close()
        login = ''
        dicionario = {}
        return 'Logout bem sucedido'

    if historico[-1] == 'Qual o usuário que será zerado?':
        if frase in logins:
            arq = open('users/' + frase + '.csv', 'w')
            arq.close()
            return 'Usuário zerado.'
        else:
            return 'Usuário não existe.'

    if historico[-1] == 'Qual o nome da serie?':
        titulo = frase
        return 'Qual temporada você está?'

    if historico[-1] == 'Qual temporada você está?':
        temporada = frase
        return 'Qual episodio você está?'

    if historico[-1] == 'Qual episodio você está?':
        episodio = frase
        if titulo in dicionario:
            horario_criacao = dicionario[titulo][2]
            dicionario[titulo] = ('T' + temporada + 'E' +  episodio, horario_criacao, datetime.now().strftime('%d/%m/%Y %H:%M'))
            return titulo + ' atualizado!'
        else:
            dicionario[titulo] = ('T' + temporada + 'E' +  episodio, datetime.now().strftime('%d/%m/%Y %H:%M'), datetime.now().strftime('%d/%m/%Y %H:%M'))
            return titulo + ' adicionado!'

    if historico[-1] == 'Qual o nome da serie a ser removida?':
        del dicionario[frase]
        return frase + ' foi removido!'

    if historico[-1] == 'Qual o nome da serie a ser retornada?':
        return str(dicionario[frase])

    if historico[-1] == 'Qual sua senha?':
        if login in logins:
            if logins[login] == frase:
                arquivo = open('users/' + login + '.csv', 'r')
                linhas = arquivo.readlines()
                dicionario = {}
                for linha in linhas:
                    if linha != '' and linha != ' ' and linha != '\n':
                        titulo, episodio, horario_criacao, horario_alteracao = linha.split(',')
                        horario_alteracao = horario_alteracao.replace('\n', '')
                        dicionario[titulo] = (episodio, horario_criacao, horario_alteracao)
                return 'Login bem sucedido \n /logout -> Siga os passos e faça logout\n /add -> Siga os passos e adicione uma série!\n /att -> Siga os passos e atualize uma série!\n /rmv -> Siga os passos e remova uma série\n /rs -> Siga os passos e saiba onde você parou em alguma série\n /rss -> Saiba onde você está em todas as séries\n /help -> Veja os comandos!' 
            else:
                return 'Senha errada. Tente novamente.'
        else:
            logins[login] = frase
            arquivo = open('users/' + login + '.csv', 'w')
            arquivo.close()
            usuarios = open('usuarios.csv', 'a')
            linha = login+','+frase+'\n'
            usuarios.write(linha)
            return 'Usuário cadastrado'

def fala(frase):
    historico.append(frase)
    print(frase)


escolha = input("Digite 1 para iniciar o servidor telegram e 2 para rodar o programa normalmente\n")

if escolha == 1:
    telegram = telepot.Bot("1004548222:AAFCg9WIPfpKNsaH1sXqv2XYk_UrwVguLIo")

    def recebendoMsg(msg):
        frase = escuta(frase = msg['text'])
        resp = pensa(frase)
        fala(resp)
        tipoMsg, tipoChat, chatID = telepot.glance(msg)
        telegram.sendMessage(chatID, resp)

    telegram.message_loop(recebendoMsg)

    while True:
        pass

while True:
    frase = escuta(input(''))
    resp = pensa(frase)
    fala(resp)

 








