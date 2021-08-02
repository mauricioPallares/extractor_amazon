import mysql.connector
import json
import configuraciones as conf


con = mysql.connector.connect(
    host = conf.DB['host'],
    user = conf.DB['user'],
    password = conf.DB['password'],
    database = conf.DB['database'],
)

cursor = con.cursor( dictionary=True)

class Producto(object):


    def __init__(self, sku = None, titulo = None, titulo_default = None, precio = None, marca = None, disponibilidad = None, stock = None, descripcion = None, caracteristicas = None, imagenes = ["","",""], peso = None, tabla = "productos"):
        super(Producto, self).__init__()
        self.__sku = sku
        self.__titulo = titulo
        self.__titulo_default = titulo_default
        self.__precio = precio
        self.__marca = marca
        self.__disponibilidad = disponibilidad
        self.__stock = stock
        self.__descripcion = descripcion
        self.__caracteristicas = caracteristicas
        self.__imagenes = imagenes
        self.__peso = peso

        self.__tabla = tabla

    @property
    def sku(self):
        return self.__sku
    
    @sku.setter
    def sku(self, sku):
        self.__sku = sku
    
    @property
    def titulo(self):
        return self.__titulo
    @property
    def tituloDefault(self):
        return self.__titulo_default
    
    @tituloDefault.setter
    def tituloDefault(self, tituloDefault):
        self.__titulo_default = tituloDefault

    @titulo.setter
    def titulo(self, titulo):
        self.__titulo = titulo

    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self, precio):
        self.__precio = precio
    
    @property
    def marca(self):
        return self.__marca
    
    @marca.setter
    def marca(self, marca):
        self.__marca = marca
    
    @property
    def disponibilidad(self):
        return self.__disponibilidad

    @disponibilidad.setter
    def disponibilidad(self, disponibilidad):
        self.__disponibilidad = disponibilidad
    @property
    def stock(self):
        return self.__stock
    
    @stock.setter
    def stock(self, stock):
        self.__stock = stock
        
    @property
    def descripcion(self):
        return self.__descripcion
    
    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion

    @property
    def caracteristicas(self):
        return self.__caracteristicas
    
    @caracteristicas.setter
    def caracteristicas(self, caracteristicas):
        self.__caracteristicas = caracteristicas
    
    @property
    def imagenes(self):
        return self.__imagenes
    @property
    def tabla(self):
        return self.__tabla
    
    @tabla.setter
    def tabla(self, tabla):
        self.__tabla = tabla
        
    @imagenes.setter
    def imagenes(self, imagenes):
        self.__imagenes = imagenes
    
    @property
    def peso(self):
        return self.__peso
    
    @peso.setter
    def peso(self, peso):
        self.__peso = peso

    def guardar(self):
        # sql = """
        # INSERT IGNORE INTO 
        #     %s (sku, titulo, titulo_default, precio, marca, disponibilidad,stock, descripcion, caracteristicas, peso, imagenes) 
        # VALUES 
        #     (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        sql = f"""
        INSERT IGNORE INTO 
            {self.__tabla} (sku, titulo, precio, marca, disponibilidad,stock, descripcion, caracteristicas, peso, imagenes) 
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        cursor.execute(sql,(
        
        self.__sku,
        self.__titulo,
        # self.__titulo_default,
        self.__precio,
        self.__marca,
        self.__disponibilidad,
        self.__stock,
        self.__descripcion,
        self.__caracteristicas,
        self.__peso,
        " ".join(self.__imagenes),
        ))

        con.commit()
    
    def actualizar(self):
        sql = f"UPDATE {self.__tabla} SET precio = %s , disponibilidad = %s WHERE sku = %s"
        

        cursor.execute(sql, (
            self.__precio,
            self.__disponibilidad,
            self.__sku
        ))

        con.commit()
    def act_disp(self):
        sql = f"UPDATE {self.__tabla} SET disponibilidad = %s, stock = %s WHERE sku = %s"

        cursor.execute(sql, (
            self.__disponibilidad,
            self.__stock,
            self.__sku
        ))

        con.commit()

    def actualizar_stock(self):
        
        sql = "UPDATE producto SET precio = %s , inStock = %s WHERE sku = %s"

        stock = 1 if self.__stock == "En Stock" else 0

        cursor.execute(sql, (
            self.__precio,
            stock,
            self.__sku
        ))

        con.commit()

    def __repr__(self):
        return json.dumps(self.__dict__, indent=2, separators=(',', ' : '))

    @staticmethod
    def esta_en_DB(sku, tabla):
        sql = f"SELECT sku FROM {tabla} WHERE sku=%s"
        val = (sku,)
        cursor.execute(sql, val)
        data = cursor.fetchone()        
        if data:
            return True
        else:
            return False
    
    def act_precio(self)-> str:
        sql = f"UPDATE {self.__tabla} SET precio = %s WHERE sku = %s"
        cursor.execute(sql, (
            
            self.__precio,
            self.__sku
        ))

        con.commit()
        


# def get_stock(disponibilidad):
#     stock = None

#     for dip in disponibilidad_true:
#         if disponibilidad.lower().startswith(dip.lower()):
#             stock = "En Stock"
#             break

    
#     for dip in disponibilidad_false:
#         if disponibilidad.lower().startswith(dip.lower()):
#             stock = "Sin Stock"
#             break

#     if not stock:
#         if disponibilidad == "":
#             stock = "Sin Stock"

#     if not stock:
#         if disponibilidad.lower().startswith("only"):
#             cant = [int(s) for s in disponibilidad.split() if s.isdigit()]
#             if cant[0] >= cantidad_minima:

#                 stock = "En Stock"
#             else:
#                 stock = "Sin Stock"

#     return stock

if __name__ == "__main__":

    print(Producto.esta_en_DB("024370349X", "productos_junior"))

    p = Producto()

    p.sku = "024370349X"
    p.precio = "18.90"
    p.stock = "En Stock"
    p.tabla = "productos_junior"

    print(p)
    p.guardar()