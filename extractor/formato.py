import unicodedata, re


def quitarTildes(texto: str) -> str:
    """Esta funcion elimina todas las tildes de una cadena de string

    Args:
        texto (str): Cadena original

    Returns:
        str: Cadena sin tildes
    """
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )

    for a, b in replacements:
        s = texto.replace(a, b).replace(a.upper(), b.upper())
    return s




def normalizarTexto(texto: str) -> str:
    """[summary]

    Args:
        texto (str): Cadena original

    Returns:
        str: Cadena normalizada
    """

    texto = texto or ""
    
    s = quitarTildes(texto)
    s = s.replace("ñ","#").replace("Ñ","#")
    s = unicodedata.normalize("NFKD",s).encode("ascii", "ignore").decode("ascii").replace("#","ñ")
    
    return s




def limpiarTexto(texto):
    
    texto = normalizarTexto(texto)
    newtexto = []
    for palabra in texto.split(" "):
        if re.search("/([+][0-9]+[-])?[()]?\d{3}[()]?[-][()]?\d{3}[()]?[-]\d{4}/",palabra) or palabra.lower() == "amazon" or palabra.lower() == "garantia" or re.search("/(http:\/\/|www\.)?[a-zA-Z0-9_.-]+\.[a-z]+\/?/",palabra):
            palabra = ""
        if re.search("/in\.$/", palabra) or re.search("/in,$/",palabra):
            palabra = "pulgadas"
        
        newtexto.append(palabra)

    newtexto = " ".join(newtexto)
    return newtexto




def limpiarPrecio(precio):
    precio = precio or ""
    aux = precio.replace("US$","").replace("$", "")
    if len(aux.split("-")) == 2:
        newPrecio= aux.split("-")[1]
         
    else:
        newPrecio = aux
    
    return newPrecio.strip()




def limpiaPeso(peso):
    peso = peso or ""

    if len(peso.split(";"))==2:
        a = peso.split(";")
        newPeso = a[1]
    else:
        newPeso = peso
    
    return newPeso.strip()





def arrayImagenes(imagenes: str) -> list:
    """ toma el campo imagenes, que es un cadena de imagenes separadas por espacion en blanco o coma, y la convierte en una lista de diccionarios, que contiene el formato de imagenes de mercadolibre

    Args:
        imagenes (str): cadena que contiene la informacion de las imagenes

    Returns:
        list: lista de imagenes 
    """
    if len(imagenes.split(",")) == 1:
        newImagenes = imagenes.split(" ")
    else:
        newImagenes = imagenes.split(",")
    
    tamanio = len(newImagenes)

    limite = tamanio if tamanio <= 6 else 6
    imgs = []
    for i in range(limite):
        imgs.append({
            "source": newImagenes[i]
        })

    return imgs
    




def fixmarca(marca: str) -> str:
    """ Esta funcion normaliza la marca, eliminando caracteres especiales y capilizando el primer caracter de cada palabra

    Args:
        marca (str): nombre de la marca del producto

    Returns:
        str: marca del producto normalizada
    """
    marca = marca or "Genérica"

    if marca is None or marca == "":
        marca = "Genérica"
    else:
        
        aux = []

        marca = marca.split("-")
        for i in marca:
            aux.append(i.title())
            marca = "-".join(aux)
        aux = []

    return marca

def imagenesProducto(imagenes):
    
    tamanio = len(imagenes)

    limite = tamanio if tamanio <= 6 else 6
    imgs = []
    for i in range(limite):
        imgs.append({
            "source": imagenes[i]
        })

    return imgs

