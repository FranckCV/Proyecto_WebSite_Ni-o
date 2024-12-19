// document.addEventListener('DOMContentLoaded', () => {
//     const rutasPermitidas = [
//         '/seleccionar_positivo',
//         '/seleccionar_negativo',
//         '/siguiente_pregunta',
//         '/pregunta_anterior'
//     ];

//     // Función para validar si la ruta actual está permitida
//     function validarRuta() {
//         const rutaActual = window.location.pathname; // Obtiene la ruta actual
//         if (!rutasPermitidas.includes(rutaActual)) {
//             alert('No tienes permiso para acceder a esta ruta.'); // Mostrar alerta
//             window.location.href = rutasPermitidas[0]; // Redirigir a la primera ruta permitida
//         }
//     }

//     // Validar al cargar la página
//     validarRuta();

//     // Detectar cambios en el historial (navegar hacia adelante o hacia atrás)
//     window.addEventListener('popstate', validarRuta);

//     // Opcional: Interceptar enlaces y prevenir el acceso a rutas no permitidas
//     document.querySelectorAll('a').forEach(link => {
//         link.addEventListener('click', (event) => {
//             const href = link.getAttribute('href');
//             if (!rutasPermitidas.includes(href)) {
//                 event.preventDefault();
//                 alert('No tienes permiso para acceder a esta ruta.');
//             }
//         });
//     });
// });



// document.addEventListener('DOMContentLoaded', () => {
//     history.pushState(null, null, window.location.href);

//     window.addEventListener('popstate', (event) => {
//         history.pushState(null, null, window.location.href);
//         alert("La navegación hacia atrás está deshabilitada en esta página.");
//     });
// });

// window.addEventListener("beforeunload", (event) => {
//     event.preventDefault();
//     event.returnValue = ""; 
// });

// document.addEventListener("keydown", (event) => {
//     if (
//         event.key === "Backspace" || 
//         (event.altKey && event.key === "ArrowLeft") || 
//         (event.altKey && event.key === "ArrowRight") 
//     ) {
//         event.preventDefault();
//         alert("La navegación hacia atrás está deshabilitada.");
//     }
// });




document.addEventListener('DOMContentLoaded', () => {
    // Agregar un estado falso al historial para controlar la navegación
    history.pushState(null, '', location.href);

    // Escuchar el evento `popstate` (se activa al navegar hacia atrás o adelante)
    window.addEventListener('popstate', (event) => {
        alert("La navegación hacia atrás o adelante está bloqueada."); // Mostrar alerta
        history.pushState(null, '', location.href); // Reinsertar el estado falso
    });

    // Opcional: Bloquear teclas de retroceso (backspace) y flechas de navegación
    document.addEventListener('keydown', (event) => {
        if (event.key === 'ArrowLeft' || event.key === 'ArrowRight' || event.key === 'Backspace') {
            alert("La navegación con flechas o retroceso está bloqueada.");
            event.preventDefault(); // Evitar el comportamiento predeterminado
        }
    });
});