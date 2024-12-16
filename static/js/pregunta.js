function verTexto(button) {
    var div = button.closest('.magnify'); 
    var text = div.querySelector('.text'); 

    if (text.style.display === 'none') {
      text.style.display = 'block';
    } else {
      text.style.display = 'none';
    }
  }

  function disminuirProgress() {
    var progressBar = document.getElementById('progressBar');
    var progressText = document.getElementById('progressText');
    
    if (progressBar.value > progressBar.min) {  
        progressBar.value -= 1;
        progressText.textContent = `${progressBar.value} / 28`;  
    }
}

function incrementProgress() {
    var progressBar = document.getElementById('progressBar');
    var progressText = document.getElementById('progressText');
    
    if (progressBar.value < progressBar.max) { 
        progressBar.value += 1;
        progressText.textContent = `${progressBar.value} / 28`; 
    }
}

