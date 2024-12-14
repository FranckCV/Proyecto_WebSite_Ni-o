function cantResultadosFilas() {
  const tableRows = document.querySelectorAll('#productTableBody tr');
  const numResult = document.getElementById('num_resultados');
  const numDispResult = document.getElementById('num_disp_si');
  const numNoDispResult = document.getElementById('num_disp_no');  

  if (tableRows && numResult) {
    const visibleRows = Array.from(tableRows).filter(row => {
      return window.getComputedStyle(row).display !== 'none';
    });
    numResult.innerHTML = `${visibleRows.length}`; 

    const dispRows = visibleRows.filter(row => row.classList.contains('fila_disp_si'));
    numDispResult.innerHTML = `${dispRows.length}`;

    const dispNoRows = visibleRows.filter(row => row.classList.contains('fila_disp_no'));
    numNoDispResult.innerHTML = `${dispNoRows.length}`;
  } 
}

cantResultadosFilas();

function filtroTableSelect(nombreSelect , atributo , valor) {
  document.getElementById(nombreSelect).addEventListener('change', function() {
    const elementSelect = this.value;
    const rows = document.querySelectorAll('#productTableBody tr');
  
    rows.forEach(row => {
      const itemDiv = row.querySelector('[data-'+atributo+']');
      const itemSelect = itemDiv ? itemDiv.getAttribute('data-'+atributo) : null;
  
      // Si el valor seleccionado es "0", mostrar todas las filas
      if (elementSelect === valor || itemSelect === elementSelect) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
    cantResultadosFilas();
  
  });
}


if (document.getElementById('categorySelect')) {
  document.getElementById('categorySelect').addEventListener('change', function() {
    const selectedCategory = this.value;
    const rows = document.querySelectorAll('#productTableBody tr');
  
    const options = document.querySelectorAll('#subcategorySelect option');
  
    options.forEach(option => {
      const optionCategory = option ? option.getAttribute('data-category') : null;
  
      if (selectedCategory === "0" || optionCategory === selectedCategory) {
        option.style.display = '';
      } else {
        option.style.display = 'none';
      }
    });
  
    rows.forEach(row => {
      const categoryDiv = row.querySelector('[data-category]');
      const productCategory = categoryDiv ? categoryDiv.getAttribute('data-category') : null;
  
      if (selectedCategory === "0" || productCategory === selectedCategory) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  
    cantResultadosFilas();
  
  });
  
}


if (document.getElementById('tiposImgNovedad')) {
  filtroTableSelect('tiposImgNovedad','tipo-img','0');
}

if (document.getElementById('subcategorySelect')) {
  filtroTableSelect('subcategorySelect','subcategory','0');
}

if (document.getElementById('subcategorySelect')) {
  filtroTableSelect('subcategorySelect','subcategory','0');
}

if (document.getElementById('brandSelect')) {
  filtroTableSelect('brandSelect','brand','0');
}


if (document.getElementById('tipoSelect')) {
  filtroTableSelect('tipoSelect','tipo','0');
}

if (document.getElementById('motivoSelect')) {
  filtroTableSelect('motivoSelect','motivo','0');
}

if (document.getElementById('estadoComSelect')) {
  filtroTableSelect('estadoComSelect','estado-comentario','-1');
}

if (document.getElementById('estadoPedidoSelect')) {
  filtroTableSelect('estadoPedidoSelect','estado-pedido','0');
}

if (document.getElementById('metodoPagoSelect')) {
  filtroTableSelect('metodoPagoSelect','metodo-pago','0');
}















// document.getElementById('subcategorySelect').addEventListener('change', function() {
//   const selectedCategory = this.value;
//   const rows = document.querySelectorAll('#productTableBody tr');

//   rows.forEach(row => {
//     const categoryDiv = row.querySelector('[data-subcategory]');
//     const productCategory = categoryDiv ? categoryDiv.getAttribute('data-subcategory') : null;

//     // Si el valor seleccionado es "0", mostrar todas las filas
//     if (selectedCategory === "0" || productCategory === selectedCategory) {
//       row.style.display = '';
//     } else {
//       row.style.display = 'none';
//     }
//   });

// cantResultadosFilas();

// });




// document.getElementById('brandSelect').addEventListener('change', function() {
//     const selectedBrand = this.value;
//     const rows = document.querySelectorAll('#productTableBody tr');

//     rows.forEach(row => {
//       const brandDiv = row.querySelector('[data-brand]');
//       const productBrand = brandDiv ? brandDiv.getAttribute('data-brand') : null;

//       // Si el valor seleccionado es "0", mostrar todas las filas
//       if (selectedBrand === "0" || productBrand === selectedBrand) {
//         row.style.display = '';
//       } else {
//         row.style.display = 'none';
//       }
//     });
//   cantResultadosFilas();

// });



// if (document.getElementById('tipoSelect')) {
//   document.getElementById('tipoSelect').addEventListener('change', function() {    
//     const selectedType = this.value;
//     const rows = document.querySelectorAll('#productTableBody tr');
  
//     rows.forEach(row => {
//       const typeDiv = row.querySelector('[data-tipo]');
//       const productType = typeDiv ? typeDiv.getAttribute('data-tipo') : null;
  
//       // Si el valor seleccionado es "0", mostrar todas las filas
//       if (selectedType === "0" || productType === selectedType) {
//         row.style.display = '';
//       } else {
//         row.style.display = 'none';
//       }
//     });
//     cantResultadosFilas();
  
//   });
// }