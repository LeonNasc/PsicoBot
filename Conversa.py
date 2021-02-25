from datetime import datetime
from Pergunta import *

PATH_PERGUNTAS = "./Perguntas/perguntas.txt"

class Conversa:

    def __init__(self, usuario):
        self.Usuario = usuario
        self.Perguntas = Pergunta.InstanciarPerguntas(PATH_PERGUNTAS)
        self.PerguntaAtual = self.Perguntas[0] # A primeira pergunta
        self.is_Valida = True
        self.Conhecimentos = {}

    def Responder(self, mensagem):

        # Começamos do começo se a ultima resposta tiver ocorrido há mais de 10 minutos
        if((mensagem.created_at - datetime.now()).seconds < -600):
            self.is_Valida = False
            return Pergunta("TIMEOUT","Hmmm... Parece que perdemos o fio da meada. Vamos começar de novo..." , [])


        else:
            tipo_resposta = self.PerguntaAtual.AnalisarResposta(mensagem) 

            if(tipo_resposta):
                #Obtivemos uma resposta que avança a conversa
                self.AtualizarBaseConhecimento(tipo_resposta)
                proxima_pergunta = [p for p in self.Perguntas if p.Id == tipo_resposta.ProximaPergunta][0]
                self.PerguntaAtual = proxima_pergunta

                if(len(self.PerguntaAtual.Respostas) == 0):
                    self.is_Valida = False


            else:
                # Resposta padrão do "Não-entendi"
                # Como a pergunta é a mesma, as respostas também o são
                return Pergunta("NE","Hmm... Você poderia explicar isso melhor para mim?", self.PerguntaAtual.Respostas)

        return proxima_pergunta

    def AtualizarBaseConhecimento(self,resposta):
            if(resposta.Conhecimento):
                self.Conhecimentos[resposta.Conhecimento[0]] = resposta.Conhecimento[1]

    
