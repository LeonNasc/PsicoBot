import joblib
import nltk
from nltk import word_tokenize

#Obtendo alguns requisitos do nltk
nltk.download('rslp')
nltk.download('stopwords')
nltk.download('punkt')
stopwords_pt = nltk.corpus.stopwords.words('portuguese')

'''
	Nota(LEON): O NLTK realiza a análise gramática pelo conceito de 
	part-of-speech (POS). Esta análise é feita sobre um corpus de
	texto taggeado, treinando um classificador. O classificador foi
	treinado pelo <https://github.com/inoueMashuu/POS-tagger-portuguese-nltk>, 
	com o maior desempenho obtido pela técn	ica de brill tagging
	 <https://en.wikipedia.org/wiki/Brill_tagger
'''
# Pasta com o modelo gramatical treinado
folder = 'trained_POS_taggers/'
tagger = joblib.load(folder+'POS_tagger_brill.pkl')


class ProcessadorGramatical:

    def ProcessarFala(fala):
            fala = fala.split(" ") #Transformamos a fala em uma lista de palavras)
            fala = ProcessadorGramatical.remover_stopwords(fala)
            fala = ProcessadorGramatical.analisar_gramatica(fala)
            return str(fala)

    def remover_stopwords(fala):
            return [ x for x in fala if x not in stopwords_pt ]

    def analisar_gramatica(fala):
            #Fala virá como array, após tirada das stopwords
            fala = " ".join(fala)
            return tagger.tag(word_tokenize(fala))

