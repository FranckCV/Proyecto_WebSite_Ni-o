from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
import controladores.controlador_agrupacion as controlador_agrupacion
import controladores.controlador_participante as controlador_participante
import controladores.controlador_seleccion  as controlador_seleccion
import hashlib
import base64
from flask_socketio import SocketIO, emit 
from datetime import datetime, date
from clases.User import User
import controladores.controlador_user as controlador_user

app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app)

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
    participante_id = request.cookies.get('id_participante_cookie')
    if participante_id:
        id_grupo = controlador_seleccion.obtener_ultima_seleccion(participante_id)
        verificado = controlador_seleccion.verificar_cantidad_seleccionada(participante_id,id_grupo)
        if id_grupo==28 and verificado:
            response = make_response(render_template(generalPage("index.html")))
            response.delete_cookie("id_participante_cookie")
            return response
        else:
            return redirect(url_for('pregunta', id_grupo=id_grupo)) 
    else:   
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

@app.route("/guardar_participante", methods=["POST"])
def guardar_participante():
    nombres = request.form["nombres"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    telefono = request.form["telefono"]
    correo = request.form["correo"]
    
    id_participante = controlador_participante.insertar_participante(
        nombres=nombres,
        fecha_nacimiento=fecha_nacimiento,
        telefono=telefono,
        correo=correo
    )
    
    id_grupo_inicial = 1
    
    respuesta = redirect(url_for('pregunta', id_grupo=id_grupo_inicial))
    respuesta.set_cookie('id_participante_cookie', str(id_participante))
    return respuesta

##############################################################################################################

@app.route("/pregunta=<int:id_grupo>")
def pregunta(id_grupo):
    participante_id = request.cookies.get('id_participante_cookie') 
    if participante_id:
        cualidades = controlador_agrupacion.obtener_cualidades(id_grupo)
        verificado = controlador_seleccion.verificar_cantidad_seleccionada(participante_id,id_grupo) 
        seleccion_positiva = controlador_seleccion.obtener_id_cualidad_positiva_seleccionada(participante_id,id_grupo) 
        print(seleccion_positiva)
        seleccion_negativa = controlador_seleccion.obtener_id_cualidad_negativa_seleccionada(participante_id,id_grupo)
        return render_template("pregunta.html", cualidades=cualidades, id_grupo=id_grupo , verificado=verificado,seleccion_negativa=seleccion_negativa,seleccion_positiva=seleccion_positiva )
    else:
        return redirect("/sign_up") 

@app.route("/seleccionar_positivo", methods=["POST"])
def seleccionar_positivo():
    participante_id = request.cookies.get('id_participante_cookie')
    grupo_id = request.form["grupo"]
    cualidad_id = request.form["positive"]
    estado = True
    mensaje = controlador_seleccion.insertar_seleccion(participante_id,grupo_id,cualidad_id,estado)
    print(mensaje)
    return redirect(request.referrer)

@app.route("/seleccionar_negativo" , methods=["POST"] )
def seleccionar_negativo():
    participante_id = request.cookies.get('id_participante_cookie')
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
    return redirect(url_for("pregunta", id_grupo=id_grupo))

@app.route("/colores")
def colores():
    return render_template(generalPage("colores.html"))

###############################################################################################################

@app.route("/resultado")
def resultado():
    participante_id = request.cookies.get('id_participante_cookie')

    if not participante_id:
        return "Error: No se encontró el ID del participante en la cookie.", 400
    
    try:
        participante_id = int(participante_id)
    except ValueError:
        return "Error: El ID del participante en la cookie no es válido.", 400
    
    print(participante_id)
    prueba = controlador_seleccion.llenar_grafico_barras(participante_id=participante_id)
    print(prueba)
    nombre_participante = controlador_participante.buscar_participante(id_participante=participante_id)
    print(nombre_participante[1])
    data = {
        "labels": [item[0] for item in prueba],
        "data": [int(item[1]) for item in prueba]
    }

    return render_template(generalPage("resultado.html"), data=data, nombre_participante=str(nombre_participante[1]))



# @app.route("/resultado_v2")
# def resultado_v2():
#     return render_template(generalPage("resultado_v2.html"))





# @app.route("/dashboard")
# def dashboard():
#     resultados = controlador_participante.obtener_resultados()
#     return render_template(adminPage("dashboard_reporte.html") , resultados = resultados)



# @app.route("/buscarResultado")
# def buscarResultado():
#     nombreBusqueda = request.args.get("buscarElemento")
#     resultados = controlador_participante.buscar_resultado_nombre(nombreBusqueda)
#     return render_template(adminPage("dashboard_reporte.html") , resultados = resultados , nombreBusqueda = nombreBusqueda)





@app.route("/dashboard")
def dashboard():
    # resultados = controlador_participante.obtener_resultados()
    return render_template(adminPage("dashboard_reporte.html"))


@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')


@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')


@socketio.on('get_tabla')
def handle_get_tabla():
    resultados = controlador_participante.obtener_resultados()
    emit("update_tabla",  {"resultados": resultados} , broadcast=True) 







# @app.route("/pruebas")
# def pruebas():
#     # elementos = controlador_participante.obtener_elementos()
#     return render_template("_no_borrar/_test.html")


# @socketio.on('connect')
# def handle_connect():
#     print('Cliente conectado')


# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Cliente desconectado')


# @socketio.on('get_tabla')
# def handle_get_tabla():
#     resultados = controlador_participante.obtener_elementos()
#     emit("update_tabla",  {"resultados": resultados} , broadcast=True) 







if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
