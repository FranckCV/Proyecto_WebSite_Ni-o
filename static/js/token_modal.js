// Abrir el modal
function openModal() {
    const modal = document.getElementById('tokenModal');
    modal.style.display = 'flex';
}

// Cerrar el modal
function closeModal() {
    const modal = document.getElementById('tokenModal');
    modal.style.display = 'none';
}

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
    const token = inputToken.value.trim();

    if (!token) {
        alert('Por favor, ingrese su token de administrador.');
        return;
    }

    try {
        const sessionToken = await getSessionData();

        if (sessionToken && sessionToken === token) {
            const response = await fetch('/activar_test', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            // Si el servidor redirige, manejamos la redirección
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
            closeModal();
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
    }
}
