const menuButton = document.querySelector("#menu_button");
const aside = document.querySelector("aside.general_element");

if (menuButton && aside) {
    menuButton.addEventListener("click", () => {
        aside.classList.toggle("desplegar");
    });
}