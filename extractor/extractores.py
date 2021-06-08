import re, math
from bs4 import BeautifulSoup

class Extractor():

    def __init__(self, respons):
        
        self.soup = BeautifulSoup(respons, "html.parser")

    def titulo(self):

        titulo = self.soup.find(id='productTitle')
        return titulo.text.strip()

    def precio(self):
        price = self.soup.find(id="priceblock_ourprice") or self.soup.find(id="price_inside_buybox") or self.soup.find(
            id="a-autoid-6-announce") or self.soup.find(id="newBuyBoxPrice") or self.soup.find(id="price") or self.soup.find(id="a-autoid-2-announce")
        return price.text.strip() if price is not None else "Precio no encontrado"

    def marca(self):
        marca = self.soup.find(id="bylineInfo")
        return marca.text.replace("Visit the", "").replace("Store", "").replace("Brand:", "").strip() if marca is not None else "Genérica"

    def imagenes(self):
        patron = re.compile('(?<="hiRes":")(.*?)(?=")', re.MULTILINE | re.DOTALL)
        imagenes = self.soup.find(id="imageBlock_feature_div")
        imagenes = imagenes.find(text=re.compile(
            '(?<="hiRes":")(.*?)(?=")', re.MULTILINE | re.DOTALL))
        imagenes = re.findall(patron, str(imagenes))

        return imagenes

    def disponibilidad(self):
        availability = self.soup.find(id="availability") or self.soup.find(
            id="exports_desktop_outOfStock_buybox_message_feature_div") or self.soup.find(id="ccbp-bb-primary-msg")
        return availability.text.replace("\n", "") if availability is not None else "Disponibilidad no encontrada"

    def caracteristicas(self):
        caracteristicas = None
        caracteristicas = self.soup.find(id="featurebullets_feature_div")
        caracteristicas = caracteristicas.find_all('li', id=False)
        caracteristicas = " ".join([c.text.strip() for c in caracteristicas])

        return caracteristicas

    def descripcion(self):
        descripcion = None
        descripcion = self.soup.find(id='productDescription')
        descripcion = descripcion.text.replace(
            "\n", "") if descripcion is not None else "No tiene descripcion"
        return descripcion

    def peso(self):
        info = self.soup.find(id='detailBullets_feature_div')

        if info is not None:

            lista = info.find_all('li')
            nuevalista = {}
            if lista:
                for item in lista:
                    if len(item.text.replace("\n", "").strip().split(":")) == 2:
                        clave, valor = item.text.replace("\n", "").strip().split(":")
                        nuevalista.update({
                            clave: valor
                        })
        else:

            info = self.soup.find(id='productDetails_feature_div')
            lista = info.table.find_all('tr') if info is not None else None
            nuevalista = {}
            if lista is not None:
                for item in lista:
                    clave = item.find('th').text.strip()
                    valor = item.find('td').text.strip()
                    nuevalista.update({
                        clave: valor
                    })

        pesoEncontrado = False
        peso = ""

        if nuevalista and (pesoEncontrado is False):
            
            for k, v in nuevalista.items():
                if k == "Item Weight" or k == "Product Dimensions":
                    peso = v
                    pesoEncontrado = True
        return peso


