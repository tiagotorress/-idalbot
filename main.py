from Chatbot import Chatbot

Bot = Chatbot('BobblesBot')
while True:
    frase = Bot.escuta()
    resp = Bot.pensa(frase)
    Bot.fala(resp)
    if resp == 'tchau':
        break
