from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response,  redirect, url_for
import controladores.controlador_agrupacion as controlador_agrupacion
import controladores.controlador_participante as controlador_participante
import controladores.controlador_seleccion  as controlador_seleccion
import controladores.controlador_estado_test  as controlador_estado_test
import hashlib
import base64
import clases.encriptar_cookie as encriptacion
import jwt
from flask_socketio import SocketIO, emit, send
import random
from datetime import datetime, date
from clases.User import User
from clases.auth import token_required
import controladores.controlador_user as controlador_user

app = Flask(__name__, template_folder='templates')
app.secret_key = 'security_key'
socketio = SocketIO(app)

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


def check_back_option(template,tipo):
    if tipo=="general":
        response = make_response(render_template(generalPage(f"{template}")))
    elif tipo == "admin":
        response = make_response(render_template(adminPage(f"{template}")))  
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


# def index():
#     participante_id = request.cookies.get('id_participante_cookie')
#     if participante_id:
#         id_grupo = controlador_seleccion.obtener_ultima_seleccion(participante_id)
#         verificado = controlador_seleccion.verificar_cantidad_seleccionada(participante_id,id_grupo)
#         if id_grupo==28 and verificado:
#             response = make_response(render_template(generalPage("index.html")))
#             response.delete_cookie("id_participante_cookie")
#             return response
#         elif id_grupo is not None:
#             return redirect(url_for('pregunta', id_grupo=id_grupo)) 
#         else:
#             return redirect(url_for('pregunta', id_grupo=1))

#     else:   
#         return render_template(generalPage("index.html"))


@app.route("/login")
def login():
    redirection = check_token(funcion='dashboard')
    if redirection: return redirection
    response = check_back_option("login.html","admin")
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

# @app.route("/")
# def main():
#     estado = controlador_estado_test.obtener_estado_test()
#     if estado:
#         return redirect(url_for('sign_up'))
#     return redirect(url_for('espera_dos'))

@app.route("/")
def sign_up():
    estado = controlador_estado_test.obtener_estado_test()
    if not estado:
        return redirect(url_for('espera_dos'))

    participante_cookie = request.cookies.get('id_participante_cookie')
    if participante_cookie:
        id_grupo = controlador_seleccion.obtener_ultima_seleccion(participante_cookie)

        verificado = controlador_seleccion.verificar_cantidad_seleccionada(participante_cookie, id_grupo)
        
        if id_grupo == 28 and verificado:
            response = make_response(render_template(generalPage("sign_up.html")))
            response.delete_cookie("id_participante_cookie")
            return response
        elif id_grupo is not None:
            return redirect(url_for('pregunta', id_grupo=id_grupo))
        else:
            return redirect(url_for('pregunta', id_grupo=1))

    response = check_back_option("sign_up.html", "general")
    return response
    # participante_cookie = request.cookies.get('id_participante_cookie')
    
    # if participante_cookie:
    #     id_grupo = controlador_seleccion.obtener_ultima_seleccion(participante_cookie)
    #     verificado = controlador_seleccion.verificar_cantidad_seleccionada(participante_cookie,id_grupo)
    #     if id_grupo==28 and verificado:
    #         response = make_response(render_template(generalPage("sign_up.html")))
    #         response.delete_cookie("id_participante_cookie")
    #         return response
    #     elif id_grupo is not None:
    #         return redirect(url_for('pregunta', id_grupo=id_grupo)) 
    #     else:
    #         return redirect(url_for('pregunta', id_grupo=1))

    # response = check_back_option("sign_up.html","general")
    # return response

@app.route("/eliminar_cookies_despues_de_resultado")
def eliminar_cookies_despues_de_resultado():
    respuesta = redirect(url_for('sign_up'))
    
    respuesta.delete_cookie('id_participante_cookie')
    respuesta.delete_cookie('id_grupo_cookie')
    
    return respuesta


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
        return redirect(url_for('error_page', message='No se pudo guardar el participante. Por favor, intente nuevamente.', redirigir = False))
    
    hash_id = encriptacion.generar_hash(id_participante)
    cookie_valor = f"{id_participante}:{hash_id}"
    
    id_grupo_inicial = 1
    respuesta = redirect(url_for('pregunta', id_grupo=id_grupo_inicial))
    respuesta.set_cookie('id_participante_cookie', cookie_valor)
    return respuesta


@app.route("/pregunta=<int:id_grupo>")
def pregunta(id_grupo):
    participante_id = request.cookies.get('id_participante_cookie')
    desordenar = session.get('desordenar', False)

    if not participante_id:
        return redirect("/sign_up")

    ultima_seleccion = controlador_seleccion.obtener_ultima_seleccion(participante_id)
    cantidad_seleccionada = controlador_seleccion.contar_selecciones_por_participante(participante_id)

    if ultima_seleccion is None:
        id_grupo = 1  
    elif id_grupo > ultima_seleccion and ultima_seleccion <28:
        id_grupo = ultima_seleccion+1



    if request.path != f"/pregunta={id_grupo}":
        return redirect(url_for("pregunta", id_grupo=id_grupo))


    cualidades_desordenadas = session.get(f"cualidades_desordenadas_{id_grupo}")
    if not cualidades_desordenadas:
        cualidades = list(controlador_agrupacion.obtener_cualidades(id_grupo))
        if desordenar:
            random.shuffle(cualidades)
        cualidades_desordenadas = cualidades
        session[f"cualidades_desordenadas_{id_grupo}"] = cualidades_desordenadas
    ##############################################################################
    
    return render_template(
        "pregunta.html",
        cualidades=cualidades_desordenadas,
        id_grupo=id_grupo,
        verificado=controlador_seleccion.verificar_cantidad_seleccionada(participante_id, id_grupo),
        seleccion_positiva=controlador_seleccion.obtener_id_cualidad_positiva_seleccionada(participante_id, id_grupo),
        seleccion_negativa=controlador_seleccion.obtener_id_cualidad_negativa_seleccionada(participante_id, id_grupo),
    )


@app.route("/seleccionar_positivo", methods=["POST"])
def seleccionar_positivo():
    participante_id = request.cookies.get('id_participante_cookie')
    id_grupo = request.form["grupo"]
    cualidad_id = request.form["positive"]
    estado = True
    mensaje = controlador_seleccion.insertar_seleccion_positiva(participante_id, id_grupo, cualidad_id, estado)
    print(mensaje)
    return redirect(url_for('pregunta',id_grupo=id_grupo))

@app.route("/seleccionar_negativo", methods=["POST"])
def seleccionar_negativo():
    participante_id = request.cookies.get('id_participante_cookie')
    id_grupo = request.form["grupo"]
    cualidad_id = request.form["negative"]
    estado = False
    mensaje = controlador_seleccion.insertar_seleccion_negativa(participante_id, id_grupo, cualidad_id, estado)
    print(mensaje)
    return redirect(url_for('pregunta',id_grupo=id_grupo))


@app.route("/siguiente_pregunta", methods=["POST"])
def siguiente_pregunta():
    id_grupo_actual = int(request.form["grupo"])
    id_grupo = id_grupo_actual + 1
    respuesta = make_response(redirect(url_for("pregunta", id_grupo=id_grupo)))
    session['desordenar'] = 'true' 
    return respuesta

# @app.route("/pregunta_anterior", methods=["POST"])
# def pregunta_anterior():
#     id_grupo_actual = int(request.form["grupo"])
#     id_grupo = id_grupo_actual - 1
#     respuesta = make_response(redirect(url_for("pregunta", id_grupo=id_grupo)))
#     session['desordenar'] = 'true'  
#     return respuesta

###############################################################################################################


@app.route("/resultado")
def resultado():
    participante_cookie = request.cookies.get('id_participante_cookie')
    id_grupo = controlador_seleccion.obtener_ultima_seleccion(participante_cookie)
    if not participante_cookie:
        return redirect(url_for('sign_up'))

    try:
        participante_id, hash_recibido = participante_cookie.split(":")
    except ValueError:
        message = "Error: La cookie está mal formada."
        return render_template(generalPage("error_page.html"), message=message, redirigir = False), 400

    if not encriptacion.verificar_hash(participante_id, hash_recibido):
        message = "Error: La cookie no es válida."
        return render_template(generalPage("error_page.html"), message=message, redirigir = False), 400

    try:
        participante_id = int(participante_id)
    except ValueError:
        message = "Error: El ID del participante en la cookie no es válido."
        return render_template(generalPage("error_page.html"), message=message, redirigir = False), 400

    cantidad_selecciones = controlador_seleccion.contar_selecciones_por_participante(participante_id)
    if cantidad_selecciones != 56:
        if id_grupo is None:
            return redirect(url_for('pregunta', id_grupo=1))
        elif id_grupo:
            return redirect(url_for('pregunta', id_grupo=int(id_grupo)))
        else:
            return redirect(url_for('error_page', message='No se pudo determinar el grupo para redirigir', redirigir = False))
    

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
    # response = check_back_option("dashboard_reporte.html")
    response = check_back_option("dashboard_reporte.html","admin")
    cant_max_progreso = controlador_agrupacion.obtener_cantidad_maxima_progreso() 
    resultados = controlador_participante.obtener_resultados()
    token = session.get('token')
    user_info = controlador_user.get_admin_by_token(token)

    user_info_0 , user_info_1 , user_info_2  = user_info

    response.set_data(render_template(adminPage("dashboard_reporte.html"), resultados = resultados , cant_max_progreso = cant_max_progreso , user_info_1 = user_info_1 , user_info_2 = user_info_2, token=token))
    return response


@app.route("/activar_test")
@token_required
def activarTest():
    response = dict()
    try:
        controlador_estado_test.modificar_estado_test(True)
        response['status'] = 1
    except:
        response['status'] = -1
    return jsonify(response)

@app.route("/desactivar_test")
@token_required
def desactivarTest():
    response = dict()
    try:
        controlador_estado_test.modificar_estado_test(False)
        response['status'] = 1
    except:
        response['status'] = -1
    return jsonify(response)

@app.route('/api/get_session')
def get_session():
    send = dict()
    send["token"] = session.get('token')
    return jsonify(send)

@app.route("/buscarResultado")
@token_required
def buscarResultado():
    response = check_back_option("dashboard_reporte.html","admin")
    nombreBusqueda = request.args.get("buscarElemento")
    user_info = controlador_user.get_admin_by_token(session.get('token'))
    user_info_0 , user_info_1 , user_info_2  = user_info
    resultados = controlador_participante.buscar_resultado_nombre(nombreBusqueda)
    cant_max_progreso = controlador_agrupacion.obtener_cantidad_maxima_progreso() 
    response.set_data(render_template(adminPage("dashboard_reporte.html") , resultados = resultados , nombreBusqueda = nombreBusqueda , cant_max_progreso = cant_max_progreso , user_info_1 = user_info_1 , user_info_2 = user_info_2))
    return response


@app.route("/eliminar_cliente", methods=["POST"])
@token_required
def eliminar_info_participante():
    par_id = request.form["par_id"]
    controlador_seleccion.eliminar_seleccion_idpar(par_id)
    controlador_participante.eliminar_participante_id(par_id)
    return redirect("/dashboard")



@app.route("/ver_informacion=<int:id>")
@token_required
def ver_informacion(id):
    response = check_back_option("dashboard_reporte.html","admin")
    user_info = controlador_user.get_admin_by_token(session.get('token'))
    user_info_0 , user_info_1 , user_info_2  = user_info
    resultado = controlador_participante.obtener_resultado_id(id)
    cant_max_progreso = controlador_agrupacion.obtener_cantidad_maxima_progreso() 
    response.set_data(render_template(adminPage("ver_informacion.html") , resultado = resultado , user_info_1 = user_info_1 , user_info_2 = user_info_2 , cant_max_progreso = cant_max_progreso ))
    return response

@socketio.on('connect')
@token_required
def handle_connect():
    print('Cliente conectado')


@socketio.on('disconnect')
@token_required
def handle_disconnect():
    print('Cliente desconectado')

@app.route

@socketio.on('get_valores_participante')
@token_required
def handle_get_valores_participante(id):
    valores = controlador_participante.obtener_valores_id(id)
    emit("update_valores_participante",  {"valores": valores} , broadcast=True) 


@socketio.on('get_valores')
@token_required
def handle_get_valores():
    resultados = controlador_participante.obtener_valores()
    emit("update_valores",  {"resultados": resultados} , broadcast=True) 




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
    return render_template(generalPage("error_page.html"), message=message , redirigir=True)


@app.route("/espera")
def espera_dos():
    return render_template(generalPage("espera.html"))










@app.route("/temas")
@token_required
def temas():
    # response = check_back_option("dashboard_reporte.html")
    response = check_back_option("dashboard_reporte.html","admin")
    user_info = controlador_user.get_admin_by_token(session.get('token'))
    user_info_0 , user_info_1 , user_info_2  = user_info
    response.set_data(render_template(adminPage("temas.html"), user_info_1 = user_info_1 , user_info_2 = user_info_2))
    return response

@app.route("/colores")
def colores():
    return render_template(generalPage("colores.html"))

CSS_FILE_PATH = 'static/css/common_styles/colores.css'

@app.route('/load-css', methods=['GET'])
def load_css():
    try:
        with open(CSS_FILE_PATH, 'r') as css_file:
            css_content = css_file.read()
        return css_content, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save-css', methods=['POST'])
def save_css():
    try:
        data = request.json
        css_content = data.get('css')

        with open(CSS_FILE_PATH, 'w') as css_file:
            css_file.write(css_content)

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/save-colors', methods=['POST'])
def save_colors():
    try:
        colors = request.json
        css_content = ":root {\n"

        # Generar las variables CSS a partir de los datos recibidos
        for var, value in colors.items():
            css_content += f"    --{var}: {value};\n"

        css_content += "}"

        # Guardar el archivo
        with open(CSS_FILE_PATH, 'w') as css_file:
            css_file.write(css_content)

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8000, debug=True)
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
