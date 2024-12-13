from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
import controladores.controlador_agrupacion as controlador_agrupacion
import controladores.controlador_participante as controlador_participante
import controladores.controlador_seleccion  as controlador_seleccion
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


##############################################################################################################

@app.route("/pregunta=<int:id_grupo>")
def pregunta(id_grupo):
    cualidades = controlador_agrupacion.obtener_cualidades(id_grupo)
    return render_template("pregunta.html", cualidades=cualidades , id_grupo=id_grupo)

@app.route("/seleccionar_positivo", methods=["POST"])
def seleccionar_positivo():
    participante_id = 1
    grupo_id = request.form["grupo"]
    cualidad_id = request.form["positive"]
    estado = True
    mensaje = controlador_seleccion.insertar_seleccion(participante_id,grupo_id,cualidad_id,estado)
    print(mensaje)
    return redirect(request.referrer)

@app.route("/seleccionar_negativo" , methods=["POST"] )
def seleccionar_negativo():
    participante_id = 1
    grupo_id = request.form["grupo"]
    cualidad_id = request.form["negative"]
    estado = False
    mensaje = controlador_seleccion.insertar_seleccion(participante_id,grupo_id,cualidad_id,estado)
    print(mensaje)
    return redirect(request.referrer)

@app.route("/siguiente_pregunta", methods=["POST"])
def siguiente_pregunta():
    id_grupo_actual = int(request.form["grupo"])
    id_grupo = id_grupo_actual + 1
    return redirect(url_for("pregunta", id_grupo=id_grupo))

@app.route("/pregunta_anterior", methods=["POST"])
def pregunta_anterior():
    id_grupo_actual = int(request.form["grupo"])
    id_grupo = id_grupo_actual - 1
    cualidades = controlador_agrupacion.obtener_cualidades(id_grupo)
    return redirect(url_for("pregunta", id_grupo=id_grupo))

###############################################################################################################

@app.route("/resultado")
def resultado():
    prueba = list(controlador_agrupacion.funcion_prueba_jpd())
    print(prueba)
    data = {
        "labels": [prueba[3][1], prueba[0][1], prueba[1][1], prueba[2][1]],
        "data": [prueba[3][2], prueba[0][2], prueba[1][2], prueba[2][2]]
    }
    return render_template(generalPage("resultado.html"), data=data)



# @app.route("/resultado_v2")
# def resultado_v2():
#     return render_template(generalPage("resultado_v2.html"))





@app.route("/dashboard")
def dashboard():
    resultados = controlador_participante.obtener_resultados()
    return render_template(adminPage("dashboard_reporte.html") , resultados = resultados)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
