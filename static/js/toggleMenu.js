// Ajustarr el espaciado del menú desplegable basado en el tamaño del header
function adjustPadding() {
    const aside = document.querySelector('aside.general_element');
    const headerHeight = document.querySelector('header').offsetHeight;
    if (aside) {
        aside.style.paddingTop = `calc(15px + ${headerHeight}px)`;
    }
}

window.addEventListener("load", adjustPadding);
window.addEventListener("resize", adjustPadding);

// Funcionalidad del menú desplegable
const menuButton = document.querySelector("#menu_button");
const aside = document.querySelector("aside.general_element");

if (menuButton && aside) {
    menuButton.addEventListener("click", () => {
        aside.classList.toggle("desplegar"); // Añadir o quitar la clase para mostrar/ocultar
        adjustPadding();
    });
}


