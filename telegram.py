import telepot
from Chatbot import Chatbot

telegram = telepot.Bot("1004548222:AAFCg9WIPfpKNsaH1sXqv2XYk_UrwVguLIo")

bot = Chatbot("Idal_Bot")

def recebendoMsg(msg):
    frase = bot.escuta(frase = msg['text'])
    resp = bot.pensa(frase)
    bot.fala(resp)
    tipoMsg, tipoChat, chatID = telepot.glance(msg)
    telegram.sendMessage(chatID, resp)

telegram.message_loop(recebendoMsg)

while True:
    pass
