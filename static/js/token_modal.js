// Función reutilizable para manejar la obtención del token de sesión
async function fetchSessionToken() {
    const url = '/api/get_session';
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
        const sessionData = await response.json();
        return sessionData.token;
    } catch (error) {
        console.error('Error al obtener el token de sesión:', error);
        return null;
    }
}

// Función para alternar el estado del Test
function toggleTest() {
    const switchElement = document.getElementById("switch");
    if (switchElement.checked) {
        console.log("Test activado");
        openModal(); // Abre el modal para ingresar el token
    } else {
        console.log("Test desactivado");
        disableTest(); // Llama a la función para desactivar el test
    }
}

// Función para abrir el modal
function openModal() {
    const modal = document.getElementById('tokenModal');
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
}

// Función para cerrar el modal
function closeModal() {
    const modal = document.getElementById('tokenModal');
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
    const switchElement = document.getElementById("switch");
    switchElement.checked = false; // Desmarca el switch si se cierra el modal
}

// Función para activar el Test
async function sendToken() {
    const inputToken = document.getElementById('adminToken');
    let token = inputToken.value.trim();

    if (!token) {
        alert('Por favor, ingrese su token de administrador.');
        return;
    }

    if (token.startsWith("b'") && token.endsWith("'")) {
        token = token.slice(2, -1);
    }

    try {
        const sessionToken = await fetchSessionToken();
        if (sessionToken && sessionToken === token) {
            const response = await fetch('/activar_test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.redirected) {
                window.location.href = response.url;
                return;
            }

            const data = await response.json();
            if (data.status === 1) {
                alert('Test activado');
            } else {
                alert('Error al activar el test');
            }

            inputToken.value = '';
            closeModal();
        } else {
            alert('Token no válido o no encontrado');
        }
    } catch (error) {
        console.error('Error al activar el test:', error);
        alert('Error al verificar el token. Intenta nuevamente.');
    }
}

// Función para desactivar el Test
async function disableTest() {
    try {
        const sessionToken = await fetchSessionToken();
        console.log("Token:", sessionToken);  // Verificar el valor del token

        if (sessionToken) {
            console.log("Entró al if");

            // Asegúrate de que el token está en el encabezado Authorization
            const response = await fetch('/desactivar_test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${sessionToken}`  // Asegúrate de que el token esté bien formado
                }
            });

            const data = await response.json();
            console.log("Se envió: ", data);
            if (data.status === 1) {
                alert('Test desactivado');
            } else {
                alert('Error al desactivar el test');
            }
        } else {
            alert('Token no válido o no encontrado');
        }
    } catch (error) {
        console.error('Error al desactivar el test:', error);
        alert('Error al verificar el token. Intenta nuevamente.');
        document.getElementById('switch').checked = true; // Mantiene el switch activado
    }
}



// Verifica el estado inicial al cargar la página
window.addEventListener('DOMContentLoaded', () => {
    const estadoTest = document.getElementById('estado_test').getAttribute('data-estado');
    console.log("El estado test es: ",estadoTest)
    const switchElement = document.getElementById('switch');
    if (estadoTest === 'True') {
        switchElement.checked = true;
    } else if (estadoTest === 'False') {
        switchElement.checked = false;
    } else {
        console.warn("Estado desconocido para el test:", estadoTest);
    }
});
