import controladores.controlador_participante as controlador_participante
import controladores.controlador_seleccion  as controlador_seleccion

def eliminacionProgramada():
    participantes_id =controlador_participante.obtenerParticipantes()
    
    for participante in participantes_id:
        participante_id = participante[0]
        
        cantidad = controlador_seleccion.contar_selecciones_por_participante(participante_id)
        
        if cantidad < 56:
            controlador_seleccion.eliminar_seleccion_idpar(participante_id)
        
        controlador_participante.eliminar_participante_id(participante_id)