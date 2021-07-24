from modelo import con, cursor
from helpers import enCola

sql = "SELECT sku, disponibilidad FROM productos_paula where disponibilidad=''" 

cursor.execute(sql)

data = cursor.fetchall()

for i in data:
    print(i['sku'], " Ingresado")
    enCola("upd_dips", i['sku'])