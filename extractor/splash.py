import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from helpers import get_proxy

url = "https://www.amazon.com/dp/B00004VUFG/ref=olp_aod_redir_impl1?_encoding=UTF8&aod=1"
header = {"Content-Type": "application/",
          'user_agent': generate_user_agent()}
print(get_proxy())
r = requests.get(
    url="http://localhost:8050/render.html",
    params={'url': url, 'wait': 2, 'proxy': get_proxy()})

soup = BeautifulSoup(r.text, 'html.parser')

ofertas = soup.find(id='aod-offer-list').find_all(id='aod-offer-price')
precios = []
for oferta in ofertas:

    precio = oferta.find('span', {'class': 'a-offscreen'}).text
    precio = precio.replace("$", "")
    precios.append(float(precio))
    print("---------------------------------------------------------")


print("el precio mas alto ", max(precios))
