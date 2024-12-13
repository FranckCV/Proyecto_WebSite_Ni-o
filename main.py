from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
import controladores.controlador_agrupacion as controlador_agrupacion
import controladores.controlador_participante as controlador_participante
import hashlib
import base64
from datetime import datetime, date

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


@app.route("/sign_up")
def sign_up():
    return render_template(generalPage("sign_up.html"))


@app.route("/colores")
def colores():
    return render_template(generalPage("colores.html"))




@app.route("/pregunta=<int:id_grupo>")
def pregunta(id_grupo):
    cualidades = controlador_agrupacion.obtener_cualidades(id_grupo)
    return render_template("pregunta.html", cualidades=cualidades , id_grupo=id_grupo)

@app.route("/resultado")
def resultado():
    return render_template(generalPage("resultado.html"))

# @app.route("/resultado_v2")
# def resultado_v2():
#     return render_template(generalPage("resultado_v2.html"))





@app.route("/dashboard")
def dashboard():
    resultados = controlador_participante.obtener_resultados()
    return render_template(adminPage("dashboard_reporte.html") , resultados = resultados)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
