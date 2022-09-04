from flask import Blueprint, render_template, redirect, url_for, request, flash,jsonify
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from base64 import b64encode
import sqlite3
from .models import User
from project.models import Comments
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email    = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # Compruebe si el usuario realmente existe
    # tomar la contraseña proporcionada por el usuario, codificarla y compararla con la contraseña codificada en la base de datos
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # si el usuario no existe o la contraseña es incorrecta, vuelva a cargar la página

    # si la verificación anterior pasa, entonces sabemos que el usuario tiene las credenciales correctas
    login_user(user, remember=remember)

    # si la verificación anterior pasa, entonces sabemos que el usuario tiene las credenciales correctas
    print("entroa la base",email)
    return redirect(url_for('auth.comments'))

@auth.route('/register')
def register():
    return render_template('register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    email    = request.form.get('email')
    fname    = request.form.get('fname')
    lname    = request.form.get('lname')
    password = request.form.get('password')
    imagen   = request.files['file'].read()
    
    user = User.query.filter_by(email=email).first() # si esto devuelve un usuario, entonces el correo electrónico ya existe en la base de datos

    if user: # si se encuentra un usuario, queremos redirigirlo a la página de registro para que el usuario pueda volver a intentarlo
        flash('Email address already exists')
        return redirect(url_for('auth.register'))

    # crear un nuevo usuario con los datos del formulario.
    new_user = User(email=email, 
                    fname=fname, 
                    lname=lname,
                    password=generate_password_hash(password, method='sha256'),
                    imagen=imagen)

    # Agregar el nuevo usuario a la base de datos
    db.session.add(new_user)
    db.session.commit()

    flash('Your account was created successfully.')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))



@auth.route('/comments')
@login_required
def comments():       
    conn=sqlite3.connect("project/db.sqlite")
    c = conn.cursor()
    row=c.execute("SELECT * FROM Comments")
    resultado =c.fetchall()
    coment_user = []
    for res in resultado:
        if (res[1] == current_user.email):
            coment_user.append(res[2]) 
    conn.close()
    return render_template('comments.html',comentario = coment_user, user_name=current_user.fname, user_lname=current_user.lname, user_image=b64encode(current_user.imagen).decode("utf-8"))


@auth.route('/comments', methods=['POST'])
def comments_post():
    comentario  = request.form.get('comentario')
    user_email   = current_user.email
    tablaComments = Comments(comentario=comentario,user_email=user_email)
    db.session.add(tablaComments)
    db.session.commit()
    response = {'status':200,'email':user_email,'id':1}
    return  redirect(url_for('auth.comments'))





@auth.route("/myprofile", methods=['POST'])
def myprofile_post():
    fname  = request.form.get('nombre')
    lname  = request.form.get('apellido')
    imagen = request.files['file'].read()
    password = request.form.get('clave')
       
    password = request.form.get('clave')
    User.query.filter_by(id=current_user.id).update(dict(fname=fname, lname=lname, imagen=imagen, password=generate_password_hash(password, method='sha256')))
    db.session.commit()
    return redirect(url_for('main.myprofile'))


