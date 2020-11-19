#Extractive Text Summarization 
#Importamos los paquetes necesarios
import nltk
import re
import heapq  
from googletrans import Translator
from nltk import word_tokenize,sent_tokenize

#Leemos el texto
archTexto = open('texto.txt','r',encoding="utf8")
contenido  = archTexto.read()
archTexto.close()

#Traducimos el texto ESP --> ENG
translator = Translator()
contenido_eng = translator.translate(contenido,dest='en',src='es')

#Limpiamos el texto
texto = re.sub(r'\s+', ' ', contenido_eng.text)
texto = re.sub('\n[a-z][.]',' ',texto) 
texto = re.sub(r'\n',' ', texto) 
texto = re.sub(r'\s+',' ',texto)


#Realizamos la tokenización de palabras y oraciones
listaDePalabras = word_tokenize(texto)
listaDeOraciones = sent_tokenize(texto)

#Creamos una lista con las palabras más frecuentes del ingles
palabrasFrec = nltk.corpus.stopwords.words('english')

#Creamos una lista con la frecuencia de las palabras en el texto
frecPalabras = {}
for i in listaDePalabras:
    if i not in palabrasFrec:
        if i not in frecPalabras.keys():
            frecPalabras[i] = 1
        else:
            frecPalabras[i] += 1

#Buscamos la palabra con mayor frecuencia
frecMax = max(frecPalabras.values())

#Realizamos una normalización de las frecuencias
for j in frecPalabras.keys():  
    frecPalabras[j] = (frecPalabras[j]/frecMax)

#Calculamos las oraciones que más se repiten
puntajeOrac = {}  
for sent in listaDeOraciones:  
    for word in nltk.word_tokenize(sent.lower()):
        if word in frecPalabras.keys():
            if len(sent.split(' ')) < 30:
                if sent not in puntajeOrac.keys():
                    puntajeOrac[sent] = frecPalabras[word]
                else:
                    puntajeOrac[sent] += frecPalabras[word]

#Realizamos el resumen con las mejores oraciones
resumenOrac = heapq.nlargest(15, puntajeOrac, key=puntajeOrac.get)
resumen = ' '.join(resumenOrac)  

#Traducir el texto ENG --> ESP
translator = Translator()
textoRes = translator.translate(str(resumen),dest="es", src="en")
#print(type(textoRes.text))

archResumen = open('resumen.txt','w')
archResumen.write(textoRes.text) 
archResumen.close()

