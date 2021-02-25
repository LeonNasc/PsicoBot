from logica import *
from nltk.stem import RSLPStemmer as stemmer

class Resposta:

    def __init__(self, texto, regra, proxima_pergunta, conhecimento=None):
        self.Texto = texto
        self.Regra = regra
        self.Aplicada = False #Se a regra de produção for atendida, torna-se True
        self.ProximaPergunta = proxima_pergunta

        if conhecimento is not None:
            self.Conhecimento = conhecimento

    def AvaliarResposta(self, mensagem):
        mensagem = eval(ProcessadorGramatical.ProcessarFala(mensagem.content))
        self.Aplicada = self.AvaliarRegra(mensagem) 


    def AvaliarRegra(self,mensagem):
        conteudo = [m[0:-1] for m in mensagem]
        estrutura = [m[-1] for m in mensagem]
        conteudo_regra = [x[:-1] for x in self.Regra] 
        estrutura_regra = [x[-1] for x in self.Regra] 

        estrutura = self.AvaliarEstrutura(estrutura_regra, estrutura)
        conteudo = self.AvaliarConteudo(conteudo_regra, conteudo)
        print(estrutura)

        return (estrutura and conteudo)

    def AvaliarEstrutura(self,regras,mensagem):
        # Se a estrutura não for a da regra, a regra não se encaixa
        for regra in regras:
            if regra not in mensagem:
                return False

        # Remove todos os sintagmas que não atendem
        est_mensagem = [regra for regra in mensagem if regra in regras]


        # Verifica se a ordem sintática está igual
        for i in range(len(regras)):
            print(regras[i], est_mensagem[i])
            if regras[i] != est_mensagem[i]:
                return False

        #Se chegou até aqui, a estrutura é igual
        return True
    
    def AvaliarConteudo(self, regras, mensagem):
        stem = stemmer()

        mensagem_f = [stem.stem(msg) for msg in Resposta.__flatten_tupla(mensagem)]

        print(regras)
        print(mensagem)

        regras_validas = [regra for regra in regras if regra[0] != "*"] #Removo as regras wildcard

        palavras = []
        for regra in regras_validas:
            for palavra in regra:
                p = stem.stem(palavra)
                if p in mensagem_f:
                    print(regra, mensagem)
                    palavras.append(regra)
                    break #A regra já foi atendida

        return len(palavras) == len(regras_validas)

    def __flatten_tupla(l):
        return list(sum(l,()))

    '''
        Função Estática para instanciar as respostas do arquivo
    '''
    def InstanciarRespostas(dados_resposta):
        respostas = []
        for k in range(0, len(dados_resposta),3):
            try:
                id_resposta,texto_resposta,proxima_pergunta = dados_resposta[k].split("\t")

                # Detesto usar eval, mas estes dados vão estar representados as-is
                # e isso vai poupar tempo
                regra = eval(dados_resposta[k+1])
                conhecimento = eval(dados_resposta[k+2])

                resposta = Resposta(texto_resposta, regra, proxima_pergunta, conhecimento)
                respostas.append(resposta)
            except:
                print(dados_resposta)

        return respostas

