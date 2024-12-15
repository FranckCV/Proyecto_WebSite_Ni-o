from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
import controladores.controlador_agrupacion as controlador_agrupacion
import controladores.controlador_participante as controlador_participante
import controladores.controlador_seleccion  as controlador_seleccion
import hashlib
import base64
import jwt
# from flask_socketio import SocketIO, emit 
from datetime import datetime, date
from clases.User import User
from clases.auth import token_required
import controladores.controlador_user as controlador_user

app = Flask(__name__, template_folder='templates')
app.secret_key = 'security_key'

def generalPage(page):
    return "general_pages/"+page


def adminPage(page):
    return "admin_pages/"+page

def check_token(funcion):
    token = session.get('token')
    if token:
        try:
            SECRET_KEY = "mi_super_secreto"
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            flash("Usted ya se encuentra registrado", "message")
            return redirect(url_for(f'{funcion}'))
        except jwt.ExpiredSignatureError:
            flash("Su sesión ha expirado, por favor inicie sesión nuevamente", "error")
            session.pop('token', None)
        except jwt.InvalidTokenError:
            flash("Token inválido, por favor inicie sesión nuevamente", "error")
            session.pop('token', None)
        return None

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
    redirection = check_token(funcion='dashboard')
    if redirection: return redirection
    response = make_response(render_template(adminPage("login.html")))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route("/sign_in", methods=['POST'])
def sign_in():
    
    username = request.form['username']
    password = request.form['password']
    response = controlador_user.login(username, password)
    if response["message"] == "success":
        session['token'] = response["data"]["token"]
        return redirect(url_for('dashboard'))
    flash("Credenciales inválidas", "error")
    return redirect(url_for('login'))

@app.route("/api_register_user", methods=['POST'])
def api_register_user():
    fullname = request.json['nombres_completos']
    username = request.json['usuario']
    password = request.json['clave']
    response = dict()
    try:
        controlador_user.register_user(fullname,username,password)
        response['data']={}
        response['message']="Registrado correctamente"
        response['status'] = 1
    except Exception as e:
        response['data']={}
        response['message']="Error al registrar: " + repr(e)
        response['status'] = -1

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





@app.route("/dashboard")
@token_required
def dashboard():
    token = session.get('token')
    user = controlador_user.get_user_by_token(token)
    print(user)
    resultados = controlador_participante.obtener_resultados()
    return render_template(adminPage("dashboard_reporte.html") , resultados = resultados)



@app.route("/buscarResultado")
def buscarResultado():
    nombreBusqueda = request.args.get("buscarElemento")
    resultados = controlador_participante.buscar_resultado_nombre(nombreBusqueda)
    return render_template(adminPage("dashboard_reporte.html") , resultados = resultados , nombreBusqueda = nombreBusqueda)

@app.route("/error")
def error_page():
    message = request.args.get('message', 'Error desconocido')
    return render_template(generalPage("error_page.html"), message=message)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
