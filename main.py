from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
import hashlib
import base64
from datetime import datetime, date
from clases.User import User
import controladores.controlador_user as controlador_user

app = Flask(__name__, template_folder='templates')

def generalPage(page):
    return "general_pages/"+page

def adminPage(page):
    return "admin_pages/"+page

def encriptar(texto):
    btexto = texto.encode('utf-8')
    objHash = hashlib.sha256(btexto)
    texto_encriptado = objHash.hexdigest()
    return texto_encriptado


@app.route("/")
def index():
    return render_template(generalPage("index.html"))


@app.route("/login")
def login():
    return render_template(adminPage("login.html"))

@app.route("/sign_in", methods=['POST'])
def sign_in():
    username = request.form['username']
    password = request.form['password']
    
    if not username or not password:
        return jsonify({"error": "Faltan credenciales"}), 400

    response = controlador_user.login(username, password)
    return jsonify(response)


@app.route("/sign_up")
def sign_up():
    return render_template(generalPage("sign_up.html"))


@app.route("/colores")
def colores():
    return render_template(generalPage("colores.html"))

@app.route("/pregunta")
def pregunta():
    return render_template(generalPage("pregunta.html"))



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
