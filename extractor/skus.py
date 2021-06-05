import pandas as pd
import math, os


base = os.path.dirname(os.path.realpath(__file__))
print(base)
lista = pd.read_excel(base + r"/skus.xlsx")

lista_skus = set(lista['asin'].to_list())


