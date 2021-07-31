from modelo import con, cursor
from helpers import enCola
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


def stock(disp: str = "") -> str:
    stock = None
    for dip in disponibilidad_true:
        if disp.lower().startswith(dip.lower()):
            stock = "En Stock"
            break
    for dip in disponibilidad_false:
        if disp.lower().startswith(dip.lower()):
            stock = "Sin Stock"
            break
    if not stock:
        if disp == "":
            stock = "Sin Stock"
    if not stock:
        if disp.lower().startswith("only"):
            cant = [int(s)
                    for s in disp.split() if s.isdigit()]
            if cant[0] >= cantidad_minima:
                stock = "En Stock"
            else:
                stock = "Sin Stock"
    return stock

sql = """SELECT sku, disponibilidad, stock, precio FROM productos_andres_descarga 
where (precio != 'Precio no encontrado') 
and disponibilidad = 'Disponibilidad no encontrada';"""

cursor.execute(sql)

data = cursor.fetchall()
print(len(data))
for i in data:
    print(i['sku'])
    sql = "UPDATE productos_andres_descarga  SET stock = %s, disponibilidad = %s WHERE sku = %s"

    cursor.execute(sql, (
        "En Stock",
        "In Stock.",
        i['sku']
    ))
    con.commit()

# sql = "SELECT sku, disponibilidad FROM productos_paula"

# cursor.execute(sql)

# data = cursor.fetchall()

# for i in data:
#     print(i['sku'], " ", stock(i['disponibilidad']))
#     sql = "UPDATE productos_paula SET stock = %s WHERE sku = %s"

#     cursor.execute(sql, (
#         stock(i['disponibilidad']),
#         i['sku']
#     ))
#     con.commit()