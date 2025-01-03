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

  if (newPassword === "" || confirmPassword === "") {
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
  } else {
    errorMessage.style.display = 'none'; 
    newPasswordInput.classList.add('valid');
    confirmPasswordInput.classList.add('valid');
    newPasswordInput.classList.remove('error');
    confirmPasswordInput.classList.remove('error');
  }
}
