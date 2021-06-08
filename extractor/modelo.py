import mysql.connector

import configuraciones as conf

con = mysql.connector.connect(
    host = conf.DB['host'],
    user = conf.DB['user'],
    password = conf.DB['password'],
    database = conf.DB['database'],
)

cursor = con.cursor()

class Producto(object):

    def __init__(self, producto):
        super(Producto, self).__init__()
        self.sku = producto['sku']
        self.titulo = producto['titulo']
        self.precio = producto['precio']
        self.marca = producto['marca']
        self.disponibilidad = producto['disponibilidad']
        self.descripcion = producto['descripcion']
        self.caracteristicas = producto['caracteristicas']
        self.imagenes = producto['imagenes']
        self.peso = producto['peso']

    def guardar(self):
        sql = """
        INSERT IGNORE INTO 
            productos_andres (sku, titulo, precio, marca, disponibilidad, descripcion, caracteristicas, peso, imagenes) 
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        cursor.execute(sql,(
        self.sku,
        self.titulo,
        self.precio,
        self.marca,
        self.disponibilidad,
        self.descripcion,
        self.caracteristicas,
        self.peso,
        " ".join(self.imagenes),
        ))

        con.commit()

    @staticmethod
    def esta_en_DB(sku):
        sql = "SELECT sku FROM productos_andres WHERE sku=%s"
        val = (sku,)
        cursor.execute(sql, val)
        data = cursor.fetchone()        
        if data:
            return True
        else:
            return False

