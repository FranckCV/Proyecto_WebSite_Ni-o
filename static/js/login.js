const usernameEt = document.querySelector('#username');
const passwordEt = document.querySelector('#password');
const formEt = document.querySelector('.login_form');
const btnStart = document.querySelector('#btnEmpezar');

// Función para validar campos vacíos
const isEmpty = (stringValidar) => stringValidar === '';

// Función para el mostrado de mensajes y manejo de colores
const showMessage = (input, message, type) => {
    const par = input.parentElement;
    const mensajeEt = par.querySelector('small');
    if (type === 'error') {
        par.classList.remove('success');
        par.classList.add('error');
        mensajeEt.textContent = message;
    } else if (type === 'success') {
        par.classList.remove('error');
        par.classList.add('success');
        mensajeEt.textContent = '';
    }
};


const checkUsuario = () => {
    let isValid = false;
    const usuario = usernameEt.value.trim();
    if (isEmpty(usuario)) {
        showMessage(usernameEt, 'No puede dejar este campo vacío', 'error');
    } else {
        showMessage(usernameEt, '', 'success');
        isValid = true;
    }
    return isValid;
};

const checkPassword = () => {
    let isValid = false;
    const pass = passwordEt.value.trim();
    if (isEmpty(pass)) {
        showMessage(passwordEt, 'La contraseña no puede estar vacía', 'error');
    } else if (pass.length < 6) {
        showMessage(passwordEt, 'La contraseña debe tener al menos 6 caracteres', 'error');
    } else {
        showMessage(passwordEt, '', 'success');
        isValid = true;
    }
    return isValid;
};

const debounce = (fn, delay = 3000) => {
    let timeoutId;
    return (...args) => {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(() => {
            fn.apply(null, args);
        }, delay);
    };
};

// Escuchar eventos en tiempo real para validar inputs
formEt.addEventListener(
    'input',
    debounce((e) => {
        switch (e.target.id) {
            case 'username':
                checkUsuario();
                break;
            case 'password':
                checkPassword();
                break;
        }
    })
);


btnStart.addEventListener('click', (event) => {
    event.preventDefault();
    const userValid = checkUsuario();
    const passValid = checkPassword();
    if (userValid && passValid) {
        formEt.submit();
    } else {
        
    }
});
