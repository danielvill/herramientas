class Empleados:
    def __init__(self,cedula,nombre,cargo,telefono):
        self.cedula=cedula
        self.nombre=nombre
        self.cargo=cargo
        self.telefono=telefono
        


    def EmpleadoDBCollection(self):
        return{
            "cedula":self.cedula,
            "nombre":self.nombre,
            "cargo":self.cargo,
            "telefono":self.telefono,
        }