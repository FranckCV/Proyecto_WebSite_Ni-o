document.querySelectorAll('.toggle-password').forEach(button => {
  button.addEventListener('click', () => {
    const input = document.querySelector(button.getAttribute('data-target'));
    const icon = button.querySelector('i');
    if (input.type === 'password') {
      input.type = 'text';

    } else {
      input.type = 'password';

    }
  });
});

document.getElementById('newPassword').addEventListener('input', validatePasswords);
document.getElementById('confirmPassword').addEventListener('input', validatePasswords);

function validatePasswords() {
  const newPassword = document.getElementById('newPassword').value;
  const confirmPassword = document.getElementById('confirmPassword').value;
  const errorMessage = document.getElementById('errorMessage');
  const newPasswordInput = document.getElementById('newPassword');
  const confirmPasswordInput = document.getElementById('confirmPassword');

  if (newPassword !== confirmPassword) {
    errorMessage.style.display = 'block';  // Muestra el mensaje de error
    newPasswordInput.classList.add('error');  // Aplica clase de error al input de nueva contraseña
    confirmPasswordInput.classList.add('error');  // Aplica clase de error al input de confirmación
    newPasswordInput.classList.remove('valid');  // Elimina clase de validación si las contraseñas no coinciden
    confirmPasswordInput.classList.remove('valid');  // Elimina clase de validación si las contraseñas no coinciden
  } else {
    errorMessage.style.display = 'none';  // Oculta el mensaje de error
    newPasswordInput.classList.add('valid');  // Aplica clase de validación al input de nueva contraseña
    confirmPasswordInput.classList.add('valid');  // Aplica clase de validación al input de confirmación
    newPasswordInput.classList.remove('error');  // Elimina clase de error si las contraseñas coinciden
    confirmPasswordInput.classList.remove('error');  // Elimina clase de error si las contraseñas coinciden
  }
}
