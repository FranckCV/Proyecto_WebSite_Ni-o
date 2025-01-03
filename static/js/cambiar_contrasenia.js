document.addEventListener('DOMContentLoaded', function () {
  // Obtener el modal de Bootstrap
  const statusModalElement = document.getElementById('statusModal');
  const statusModal = new bootstrap.Modal(statusModalElement);

  // Función para mostrar/ocultar contraseña
  document.querySelectorAll('.toggle-password').forEach(button => {
    button.addEventListener('click', () => {
      const input = document.querySelector(button.getAttribute('data-target'));
      const icon = button.querySelector('i');
      if (input.type === 'password') {
        input.type = 'text';
        icon.textContent = '🙈'; // Cambiar ícono al mostrar la contraseña
      } else {
        input.type = 'password';
        icon.textContent = '👁️'; // Cambiar ícono al ocultar la contraseña
      }
    });
  });

  // Funciones de validación específicas
  const isRequired = (value) => value.trim() !== '';
  const isPasswordValid = (password) => password.length >= 6;

  // Mostrar mensajes de error o éxito
  const showPasswordError = (input, message) => {
    const inputGroup = input.parentElement;
    inputGroup.classList.remove('success');
    inputGroup.classList.add('error');
  
    const error = inputGroup.querySelector('small');
    if (error) {
      error.textContent = message;
      error.style.display = 'block';
    }
  
    // Agregar la clase para ajustar la posición del botón
    inputGroup.classList.add('error-visible');
  };
  
  const showPasswordSuccess = (input) => {
    const inputGroup = input.parentElement;
    inputGroup.classList.remove('error');
    inputGroup.classList.add('success');
  
    const error = inputGroup.querySelector('small');
    if (error) {
      error.textContent = '';
      error.style.display = 'none';
    }
  
    // Eliminar la clase para ajustar la posición del botón
    inputGroup.classList.remove('error-visible');
  };
  

  const checkCurrentPassword = () => {
    let valid = false;
    const currentPassword = currentPasswordEl.value.trim();
    if (!isRequired(currentPassword)) {
      showPasswordError(currentPasswordEl, 'El campo Contraseña actual no puede estar vacío.');
    } else {
      showPasswordSuccess(currentPasswordEl);
      valid = true;
    }
    return valid;
  };

  const checkNewPassword = () => {
    let valid = false;
    const newPassword = newPasswordEl.value.trim();
    const currentPassword = currentPasswordEl.value.trim();

    if (!isRequired(newPassword)) {
      showPasswordError(newPasswordEl, 'El campo Nueva contraseña no puede estar vacío.');
    } else if (!isPasswordValid(newPassword)) {
      showPasswordError(newPasswordEl, 'La nueva contraseña debe tener al menos 6 caracteres.');
    } else if (newPassword === currentPassword) {
      showPasswordError(newPasswordEl, 'La nueva contraseña debe ser distinta.');
    } else {
      showPasswordSuccess(newPasswordEl);
      valid = true;
    }
    return valid;
  };

  const checkConfirmPassword = () => {
    let valid = false;
    const confirmPassword = confirmPasswordEl.value.trim();
    const newPassword = newPasswordEl.value.trim();

    if (!isRequired(confirmPassword)) {
      showPasswordError(confirmPasswordEl, 'El campo Confirmar contraseña no puede estar vacío.');
    } else if (confirmPassword !== newPassword) {
      showPasswordError(confirmPasswordEl, 'Las contraseñas no coinciden.');
    } else {
      showPasswordSuccess(confirmPasswordEl);
      valid = true;
    }
    return valid;
  };

  // Selección de elementos del formulario
  const currentPasswordEl = document.querySelector('#currentPassword');
  const newPasswordEl = document.querySelector('#newPassword');
  const confirmPasswordEl = document.querySelector('#confirmPassword');
  const passwordForm = document.querySelector('#passwordForm');

  // Función para forzar la validación de campos vacíos al cargar
  const validateEmptyFields = () => {
    if (!isRequired(currentPasswordEl.value)) {
      showPasswordError(currentPasswordEl, 'El campo Contraseña actual no puede estar vacío.');
    }
    if (!isRequired(newPasswordEl.value)) {
      showPasswordError(newPasswordEl, 'El campo Nueva contraseña no puede estar vacío.');
    }
    if (!isRequired(confirmPasswordEl.value)) {
      showPasswordError(confirmPasswordEl, 'El campo Confirmar contraseña no puede estar vacío.');
    }
  };

  // Validación de todos los campos
  const validateForm = () => {
    const isCurrentPasswordValid = checkCurrentPassword();
    const isNewPasswordValid = checkNewPassword();
    const isConfirmPasswordValid = checkConfirmPassword();

    return isCurrentPasswordValid && isNewPasswordValid && isConfirmPasswordValid;
  };

  // Función para validar los campos al cargar el formulario (autocompletados)
  const validateFieldsOnLoad = () => {
    validateEmptyFields(); // Validar campos vacíos
    checkCurrentPassword();
    checkNewPassword();
    checkConfirmPassword();
  };

  // Llamar a la validación al cargar el formulario (por si el navegador autocompleta)


  // Enviar el formulario solo si es válido
  passwordForm.addEventListener('submit', function (e) {
    e.preventDefault(); // Prevenir el envío del formulario si hay errores
    validateFieldsOnLoad();

    if (validateForm()) {
      // Si todo es válido, procesamos el envío con fetch
      const formData = new FormData(passwordForm);
      const data = Object.fromEntries(formData.entries());

      fetch('/change_password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      .then((response) => response.json())
      .then((data) => {
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
      .catch((error) => {
        console.error('Error:', error);
        modalMessage.textContent = 'Hubo un error al cambiar la contraseña.';
        statusModal.show();
      });
    } else {
      console.log("Formulario no válido, corregir errores.");
    }
  });

  // Validación en tiempo real (sin necesidad de hacer clic)
  passwordForm.addEventListener('input', function (e) {
    switch (e.target.id) {
      case 'currentPassword':
        checkCurrentPassword();
        break;
      case 'newPassword':
        checkNewPassword();
        break;
      case 'confirmPassword':
        checkConfirmPassword();
        break;
    }
  });
});
