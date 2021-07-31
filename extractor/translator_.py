from googletrans import Translator
from helpers import get_proxy
from modelo import con, cursor

def traducir(texto: str = None)-> str:
    proxy = get_proxy()
    translator = Translator(proxies=proxy)
    # print(proxy)
    try:

        text_translated = translator.translate(texto, dest='es')
        return text_translated.text
    except Exception as e:
        print("ha ocurrido un error en la traduccion")
        print(e)
        return None


    # print(text_translated.text)
    

if __name__ == '__main__':
    palabras = ["hello world",
    "translate a spanish text to arabic for instance",
    "the following commands:",
    "the translated text and language", None]

    sql = "SELECT sku, titulo FROM productos_andres_descarga where sku = 'B0001YXMUA'"
    cursor.execute(sql)

    data = cursor.fetchall()
    print("inicia la traduccion...")
    for i in data:
        # print(i['sku'], " ", traducir(i['descripcion']))
        traduccion = traducir(i['titulo'])
        if traduccion:
            sql = "UPDATE productos_andres_descarga SET titulo = %s WHERE sku = %s"

            cursor.execute(sql, (
                traduccion,
                i['sku']
            ))
            con.commit()
            print(i['sku'], traduccion)
        else:
            print(i['sku'], "no traducido")