// Mostrar el modal
function openModal() {
    const modal = document.getElementById('tokenModal');
    modal.style.display = 'flex';
}

// Cerrar el modal
function closeModal() {
    const modal = document.getElementById('tokenModal');
    modal.style.display = 'none';
}

// Enviar el token
function sendToken() {
    const token = document.getElementById('adminToken').value;
    if (!token) {
        alert('Por favor, ingrese su token de administrador.');
        return;
    }
    // Aquí podrías enviar el token al servidor, si es necesario
    console.log('Token enviado:', token);
    cerrarModal();
}
