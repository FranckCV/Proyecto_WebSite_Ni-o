// Seleccionar elementos del formulario
const nombresEl = document.querySelector('#nombres');
const apellidosEl = document.querySelector('#apellidos');
const emailEl = document.querySelector('#email');
const fechaNacimientoEl = document.querySelector('#fecha_nacimiento');
const telefonoEl = document.querySelector('#telefono');
const form = document.querySelector('.sign_up_form');

// Funciones base
const isRequired = value => value === '' ? false : true;
const isEmailValid = (email) => {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
};
const isPhoneValid = (phone) => {
    const re = /^\d{9}$/; // Exactamente 9 dígitos
    return re.test(phone);
};
const isAdult = (birthDate) => {
    const today = new Date();
    const dob = new Date(birthDate);
    const age = today.getFullYear() - dob.getFullYear();
    const monthDifference = today.getMonth() - dob.getMonth();
    return age > 18 || (age === 18 && monthDifference >= 0 && today.getDate() >= dob.getDate());
};
const showError = (input, message) => {
    const formField = input.parentElement; // Ahora apunta al contenedor .input_group
    formField.classList.remove('success');
    formField.classList.add('error');

    // Seleccionar el <small> específico dentro del contenedor
    const error = formField.querySelector('small');
    error.textContent = message;
};

const showSuccess = (input) => {
    const formField = input.parentElement; // Ahora apunta al contenedor .input_group
    formField.classList.remove('error');
    formField.classList.add('success');

    // Asegurarse de que el mensaje se borre
    const error = formField.querySelector('small');
    error.textContent = '';
};


// Validaciones específicas
const checkNombres = () => {
    let valid = false;
    const nombres = nombresEl.value.trim();
    if (!isRequired(nombres)) {
        showError(nombresEl, 'El campo Nombres no puede estar vacío.');
    } else {
        showSuccess(nombresEl);
        valid = true;
    }
    return valid;
};

const checkApellidos = () => {
    let valid = false;
    const apellidos = apellidosEl.value.trim();
    if (!isRequired(apellidos)) {
        showError(apellidosEl, 'El campo Apellidos no puede estar vacío.');
    } else {
        showSuccess(apellidosEl);
        valid = true;
    }
    return valid;
};

const checkEmail = () => {
    let valid = false;
    const email = emailEl.value.trim();
    if (!isRequired(email)) {
        showError(emailEl, 'El campo Correo no puede estar vacío.');
    } else if (!isEmailValid(email)) {
        showError(emailEl, 'El formato del correo no es válido.');
    } else {
        showSuccess(emailEl);
        valid = true;
    }
    return valid;
};

const checkFechaNacimiento = () => {
    let valid = false;
    const fechaNacimiento = fechaNacimientoEl.value;
    if (!isRequired(fechaNacimiento)) {
        showError(fechaNacimientoEl, 'El campo Fecha de Nacimiento no puede estar vacío.');
    } else if (!isAdult(fechaNacimiento)) {
        showError(fechaNacimientoEl, 'Debes ser mayor de 18 años.');
    } else {
        showSuccess(fechaNacimientoEl);
        valid = true;
    }
    return valid;
};

const checkTelefono = () => {
    let valid = false;
    const telefono = telefonoEl.value.trim();
    if (!isRequired(telefono)) {
        showError(telefonoEl, 'El campo Teléfono no puede estar vacío.');
    } else if (!isPhoneValid(telefono)) {
        showError(telefonoEl, 'El Teléfono debe tener exactamente 9 dígitos.');
    } else {
        showSuccess(telefonoEl);
        valid = true;
    }
    return valid;
};

// Eventos
form.addEventListener('submit', function (e) {
    e.preventDefault();

    const isNombresValid = checkNombres();
    const isApellidosValid = checkApellidos();
    const isEmailValid = checkEmail();
    const isFechaNacimientoValid = checkFechaNacimiento();
    const isTelefonoValid = checkTelefono();

    const isFormValid = isNombresValid &&
        isApellidosValid &&
        isEmailValid &&
        isFechaNacimientoValid &&
        isTelefonoValid;

    if (isFormValid) {
        // Aquí puedes enviar el formulario al servidor
        form.submit();
    }
});

form.addEventListener('input', function (e) {
    switch (e.target.id) {
        case 'nombres':
            checkNombres();
            break;
        case 'apellidos':
            checkApellidos();
            break;
        case 'email':
            checkEmail();
            break;
        case 'fecha_nacimiento':
            checkFechaNacimiento();
            break;
        case 'telefono':
            checkTelefono();
            break;
    }
});
