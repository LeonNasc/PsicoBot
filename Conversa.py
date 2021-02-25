from datetime import datetime
from Pergunta import *

PATH_PERGUNTAS = "./Perguntas/perguntas.txt"

class Conversa:

    CONTADOR_MAX = 20

    def __init__(self, usuario):
        self.Usuario = usuario
        self.Perguntas = Pergunta.InstanciarPerguntas(PATH_PERGUNTAS)
        self.PerguntaAtual = self.Perguntas[0] # A primeira pergunta
        self.is_Valida = True
        self.Conhecimentos = {}
        self.contador = 0

    def Responder(self, mensagem):

        is_termino = self._AvaliarCondicoesDeTermino(mensagem)

        if(is_termino): 
            #A conversa chegou ao fim, retornando uma resposta padrão
            return is_termino
        else:
            tipo_resposta = self.PerguntaAtual.AnalisarResposta(mensagem) 

            if(tipo_resposta):
                #Obtivemos uma resposta que avança a conversa
                self.AtualizarBaseConhecimento(tipo_resposta)
                proxima_pergunta = [p for p in self.Perguntas if p.Id == tipo_resposta.ProximaPergunta][0]
                self.PerguntaAtual = proxima_pergunta

                if(len(self.PerguntaAtual.Respostas) == 0):
                    self.is_Valida = False

                self.contador = self.contador + 1 

            else:
                # Resposta padrão do "Não-entendi"
                # Como a pergunta é a mesma, as respostas também o são
                return Pergunta("NE","Hmm... Você poderia explicar isso melhor para mim?", self.PerguntaAtual.Respostas)

        return proxima_pergunta

    def _AvaliarCondicoesDeTermino(self, mensagem):
        # Começamos do começo se a ultima resposta tiver ocorrido há mais de 10 minutos
        if((mensagem.created_at - datetime.now()).seconds < -600):
            self.is_Valida = False
            return Pergunta("TIMEOUT","Hmmm... Parece que perdemos o fio da meada. Vamos começar de novo..." , [])

        # A conversa andou andou e não deu em nada
        elif(self.contador > Conversa.CONTADOR_MAX): 
            self.is_Valida = False
            return Pergunta("OVERFLOW","%s, com base nas informações dadas, não consigo afirmar se você tem ansiedade ou não. Nestes casos, a melhor coisa a se fazer é procurar um profissional. Eu sou apenas um robô bobo! :)" % mensagem.author , [])

        elif(self.AvaliarCriterios()):
            self.is_Valida = False
            return Pergunta("CRITERIOS","%s, me parece que você pode ter um Transtorno de Ansiedade. Nestes casos, a melhor coisa a se fazer é procurar um profissional. Eu sou apenas um robô bobo! :)" % mensagem.author , [])
        else:
            return False

    def AvaliarCriterios(self):
        sintomas  = self.AvaliarSintomas()
        impacto = self.Conhecimento["Impacto"]
        tempo = self.Conhecimento["Tempo"]

        if (sintomas and impacto and tempo):
            return True
        else:
            return False


    def AtualizarBaseConhecimento(self,resposta):
            if(resposta.Conhecimento):
                self.Conhecimentos[resposta.Conhecimento[0]] = resposta.Conhecimento[1]

    
