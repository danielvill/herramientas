class Reporte:
    def __init__(self,id_p,empleado_p,cedula_p,codigo_p,nombreh_p,stock_p,fecha_p,fecha_pf,estado,comentario):
        self.id_p = id_p
        self.empleado_p = empleado_p
        self.cedula_p = cedula_p
        self.codigo_p = codigo_p
        self.nombreh_p = nombreh_p
        self.stock_p = stock_p
        self.fecha_p = fecha_p
        self.fecha_pf = fecha_pf
        self.estado = estado
        self.comentario = comentario

    def ReporteDBCollection(self):
        return{
            "id_p":self.id_p,
            "empleado_p":self.empleado_p,
            "cedula_p":self.cedula_p,
            "codigo_p":self.codigo_p,
            "nombreh_p":self.nombreh_p,
            "stock_p":self.stock_p,
            "fecha_p":self.fecha_p,
            "fecha_pf":self.fecha_pf,
            "estado":self.estado,
            "comentario":self.comentario,
        }