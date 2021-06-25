import re
import math
from bs4 import BeautifulSoup
from formato import normalizarTexto
from helpers import log
from helpers import realizar_peticion

unidad_peso = ["pounds", "ounces", "kilograms"]
peso_en = ["Item Weight", "Package Dimensions", "Product Dimensions"]
disponibilidad_true = [
    "in stock.",
    "Usually ships within",
    "Usually ships soon.",
    "Available to ship",
    
]
disponibilidad_false = [
    "Temporarily out of stock",
    "disponibilidad no encontrada",
    "Currently unavailable",
    "This item will be released on",
    "in stock soon",
    "in stock on",
]
cantidad_minima = 3

class Extractor():
    """ Clase Extractor, posee metodos para extraer informacion estructurada de un producto de la tienda en linea amazon
    """

    def __init__(self, respons):
        """[summary]

        Args:
            respons (requests): Recibe un request.text, desde una peticion a https://amazon.com/dp/sku 
        """
        self.soup = BeautifulSoup(respons, "html.parser")

    def titulo(self):
        """[summary]

        Returns:
            [String]: [Titulo del producto]
        """
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
        patron = re.compile('(?<="hiRes":")(.*?)(?=")',
                            re.MULTILINE | re.DOTALL)
        imagenes = self.soup.find(id="imageBlock_feature_div")
        imagenes = imagenes.find(text=re.compile(
            '(?<="hiRes":")(.*?)(?=")', re.MULTILINE | re.DOTALL))
        imagenes = re.findall(patron, str(imagenes))

        return imagenes

    def disponibilidad(self):
        availability = self.soup.find(id="availability") or self.soup.find(
            id="exports_desktop_outOfStock_buybox_message_feature_div") or self.soup.find(id="ccbp-bb-primary-msg")
        return availability.text.replace("\n", "") if availability is not None else "Disponibilidad no encontrada"
        
    def stock(self):
        stock = None

        for dip in disponibilidad_true:
            if self.disponibilidad().lower().startswith(dip.lower()):
                stock = "En Stock"
                break

        
        for dip in disponibilidad_false:
            if self.disponibilidad().lower().startswith(dip.lower()):
                stock = "Sin Stock"
                break

        if not stock:
            if self.disponibilidad() == "":
                stock = "Sin Stock"

        if not stock:
            if self.disponibilidad().startswith("only"):
                cant = [int(s) for s in self.disponibilidad().split() if s.isdigit()]
                if cant[0] >= cantidad_minima:

                    stock = "En Stock"
                else:
                    stock = "Sin Stock"

        return stock

    def caracteristicas(self):
        caracteristicas = None
        caracteristicas = self.soup.find(id="featurebullets_feature_div")
        # revisar error
        try:

            caracteristicas = caracteristicas.find_all('li', id=False)
            caracteristicas = " ".join([c.text.strip() for c in caracteristicas])
            return caracteristicas

        except AttributeError:
            log("Error: Atributo no encontrando.")
            return ""

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
                        clave, valor = item.text.replace(
                            "\n", "").strip().split(":")
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

        # pesoEncontrado = False
        peso = ""

        if nuevalista:

            for k, v in nuevalista.items():
                k = normalizarTexto(k)
                if k in peso_en:
                    for up in unidad_peso:
                        if up.lower() in v.lower():
                            peso = v
                            break

        return peso




if __name__ == '__main__':

    soup = realizar_peticion("B07V4FTX6C")
    ex = Extractor(soup.text)

    print(ex.titulo())
    print(ex.disponibilidad())
    print(ex.stock())
