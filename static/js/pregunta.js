function verTexto(button) {
    var div = button.closest('.magnify'); 
    var text = div.querySelector('.text'); 

    if (text.style.display === 'none') {
      text.style.display = 'block';
    } else {
      text.style.display = 'none';
    }
  }