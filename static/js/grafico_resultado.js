// const div = document.getElementById('google-chart');

// function renderizar(){
//     console.log(google);
//     const data = new google.visualization.DataTable();
//     data.addColumn('string', 'Elementos');
//     data.addColumn('number', 'Puntaje');
//     data.addRows([
//         ['Tierra', -10],
//         ['Fuego', 20],
//         ['Agua', 30],
//         ['Aire', -25]
//     ]);

//     const config = {
//         width: 1000,
//         height: 400
//     }
//     const chart = new google.visualization.BarChart(div);
//     chart.draw(data, config);
// }

// google.charts.load('current', {'packages':['corechart']});
// google.charts.setOnLoadCallback(renderizar);

const div = document.getElementById('google-chart');

function renderizar() {
    console.log(google);
    const data = new google.visualization.DataTable();
    data.addColumn('string', 'Elementos');
    data.addColumn('number', 'Tierra');
    data.addColumn('number', 'Fuego');
    data.addColumn('number', 'Agua');
    data.addColumn('number', 'Aire');
    data.addRows([
        ['Elementos', -10, null, null, null], // Solo Tierra tiene valor
        ['Elementos', null, 20, null, null], // Solo Fuego tiene valor
        ['Elementos', null, null, 30, null], // Solo Agua tiene valor
        ['Elementos', null, null, null, -25] // Solo Aire tiene valor
    ]);

    const config = {
        width: 600,
        height: 400,
        legend: { position: 'none' },
        colors: ['#C51D34', '#FF4500', '#1E90FF', '#A9A9A9'], // Colores específicos para cada barra
        bar: { groupWidth: '200%' }, // Aumenta el ancho relativo de las barras
        chartArea: { width: '100%' }, // Reduce el espacio alrededor de las barras
    };

    const chart = new google.visualization.ColumnChart(div);
    chart.draw(data, config);
}

google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(renderizar);
