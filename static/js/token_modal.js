// Función para alternar el estado del Test
function toggleTest() {
    var switchElement = document.getElementById("switch");

    // Si el switch está activado, activar el test
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
}

// Función para cerrar el modal
function closeModal() {
    const modal = document.getElementById('tokenModal');
    modal.style.display = 'none';
    
    const switchElement = document.getElementById("switch");
    switchElement.checked = false;  // Desmarca el switch si se cierra el modal
}

// Función para obtener el token de sesión del servidor
const socketMessage = io();

async function getSessionData() {
    const url = '/api/get_session';

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const sessionData = await response.json();
        return sessionData.token;  // Devuelve el token que el servidor tiene almacenado

    } catch (error) {
        console.error('Error fetching session data:', error);
        return null;
    }
}


// Activar Test: Llama a la ruta /activar_test
async function sendToken() {
    const inputToken = document.getElementById('adminToken');
    let token = inputToken.value.trim();

    if (!token) {
        alert('Por favor, ingrese su token de administrador.');
        return;
    }

    // Detecta y elimina el prefijo `b'` y el sufijo `'` si están presentes
    if (token.startsWith("b'") && token.endsWith("'")) {
        token = token.slice(2, -1);
    }

    try {
        const sessionToken = await getSessionData();
        console.log("Token ingresado:", token);
        console.log("Token de sesión:", sessionToken);

        // Comparar los tokens como strings
        if (sessionToken && sessionToken === token) {
            const response = await fetch('/activar_test', {
                method: 'GET',
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

            inputToken.value = "";
            closeModal();  // Cierra el modal una vez activado el test
        } else {
            alert('Token no válido o no encontrado');
        }

    } catch (error) {
        console.error('Error checking session or sending token:', error);
        alert('Error al verificar el token. Intenta nuevamente.');
    }
}


// Desactivar Test: Llama a la ruta /desactivar_test
async function disableTest() {
    const switchElement = document.getElementById('switch');
    
    try {
        const sessionToken = await getSessionData(); // Obtén el token del servidor

        if (sessionToken) {
            console.log('Token is valid. Proceed with the operation.');
            
            // Llama a la ruta de desactivar test
            const response = await fetch('/desactivar_test', {
                method: 'GET', // Usa POST o el método que tu ruta requiera
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${sessionToken}` // Se pasa el token de administrador en la cabecera
                }
            });

            const data = await response.json();
            if (data.status === 1) {
                alert('Test desactivado');
            } else {
                alert('Error al desactivar el test');
            }
        } else {
            alert('Token no válido o no encontrado');
        }
    } catch (error) {
        console.error('Error checking session or disabling token:', error);
        alert('Error al verificar el token. Intenta nuevamente.');

        // Si ocurre un error, no desmarcar el switch
        // Esto evita que el switch se quede en OFF por un error
        switchElement.checked = true;  // Mantiene el switch activado
    }
}

// Función para verificar el estado del test y ajustar el switch al cargar la página
window.addEventListener('DOMContentLoaded', function() {
    const estadoTest = document.getElementById('estado_test').getAttribute('data-estado');
    const switchElement = document.getElementById('switch');
    
    console.log("Estado del test: ", estadoTest);  // Verifica el valor
    if (estadoTest === 'True') {
        switchElement.checked = true;  // Si está ON, marca el switch
    } else {
        switchElement.checked = false;  // Si está OFF, desmarca el switch
    }
});
