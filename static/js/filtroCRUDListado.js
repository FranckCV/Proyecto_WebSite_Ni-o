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

function aplicarFiltros() {
  const dateInicioInput = document.getElementById('dateInicio');
  const hourInicioInput = document.getElementById('hourInicio');
  const dateFinalInput = document.getElementById('dateFinal');
  const hourFinalInput = document.getElementById('hourFinal');
  const estadoSelect = document.getElementById('estadoSelect');
  const rows = document.querySelectorAll('#productTableBody tr');

  const dateInicio = dateInicioInput?.value ? new Date(dateInicioInput.value + "T" + (hourInicioInput.value || "00:00")) : null;
  const dateFinal = dateFinalInput?.value ? new Date(dateFinalInput.value + "T" + (hourFinalInput.value || "23:59")) : null;
  const estadoSeleccionado = estadoSelect?.value || null;

  rows.forEach(row => {
    const fechaDiv = row.querySelector('[data-fecha]');
    const horaDiv = row.querySelector('[data-hora]');
    const fechaRow = fechaDiv ? new Date(fechaDiv.getAttribute('data-fecha') + "T" + (horaDiv ? horaDiv.getAttribute('data-hora') : "00:00")) : null;
    const estadoRow = fechaDiv ? fechaDiv.getAttribute('data-estado') : null;

    const cumpleFechaInicio = !dateInicio || (fechaRow && fechaRow >= dateInicio);
    const cumpleFechaFinal = !dateFinal || (fechaRow && fechaRow <= dateFinal);
    const cumpleEstado = !estadoSeleccionado || estadoSeleccionado === '0' || estadoSeleccionado === estadoRow;

    if (cumpleFechaInicio && cumpleFechaFinal && cumpleEstado) {
      row.style.display = ''; // Mostrar la fila
    } else {
      row.style.display = 'none'; // Ocultar la fila
    }
  });

  cantResultadosFilas();
}

function limpiarFiltros() {
  document.getElementById('dateInicio').value = '';
  document.getElementById('hourInicio').value = '';
  document.getElementById('dateFinal').value = '';
  document.getElementById('hourFinal').value = '';
  document.getElementById('estadoSelect').value = '0';
  aplicarFiltros(); // Reaplicar los filtros para mostrar todas las filas
}

// Eventos para los filtros
document.getElementById('dateInicio')?.addEventListener('input', aplicarFiltros);
document.getElementById('hourInicio')?.addEventListener('input', aplicarFiltros);
document.getElementById('dateFinal')?.addEventListener('input', aplicarFiltros);
document.getElementById('hourFinal')?.addEventListener('input', aplicarFiltros);
document.getElementById('estadoSelect')?.addEventListener('change', aplicarFiltros);

// Evento para el botón de limpiar filtros
document.getElementById('clearFilters')?.addEventListener('click', limpiarFiltros);

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
  aplicarFiltros();
  cantResultadosFilas();
});


// function cantResultadosFilas() {
//   const tableRows = document.querySelectorAll('#productTableBody tr');
//   const numResult = document.getElementById('num_resultados');
//   const numDispResult = document.getElementById('num_disp_si');
//   const numNoDispResult = document.getElementById('num_disp_no');

//   if (tableRows && numResult) {
//     const visibleRows = Array.from(tableRows).filter(row => {
//       return window.getComputedStyle(row).display !== 'none';
//     });
//     numResult.innerHTML = `${visibleRows.length}`;
//     const dispRows = visibleRows.filter(row => row.classList.contains('fila_disp_si'));
//     numDispResult.innerHTML = `${dispRows.length}`;

//     const dispNoRows = visibleRows.filter(row => row.classList.contains('fila_disp_no'));
//     numNoDispResult.innerHTML = `${dispNoRows.length}`;
//   }
// }

// function aplicarFiltros() {
//   const dateInicioInput = document.getElementById('dateInicio');
//   const dateFinalInput = document.getElementById('dateFinal');
//   const estadoSelect = document.getElementById('estadoSelect');
//   const rows = document.querySelectorAll('#productTableBody tr');

//   const dateInicio = dateInicioInput?.value ? new Date(dateInicioInput.value) : null;
//   const dateFinal = dateFinalInput?.value ? new Date(dateFinalInput.value) : null;
//   const estadoSeleccionado = estadoSelect?.value || null;

//   rows.forEach(row => {
//     const fechaDiv = row.querySelector('[data-fecha]');
//     const fechaRow = fechaDiv ? new Date(fechaDiv.getAttribute('data-fecha')) : null;
//     const estadoRow = fechaDiv ? fechaDiv.getAttribute('data-estado') : null;

//     const cumpleFechaInicio = !dateInicio || (fechaRow && fechaRow >= dateInicio);
//     const cumpleFechaFinal = !dateFinal || (fechaRow && fechaRow <= dateFinal);
//     const cumpleEstado = !estadoSeleccionado || estadoSeleccionado === '0' || estadoSeleccionado === estadoRow;

//     if (cumpleFechaInicio && cumpleFechaFinal && cumpleEstado) {
//       row.style.display = ''; // Mostrar la fila
//     } else {
//       row.style.display = 'none'; // Ocultar la fila
//     }
//   });

//   cantResultadosFilas();
// }

// // Eventos para los filtros de fechas y select
// document.getElementById('dateInicio')?.addEventListener('input', aplicarFiltros);
// document.getElementById('dateFinal')?.addEventListener('input', aplicarFiltros);
// document.getElementById('estadoSelect')?.addEventListener('change', aplicarFiltros);

// // Inicialización
// document.addEventListener('DOMContentLoaded', () => {
//   aplicarFiltros();
//   cantResultadosFilas();
// });


document.querySelectorAll('#productTableBody tr').forEach(fila => {
  fila.addEventListener('change',()=> {
    cantResultadosFilas();
  });
});
