import requests
from bs4 import BeautifulSoup as bs
import warnings

# Ignora ciertos warnings de bs4
warnings.filterwarnings("ignore", module='bs4')

# Función para la búsqueda en la web, utilzando en este caso el motor de Bing
def searchBing(query, num):
    url = 'https://www.bing.com/search?q=' + query
    urls = []

    page = requests.get(url, headers = {'User-agent': 'John Doe'})
    soup = bs(page.text, 'html.parser')

    # Utiliza soup (beautifulsoup) para obtener datos de páginas web y extraerlos para su comparación.
    for link in soup.find_all('a'):
        url = str(link.get('href'))
        if url.startswith('http'):
            if not url.startswith('http://go.m') and not url.startswith('https://go.m'):
                urls.append(url)
    
    return urls[:num]

# Extrae el texto de la url buscada por searchBing()
def extractText(url):
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    return soup.get_text()
    
