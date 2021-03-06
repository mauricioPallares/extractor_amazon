import pandas as pd, shutil
import math, os, redis
from helpers import counts, enCola

DIR_PACK = os.path.dirname(os.path.realpath(__file__)) + "/paquetes"
DIR_AGREGADOS = os.path.dirname(os.path.realpath(__file__)) + "/agregados"

def cargar_skus_from_file(archivo):
    
    lista = pd.read_excel(os.path.join(DIR_PACK,archivo))
    lista_sku = set(lista['asin'].to_list())

    for sku in lista_sku:
        enCola(sku)

    return len(lista_sku)

def mover_archivo(archivo):
    shutil.move(os.path.join(DIR_PACK,archivo),os.path.join(DIR_AGREGADOS,archivo))
    print(f"\nArchivo {archivo} movido a {os.path.join(DIR_AGREGADOS,archivo)}")

def menu():
    op = 0
    print("\n\n\tArchivos para agregar a la cola de redis")
    print("------------------------------------------------------\n")

    for file in archivos_contenidos:
            

            print(f"\t{op} => {file}")
            op += 1

    print("------------------------------------------------------\n")
    opcion = int(input("opcion del archivo: "))
    return opcion

archivos_contenidos = os.listdir(DIR_PACK)



if len(archivos_contenidos) > 0:

    try:
        opcion = menu()

        archivo_a_listar = archivos_contenidos[opcion]

        cantidad = cargar_skus_from_file(archivo_a_listar)

        mover_archivo(archivo_a_listar)

        print(f"\n\nCantidad en el archivo {cantidad: ,.0f}")
        print(f"Cantidad en la cola de redis: {counts(): ,.0f}")

    except ValueError as e:
        print("\nError:", e)
        print("Error: la opcion ingresada es una letra, no un valor entero.")

    except Exception as e:
        print("\nError: ",e)
        print("Error: Indice fuera de rango, por favor ingresalo correctamente.")
        
        
else:
    print("No hay archivos en el directorio")


