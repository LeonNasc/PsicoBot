import discord
from logica import *
from Conversa import *

class Bot(discord.Client):

    conversas_ativas = []

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):

        # Para o bot não falar sozinho
        if message.author == self.user:
            return

        #Vamos limpar a memória de conversas que já acabaram
        Bot.conversas_ativas = [c for c in Bot.conversas_ativas if c.is_Valida == True]
        
        conversa, is_nova_conversa = Bot.obter_conversa(message)
        if(is_nova_conversa):
            resposta = conversa.PerguntaAtual
        else:
            resposta = conversa.Responder(message) 

        await message.channel.send(resposta.Texto)


    def obter_conversa(message):
        conversas_c_pessoa = [conversa for conversa in Bot.conversas_ativas 
                if conversa.Usuario == message.author]

        if len(list(conversas_c_pessoa)) == 0:
            conversa = Conversa(message.author)
            Bot.conversas_ativas.append(conversa)
            is_Nova = True
        else:
            conversa = list(conversas_c_pessoa)[0] 
            is_Nova = False

        return (conversa, is_Nova)


client = Bot()

# SUBSTITUIR TOKEN AQUI
with open('_token.txt','r') as f:
    token = f.readlines()[0] 

client.run(token)
