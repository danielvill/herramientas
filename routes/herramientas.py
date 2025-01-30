from flask import Blueprint, render_template, request, flash, session, redirect, url_for,send_file ,current_app
from controllers.database import Conexion as dbase
from werkzeug.utils import secure_filename # Archivo que se tiene que importar
import os # Tambien este codigo se tiene que agregar
from modules.herramientas import Herramientas
from pymongo import MongoClient
from reportlab.pdfgen import canvas # *pip install reportlab este es para imprimir reportes
from reportlab.lib.pagesizes import letter #* pip install reportlab 
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer ,Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet ,ParagraphStyle


db = dbase()
herramientas = Blueprint('herramientas', __name__)

@herramientas.route('/alguna_ruta')
def alguna_funcion():
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    
# codigo de verificacion de herramientas con las imagenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}



# Este codigo es para las  imagenes
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_next_sequence(name): 
    seq = db.seqs.find_one({'_id': name})
    if seq is None:
        # Inicializa 'productoId' en 220 si no existe
        db.seqs.insert_one({'_id': 'productoId', 'seq': 0})
        seq = db.seqs.find_one({'_id': name})

    result = db.seqs.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},# Aqui tambien le puedes cambiar para que empieze con otro valor 
        return_document=True
    )
    return result.get('seq')

# * Ingresar Herramientas
@herramientas.route('/admin/in_herramientas',methods=['GET', 'POST'])
def inherra():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('herramientas.index'))
    
    try:
        if request.method == 'POST':
            id_h = 'A' + str(get_next_sequence('productoId')).zfill(3) #esta parte del codigo cambiaba todo
            herramienta = db['herramientas']
            codigo = request.form['codigo']
            nombre_h= request.form['nombre_h']
            stock = request.form['stock']
            comentario = request.form['comentario']

            exist_id_h = herramienta.find_one({"id_h":id_h})
            exist_codigo = herramienta.find_one({"codigo":codigo}) 
            exist_nombre_h = herramienta.find_one({"nombre_h":nombre_h})

            if exist_nombre_h:
                flash("El nombre de la herramienta ya existe")
                return redirect(url_for('herramientas.inherra'))
            elif exist_codigo:
                flash("El codigo de la herramienta ya existe")
                return redirect(url_for('herramientas.inherra'))
            elif exist_id_h:
                flash("El id de la herramienta ya existe")
                return redirect(url_for('herramientas.inherra'))
            else:
                # Aquí es donde manejarías la carga de archivos
                if 'imagen' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                file = request.files['imagen']
                if file.filename == '':
                    flash('Selecciona una imagen')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    # Guarda solo el nombre del archivo en la base de datos
                    imagen_filename = os.path.join('img', filename)
                    herramienta_instancia = Herramientas(id_h, codigo, nombre_h, stock, comentario, filename)
                    herramienta.insert_one(herramienta_instancia.__dict__)
                    flash("Herramienta agregada con exito")
                    return redirect(url_for('herramientas.inherra'))
                else:
                    flash('Solo archivos con estas extensiones permite el sistema jpg , png , jpeg')
                    return redirect(request.url)
        else:
            return render_template('admin/in_herramientas.html')
    except Exception as e:
        print(e)
        flash(str(e)) 
        return redirect(url_for('herramientas.inherra'))

# * Editar Herramienta
@herramientas.route('/edit_pr/<string:edadpro>', methods=['GET', 'POST'])
def edit_pros(edadpro):
    herramienta = db['herramientas']
    id_h = edadpro
    codigo = request.form["codigo"]
    nombre_h = request.form["nombre_h"]
    stock = request.form["stock"]
    comentario = request.form["comentario"]
    # Encuentra la herramienta existente para obtener el nombre de la imagen actual
    herramienta_existente = herramienta.find_one({"id_h": edadpro})

    if 'imagen' in request.files and request.files['imagen'].filename != '':
        file = request.files['imagen']
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    else:
        # Si no se carga una nueva imagen, usa el nombre de la imagen existente
        filename = herramienta_existente['imagen']
    
    campos = [id_h, codigo, nombre_h, stock, comentario, filename]

    try:
        if all(campos):
            herramienta.update_one(
                {"id_h": edadpro},
                {
                    "$set": {
                        "id_h": id_h,
                        "codigo": codigo,
                        "nombre_h": nombre_h,
                        "stock": stock,
                        "comentario": comentario,
                        "imagen": filename,
                    }
                }
            )
            flash("Herramienta con " + codigo + " actualizada con exito" )
            return redirect(url_for('herramientas.v_producto'))
        else:
            flash("Todos los campos son obligatorios")
            return redirect(url_for('herramientas.edit_pros', edadpro=edadpro))
    except Exception as e:
        print(e)
        flash("Ha ocurrido un error")




#  * Eliminar Herramienta
@herramientas.route('/delete_pr/<string:eliadpro>')
def delete_pro(eliadpro):
    herramienta = db['herramientas']
    documento = herramienta.find_one({"id_h":eliadpro})
    prod = documento["nombre_h"]
    cod = documento["codigo"]
    herramienta.delete_one({'id_h':eliadpro})
    flash('Herramienta con  codigo '+cod+ " y nombre "+ prod + " eliminado correctamente")
    return redirect(url_for('herramientas.v_producto'))


# * Vista de productos 
@herramientas.route("/admin/herramientas")
def v_producto():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('herramientas.index'))
    herramientas = db['herramientas'].find()
    return render_template('admin/herramientas.html', herramientas=herramientas)

