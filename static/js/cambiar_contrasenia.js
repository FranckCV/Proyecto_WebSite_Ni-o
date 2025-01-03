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
  const currentPassword = document.getElementById('currentPassword').value;
  const newPassword = document.getElementById('newPassword').value;
  const confirmPassword = document.getElementById('confirmPassword').value;
  const errorMessage = document.getElementById('errorMessage');
  const newPasswordInput = document.getElementById('newPassword');
  const confirmPasswordInput = document.getElementById('confirmPassword');

  if (newPassword.length < 6 || confirmPassword.length < 6) {
    errorMessage.style.display = 'block';
    errorMessage.textContent = "La contraseña debe tener al menos 6 caracteres.";
    newPasswordInput.classList.add('error');
    confirmPasswordInput.classList.add('error');
    newPasswordInput.classList.remove('valid');
    confirmPasswordInput.classList.remove('valid');
  } else if (newPassword === "" || confirmPassword === "") {
    errorMessage.style.display = 'block';
    errorMessage.textContent = "Por favor, complete ambos campos de contraseña.";
    newPasswordInput.classList.add('error');
    confirmPasswordInput.classList.add('error');
    newPasswordInput.classList.remove('valid');
    confirmPasswordInput.classList.remove('valid');
  } else if (newPassword !== confirmPassword) {
    errorMessage.style.display = 'block';
    errorMessage.textContent = "Las contraseñas no coinciden.";
    newPasswordInput.classList.add('error');
    confirmPasswordInput.classList.add('error');
    newPasswordInput.classList.remove('valid');
    confirmPasswordInput.classList.remove('valid');
  } else if (newPassword === currentPassword) {
    errorMessage.style.display = 'block';
    errorMessage.textContent = "La nueva contraseña no puede ser igual a la actual.";
    newPasswordInput.classList.add('error');
    newPasswordInput.classList.remove('valid');
  } else {
    errorMessage.style.display = 'none';
    newPasswordInput.classList.add('valid');
    confirmPasswordInput.classList.add('valid');
    newPasswordInput.classList.remove('error');
    confirmPasswordInput.classList.remove('error');
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const passwordForm = document.getElementById('passwordForm');
  const modalMessage = document.getElementById('modalMessage');
  const statusModal = new bootstrap.Modal(document.getElementById('statusModal'));

  passwordForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(passwordForm);

    // Convertir FormData a objeto para enviar como JSON (opcional)
    const data = Object.fromEntries(formData.entries());

    fetch('/change_password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          modalMessage.textContent = data.message;
          statusModal.show();

          // Eliminar sesión y redirigir después de 2 segundos
          setTimeout(() => {
            fetch('/logout', { method: 'GET' }).then(() => {
              window.location.href = '/login';
            });
          }, 3000);
        } else {
          modalMessage.textContent = data.message;
          statusModal.show();
        }
      })
      .catch(error => {
        console.error('Error:', error);
        modalMessage.textContent = 'Hubo un error al cambiar la contraseña.';
        statusModal.show();
      });
  });
});
