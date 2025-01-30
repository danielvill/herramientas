from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.empleados import Empleados
from pymongo import MongoClient
db = dbase()
empleados = Blueprint('empleados', __name__)


@empleados.route('/admin/in_empleados',methods=['GET','POST'])
def inem():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('empleados.index'))  # Redirige al usuario al inicio si no está en la sesión
    
    if request.method == 'POST':
        empleados = db["empleados"]
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        cargo = request.form['cargo']
        telefono = request.form['telefono']
    
        exist_cedula = empleados.find_one ({"cedula":cedula})
        exist_nombre = empleados.find_one ({"nombre":nombre})
        exist_telefono = empleados.find_one ({"telefono":telefono})

        if exist_cedula:
            flash("La cedula ya existe")
            return redirect(url_for('empleados.inem'))
        elif exist_nombre:
            flash("El nombre ya existe")
            return redirect(url_for('empleados.inem'))
        elif exist_telefono:
            flash("El telefono ya existe")
            return redirect(url_for('empleados.inem'))
        else:
            empleado = Empleados(cedula,nombre,cargo,telefono)
            empleados.insert_one(empleado.EmpleadoDBCollection())
            flash("Enviado a la base de datos")
            return redirect(url_for('empleados.inem'))
    else:
        return render_template('admin/in_empleados.html')

# Editar Usuario
@empleados.route('/edit_us/<string:edaduser>', methods=['GET', 'POST'])#
def edit_user(edaduser):
    empleados = db['empleados']
    cedula = request.form['cedula']
    nombre = request.form['nombre']
    cargo = request.form['cargo']
    telefono = request.form['telefono']
    
    if cedula and nombre and cargo and telefono:
        empleados.update_one({'cedula' : edaduser}, {'$set' : {'cedula' : cedula, 'nombre' : nombre, 'cargo':cargo,'telefono':telefono}})
        flash("Empleado " + nombre + " con cedula " + cedula +  "editado correctamente")
        return redirect(url_for('empleados.v_user'))
    else:
        return render_template('admin/empleados.html')
    
# * Eliminar Usuarios
@empleados.route('/delete_us/<string:eliaduser>')
def delete_us(eliaduser):#Pasa la funcion al form osea al boton
    empleados = db['empleados']
    documento = empleados.find_one({"cedula":eliaduser})
    nombre = documento["nombre"]
    cedula = documento["cedula"]
    empleados.delete_one({'cedula' : eliaduser})
    flash("Empleado "+ nombre + ' con cedula '+ cedula + " eliminado con exito ")
    return redirect(url_for('empleados.v_user'))

# *Visualizar usuario
@empleados.route("/admin/empleados")
def v_user():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('empleado.index'))
    empleados = db['empleados'].find()
    return render_template('admin/empleados.html', empleados=empleados)
