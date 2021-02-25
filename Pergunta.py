from Resposta import *

class Pergunta:

    def __init__(self,_id, texto, respostas):
        self.Id = _id
        self.Texto = texto
        self.Respostas = respostas

    def AnalisarResposta(self, mensagem):

        for k in range(len(self.Respostas)):
            self.Respostas[k].AvaliarResposta(mensagem)

        selecionadas = [r for r in self.Respostas if r.Aplicada == True]

        if len(selecionadas) == 0: 
            # Resposta padrão para o caso de não entendimento
            return False

        else:
            return selecionadas[0]


    '''
    Função estática para instanciar as perguntas do arquivo base
    '''
    def InstanciarPerguntas(path):
            perguntas = []

            with open(path, 'r') as f:
                conteudo = f.read().splitlines()

            i = 0
            while i < len(conteudo):

                '''
                    Por exemplo, se a primeira pergunta está na linha 1 e tem 2
                    possíveis respostas, teremos:

                    1. Pergunta
                    2. Dados Resposta 1
                    3. Regras Resposta 1
                    4. Conhecimento Resposta 1
                    5. Dados Resposta 2
                    6. Regras Resposta 2
                    7. Conhecimento Resposta 2

                    Com isso, nosso intervalo de respostas é de i+1 até i+(3*n))
                    E precisamos incrementar o contador em i+(3*n)
                '''

                id_pergunta, texto_pergunta, n_respostas = conteudo[i].split("\t")
                comeco = i+1
                fim = i + 3*(int(n_respostas)) 

                if(n_respostas != 0):
                    dados_respostas = conteudo[comeco:fim + 1] #O python pega como ultimo item o index fim
                    respostas = Resposta.InstanciarRespostas(dados_respostas)

                i = fim+1 # Acertamos o indice

                pergunta = Pergunta(id_pergunta, texto_pergunta, respostas)
                perguntas.append(pergunta)

            return perguntas

