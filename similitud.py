from tkinter import CENTER
import nltk
import busquedaweb
from difflib import SequenceMatcher
import pandas as pd

# Sirven para preprocesar textos, previene que ciertos caracteres se tomen en cuenta
nltk.download('stopwords')
nltk.download('punkt')

# Idioma inglés por defecto, no afecta a la búsqueda
stop_words = set(nltk.corpus.stopwords.words('english')) 

# Purifica el texto ingresado, lo prepara para su tratamiento
def purifyText(string):
    words = nltk.word_tokenize(string)
    return (" ".join([word for word in words if word not in stop_words]))

# Función que verifica en la web los resultados que son ingresados, busca en el navegador por matches
def webVerify(string, results_per_sentence):
    sentences = nltk.sent_tokenize(string)
    matching_sites = []
    for url in busquedaweb.searchBing(query=string, num=results_per_sentence):
        matching_sites.append(url)
    for sentence in sentences:
        for url in busquedaweb.searchBing(query = sentence, num = results_per_sentence):
            matching_sites.append(url)

    return (list(set(matching_sites)))

# Función para encontrar la similitud entre dos textos, utilizando SequenceMatcher (*100 para porcentaje)
def similarity(str1, str2):
    return (SequenceMatcher(None,str1,str2).ratio())*100


# Función para construir el reporte con la tabla de links
def report(text):
    matching_sites = webVerify(purifyText(text), 2)
    matches = {}

    # Itera entre las búsquedas de los sitios para encontrar los items que hagan match (Indica el plagio)
    for i in range(len(matching_sites)):
        matches[matching_sites[i]] = similarity(text, busquedaweb.extractText(matching_sites[i]))

    matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)}
    return matches


'''
Función para retornar la tabla del reporte con los links y su porcentaje de coincidencias.
No están acomodados, pero usualmente el link con porcentaje más alto es el que indica el plagio.
'''
def returnTable(dictionary):
    df = pd.DataFrame({'(%) de Similitud': dictionary})
    sorted_df = df.sort_values(by='(%) de Similitud')
    tableOfResults = sorted_df.to_html(classes=['table-bordered', 'table-striped', 'table-hover'], render_links=True, escape=True, justify=CENTER)
    print(tableOfResults)
    print(type(tableOfResults))
    return tableOfResults

# Función main con un reporte de prueba sencillo
if __name__ == '__main__':
    report('This is a pure test')
