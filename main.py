from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
import controladores.controlador_agrupacion as controlador_agrupacion
import controladores.controlador_participante as controlador_participante
import controladores.controlador_seleccion  as controlador_seleccion
import hashlib
import base64
import clases.encriptar_cookie as encriptacion
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
    
def check_back_option(template):
    response = make_response(render_template(adminPage(f"{template}")))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

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
    response = check_back_option("login.html")
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
    apellidos = request.form["apellidos"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    telefono = request.form["telefono"]
    correo = request.form["correo"]
    
    id_participante = controlador_participante.insertar_participante(
        nombres=nombres,
        apellidos=apellidos,
        fecha_nacimiento=fecha_nacimiento,
        telefono=telefono,
        correo=correo
    )
    
    if not isinstance(id_participante, int):
        return redirect(url_for('error_page', message='No se pudo guardar el participante. Por favor, intente nuevamente.'))
    
    hash_id = encriptacion.generar_hash(id_participante)
    cookie_valor = f"{id_participante}:{hash_id}"
    
    id_grupo_inicial = 1
    
    respuesta = redirect(url_for('pregunta', id_grupo=id_grupo_inicial))
    respuesta.set_cookie('id_participante_cookie', cookie_valor)
    return respuesta

##############################################################################################################

# @app.route("/pregunta=<int:id_grupo>")
# def pregunta(id_grupo):
#     participante_id = request.cookies.get('id_participante_cookie') 
#     if participante_id:
#         cualidades = controlador_agrupacion.obtener_cualidades(id_grupo)
#         verificado = controlador_seleccion.verificar_cantidad_seleccionada(participante_id,id_grupo) 
#         seleccion_positiva = controlador_seleccion.obtener_id_cualidad_positiva_seleccionada(participante_id,id_grupo) 
#         print(seleccion_positiva)
#         seleccion_negativa = controlador_seleccion.obtener_id_cualidad_negativa_seleccionada(participante_id,id_grupo)
#         return render_template("pregunta.html", cualidades=cualidades, id_grupo=id_grupo , verificado=verificado,seleccion_negativa=seleccion_negativa,seleccion_positiva=seleccion_positiva )
#     else:
#         return redirect("/sign_up") 

@app.route("/pregunta=<int:id_grupo>")
def pregunta(id_grupo):
    participante_cookie = request.cookies.get('id_participante_cookie')
    
    if participante_cookie:
        respuesta = make_response(render_template(
            "pregunta.html", 
            cualidades=controlador_agrupacion.obtener_cualidades(id_grupo),
            id_grupo=id_grupo,
            verificado=controlador_seleccion.verificar_cantidad_seleccionada(participante_cookie, id_grupo),
            seleccion_positiva=controlador_seleccion.obtener_id_cualidad_positiva_seleccionada(participante_cookie, id_grupo),
            seleccion_negativa=controlador_seleccion.obtener_id_cualidad_negativa_seleccionada(participante_cookie, id_grupo)
        ))
        respuesta.set_cookie("id_grupo_cookie", str(id_grupo))
        return respuesta
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
    participante_cookie = request.cookies.get('id_participante_cookie')
    id_grupo_cookie = request.cookies.get('id_grupo_cookie')  # Obtener el último grupo visitado

    if not participante_cookie:
        return "Error: No se encontró el ID del participante en la cookie.", 400

    try:
        participante_id, hash_recibido = participante_cookie.split(":")
    except ValueError:
        return "Error: La cookie está mal formada.", 400

    if not encriptacion.verificar_hash(participante_id, hash_recibido):
        return "Error: La cookie no es válida.", 400

    try:
        participante_id = int(participante_id)
    except ValueError:
        return "Error: El ID del participante en la cookie no es válido.", 400

    cantidad_selecciones = controlador_seleccion.contar_selecciones_por_participante(participante_id)
    if cantidad_selecciones != 56:
        if id_grupo_cookie:
            return redirect(url_for('pregunta', id_grupo=int(id_grupo_cookie)))
        else:
            return "Error: No se puede determinar el grupo al que redirigir.", 400

    prueba = controlador_seleccion.llenar_grafico_barras(participante_id=participante_id)
    nombre_participante = controlador_participante.buscar_participante(id_participante=participante_id)
    nombre_completo = nombre_participante[1] + " " + nombre_participante[2]
    data = {
        "labels": [item[0] for item in prueba],
        "data": [int(item[1]) for item in prueba]
    }

    return render_template(generalPage("resultado.html"), data=data, nombre_participante=str(nombre_completo))


# @app.route("/resultado_v2")
# def resultado_v2():
#     return render_template(generalPage("resultado_v2.html"))





@app.route("/dashboard")
@token_required
def dashboard():
    response = check_back_option("dashboard_reporte.html")

    cant_max_progreso = controlador_agrupacion.obtener_cantidad_maxima_progreso() 
    resultados = controlador_participante.obtener_resultados()
    user_info = controlador_user.get_admin_by_token(session.get('token'))
    user_info_0 , user_info_1 , user_info_2  = user_info
    response.set_data(render_template(adminPage("dashboard_reporte.html"), resultados = resultados , cant_max_progreso = cant_max_progreso , user_info_1 = user_info_1 , user_info_2 = user_info_2))
    return response


@app.route("/buscarResultado")
# @token_required
def buscarResultado():
    nombreBusqueda = request.args.get("buscarElemento")
    user_info = controlador_user.get_user_by_token(session.get('token')).to_dict()
    resultados = controlador_participante.buscar_resultado_nombre(nombreBusqueda)
    cant_max_progreso = controlador_agrupacion.obtener_cantidad_maxima_progreso() 

    return render_template(adminPage("dashboard_reporte.html") , resultados = resultados , nombreBusqueda = nombreBusqueda , cant_max_progreso = cant_max_progreso , user_info = user_info)



@app.route("/eliminar_cliente", methods=["POST"])
def eliminar_info_participante():
    par_id = request.form["par_id"]
    controlador_seleccion.eliminar_seleccion_idpar(par_id)
    controlador_participante.eliminar_participante_id(par_id)
    return redirect("/dashboard")



@app.route("/ver_informacion=<int:id>")
# @token_required
def ver_informacion(id):
    user_info = controlador_user.get_admin_by_token(session.get('token'))
    user_info_0 , user_info_1 , user_info_2  = user_info
    resultado = controlador_participante.obtener_resultado_id(id)
    cant_max_progreso = controlador_agrupacion.obtener_cantidad_maxima_progreso() 
    return render_template(adminPage("ver_informacion.html") , resultado = resultado , user_info_1 = user_info_1 , user_info_2 = user_info_2 , cant_max_progreso = cant_max_progreso )



@app.route("/logout")
def logout():
    token = session.get('token')
    if token:
        session.pop('token', None)
        return redirect('/login')
    flash("Sesión vencida", "error")
    return redirect(url_for('login'))


@app.route("/error")
def error_page():
    message = request.args.get('message', 'Error desconocido')
    return render_template(generalPage("error_page.html"), message=message)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
