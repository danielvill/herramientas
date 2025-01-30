class Herramientas:
    def __init__(self,id_h,codigo,nombre_h,stock,comentario,imagen):
        self.id_h = id_h
        self.codigo = codigo
        self.nombre_h = nombre_h
        self.stock = stock
        self.comentario = comentario
        self.imagen = imagen
        


    def HerramientasDBCollection(self):
        return{
            "id_h":self.id_h,
            "codigo":self.codigo,
            "nombre_h":self.nombre_h,
            "stock":self.stock,
            "comentario":self.comentario,
            "imagen":self.imagen,
        }