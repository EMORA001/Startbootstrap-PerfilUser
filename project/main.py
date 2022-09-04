from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from base64 import b64encode
import sqlite3
from .models import Comments
from . import db

main = Blueprint('main', __name__)


@main.route('/index')
@login_required
def index():
    return render_template('index.html', user_name=current_user.fname, user_lname=current_user.lname, user_image=b64encode(current_user.imagen).decode("utf-8"))

@main.route('/login', methods=['POST'])
def ajax_login():
    print(request.form)
    email    = request.form.get('email')
    response = {'status':200,'email':email,'id':1}
    return jsonify(response)


@main.route('/myprofile')
@login_required
def myprofile():
    conn=sqlite3.connect("project/db.sqlite")
    c = conn.cursor()
    row=c.execute("SELECT * FROM Comments")
    resultado =c.fetchall()
    coment_user = []
    for res in resultado:
        if (res[1] == current_user.email):
            coment_user.append(res[2])
    conn.close()
    return render_template('myprofile.html', comentario = coment_user, email=current_user.email, user_name=current_user.fname, user_lname=current_user.lname, user_image=b64encode(current_user.imagen).decode("utf-8"))

