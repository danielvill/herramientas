from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.prestamo import Prestamo
from modules.reporte import Reporte
from pymongo import MongoClient
from datetime import datetime
from babel.dates import format_datetime
import locale

db = dbase()
prestamo = Blueprint('prestamo', __name__)
reporte = Blueprint('reporte', __name__)
# Establece la configuración regional en español
locale.setlocale(locale.LC_TIME, 'es_ES')

# Funcion para hacer un id autoincremntable 
def get_next_sequence(name):
    seq = db.seqs.find_one({'_id': name})
    if seq is None:
        # Inicializa 'productoId' si no existe
        db.seqs.insert_one({'_id': 'stockId', 'seq': 0})
        seq = db.seqs.find_one({'_id': name})

    result = db.seqs.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return result.get('seq')


@prestamo.route('/admin/in_prestamo',methods=['GET','POST'])
def prest():
    stock = 1
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('prestamo.index'))
    # Empleados
    empleados = db["empleados"].find()
    herramientas = db["herramientas"].find()

    if request.method == 'POST':
        prestamo = db['prestamo']        
        id_p = (get_next_sequence('stockId'))
        empleado_p = request.form['empleado_p']
        cedula_p = request.form['cedula_p']
        codigo_p = request.form['codigo_p']
        nombreh_p = request.form['nombreh_p']
        stock_p = request.form['stock_p']
        id_h = request.form['id_h'] 
        # Formatear fecha
        fecha_dt = request.form['fecha_p']
        fecha_pt =datetime.strptime(fecha_dt, '%Y-%m-%dT%H:%M')
        fecha_p = format_datetime(fecha_pt, locale='es_ES',format='full') # Formatear la fecha para que salga de esta forma
        
        fecha_pf = request.form['fecha_pf']
        estado = request.form['estado']
        comentario = request.form['comentario'] 
        # Validar que los campos no estén vacíos
        campos_vacios = any(not request.form[field].strip() for field in ['empleado_p', 'cedula_p', 'codigo_p', 'nombreh_p', 'stock_p', 'id_h', 'fecha_p', 'estado', 'comentario'])
        
        if campos_vacios:
            flash("Todos los campos son obligatorios.")
            return redirect(url_for('prestamo.prest'))
        else:
            actualizacion = int (stock_p) - int (stock)
            db.herramientas.update_one({"id_h":id_h},{"$set":{"stock":actualizacion}})
            prestamo.insert_one(Prestamo(id_p,empleado_p,cedula_p,codigo_p,nombreh_p,stock_p,id_h,fecha_p,fecha_pf,estado,comentario).PrestamoDBCollection())
            flash("Prestamo registrado con exito")
            return redirect(url_for('prestamo.prest'))
    else:
        return render_template('admin/in_prestamo.html',empleados=empleados,herramientas=herramientas)


# *Visualizar prestamo
@prestamo.route("/admin/prestamo",methods=['GET','POST'])
def v_pre():
    prestamos_cursor = db['prestamo'].find()  # Cursor 
    stock =0
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('prestamo.index'))
    if request.method == 'POST':  
        prestamo = db['prestamo']
        report = db['reporte']
        id_p = int(request.form['id_p']) 
        id_h = request.form['id_h']
        empleado_p = request.form['empleado_p']
        cedula_p = request.form['cedula_p']
        codigo_p = request.form['codigo_p']
        nombreh_p = request.form['nombreh_p']
        stock_p = request.form['stock_p']
        fecha_p = request.form['fecha_p']
        # Formatear la fecha de finalziacion
        fecha_ft = request.form['fecha_pf']
        
        

        estado = request.form['estado']
        comentario = request.form['comentario']
        
        if fecha_ft:  # Verifica si fecha_pf no está vacío
                fecha_pft =datetime.strptime(fecha_ft, '%Y-%m-%dT%H:%M')          
                fecha_pf = format_datetime(fecha_pft, locale='es_ES',format='full')
                report.insert_one(Reporte(id_p,empleado_p,cedula_p,codigo_p,nombreh_p,stock_p,fecha_p,fecha_pf,estado,comentario).ReporteDBCollection())
                prestamo.delete_one({'id_p' : id_p})  # Eliminar De prestamo
                actual = int(stock_p) + int (stock)
                db.herramientas.update_one({"id_h":id_h},{"$set":{"stock":actual}})
                flash("Nombre " + empleado_p + " con fecha finalizada " + fecha_pf)
                return redirect(url_for('prestamo.v_pre'))
        else:
            flash("Ingresa la fecha de finalización del préstamo")  # Mensaje si fecha_pf está vacío
    
    return render_template('admin/prestamo.html', prestamo=prestamos_cursor)


# * Reporte en PDF para lo que es para el sis
