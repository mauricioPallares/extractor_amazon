import re
from bs4 import BeautifulSoup
from helpers import normal_request

patron_hiRes = re.compile('(?<="hiRes":")(.*?)(?=")',
                                re.MULTILINE | re.DOTALL)
patron_large = re.compile('(?<="large":")(.*?)(?=")',
                                re.MULTILINE | re.DOTALL)

r = normal_request("1928576737")

soup = BeautifulSoup(r.text, "html.parser")



campo_imagenes = soup.find(id="imageBlock_feature_div")

# imagenes = imagenes.find(text=re.compile('(?<="hiRes":")(.*?)(?=")', re.MULTILINE | re.DOTALL))
imagenes1 = campo_imagenes.find(text=patron_hiRes)



if imagenes1 :
    imagenes1 = re.findall(patron_large, str(imagenes1))
    img = imagenes1
else :
    imagenes2 = campo_imagenes.find(text=patron_large)

    imagenes2 = re.findall(patron_large, str(imagenes2))
    img = imagenes2
    
print(img)

        