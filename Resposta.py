from logica import *

class Resposta:

    def __init__(self, texto, regra, proxima_pergunta, conhecimento=None):
        self.Texto = texto
        self.Regra = regra
        self.Aplicada = False #Se a regra de produção for atendida, torna-se True
        self.ProximaPergunta = proxima_pergunta

        if conhecimento is not None:
            self.Conhecimento = conhecimento

    def AvaliarResposta(self, mensagem):
        mensagem = ProcessadorGramatical.ProcessarFala(mensagem.content)
        self.Aplicada = self.AvaliarRegra(mensagem) 


    def AvaliarRegra(self,mensagem):
        conteudo, estrutura = zip(*mensagem)
        conteudo_regra, estrutura_regra = zip(*self.Regra)

        self.AvaliarEstrutura(estrutura_regra, estrutura)

    def AvaliarEstrutura(regras,mensagem):
        # Se a estrutura não for a da regra, a regra não se encaixa
        for regra in regras:
            if regra not in mensagem:
                return False

        est_mensagem = [regra for mensagem if regra in regras]



    '''
        Função Estática para instanciar as respostas do arquivo
    '''
    def InstanciarRespostas(dados_resposta):
        respostas = []
        for k in range(0, len(dados_resposta),3):
            id_resposta,texto_resposta,proxima_pergunta = dados_resposta[k].split("\t")

            # Detesto usar eval, mas estes dados vão estar representados as-is
            # e isso vai poupar tempo
            regra = eval(dados_resposta[k+1])
            conhecimento = eval(dados_resposta[k+2])

            resposta = Resposta(texto_resposta, regra, proxima_pergunta, conhecimento)
            respostas.append(resposta)

        return respostas

