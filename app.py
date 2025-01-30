from flask import flash, Flask, json, send_file,session, render_template, request,Response ,jsonify, redirect, url_for
from bson import json_util
from controllers.database import Conexion as dbase
from datetime import datetime,timedelta #* Importacion de manejo de tiempo
from flask import jsonify
from reportlab.pdfgen import canvas # *pip install reportlab este es para imprimir reportes
from reportlab.lib.pagesizes import letter #* pip install reportlab 
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer ,Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet ,ParagraphStyle
from routes.empleados import empleados
from routes.herramientas import  herramientas
from routes.prestamo import prestamo
from routes.reporte import reporte
import os
# ! Puntos para instalar pip install flask-paginate flask pymongo reportlab pip install babel
# ! Codigo para que se ejecute 

db = dbase()
app = Flask(__name__)
app.secret_key = 'herramientas14526'
app.config['UPLOAD_FOLDER'] = 'D:/Herramientas/static/img'



@app.route('/crear_backup', methods=['POST'])
def crear_backup():
    # Obtén los datos de las colecciones 'empleados', 'herramientas' y 'reporte'
    empleados_data = db.empleados.find({}, {'_id': 0})  # Excluye el campo '_id'
    herramientas_data = db.herramientas.find({}, {'_id': 0})
    reporte_data = db.reporte.find({}, {'_id': 0})

    # Crea una carpeta para los respaldos (si no existe)
    backup_folder = 'backups'
    os.makedirs(backup_folder, exist_ok=True)

    # Genera nombres de archivo con la fecha actual
    fecha_actual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    empleados_filename = f'{backup_folder}/empleados_{fecha_actual}.json'
    herramientas_filename = f'{backup_folder}/herramientas_{fecha_actual}.json'
    reporte_filename = f'{backup_folder}/reporte_{fecha_actual}.json'

    # Guarda los datos en archivos JSON
    with open(empleados_filename, 'w') as empleados_file:
        for empleado in empleados_data:
            json.dump(empleado, empleados_file)
            empleados_file.write('\n')

    with open(herramientas_filename, 'w') as herramientas_file:
        for herramienta in herramientas_data:
            json.dump(herramienta, herramientas_file)
            herramientas_file.write('\n')

    with open(reporte_filename, 'w') as reporte_file:
        for reporte in reporte_data:
            json.dump(reporte, reporte_file)
            reporte_file.write('\n')
    flash("Respaldo hecho de manera efectiva revisar en la carpeta backups")
    return render_template('index.html')


# * Vista de Ingreso al sistema 
@app.route('/',methods=['GET','POST'])
def run():
    return render_template('index.html')


#* Este es para cerrar la sesion 
@app.route('/logout')
def logout():
    # Elimina el usuario de la sesión si está presente
    session.pop('username', None)
    return redirect(url_for('index'))


#* Vista Ingreso de admin y usuarios
@app.route('/index',methods=['GET','POST'])
def index():

    if request.method == 'POST':
        usuario = request.form['user']
        password = request.form['contraseña']
        usuario_fo = db.admin.find_one({'user':usuario,'contraseña':password})
        if usuario_fo:
            session["username"]= usuario
            return redirect(url_for('reporte.v_reporte'))
        else:
            flash("Contraseña incorrecta")
            return redirect(url_for('index'))
    else:
        return render_template('index.html')
    
#Vista de todo lo del sistema
@app.route("/admin/inicio",methods = ["GET", "POST"])
def inicio():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('herramientas.index'))
    herramientas = db["herramientas"].find()
    prestamo = db["prestamo"].find()
    prestadi = db["prestamo"].find()
    reporte = db["reporte"].find()
    reporte2 = db["reporte"].find()
    return render_template('admin/inicio.html', empleados=empleados, herramientas=herramientas, prestamo=prestamo,prestadi=prestadi
    ,reporte=reporte,reporte2= reporte2)

# *Codigo de ingreso de empleados
app.register_blueprint(empleados)

# * Codigo de ingreso de herramientas
app.register_blueprint(herramientas)

# * Codigo de ingreso de prestamos
app.register_blueprint(prestamo)

# * Codigo de ingreso de reportes

app.register_blueprint(reporte)

# *  Este es para manejo de errores
@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    return render_template('404.html', message=message), 404


if __name__ == '__main__':
    app.run(debug=True, port=4000)
