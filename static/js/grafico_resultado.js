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
    data.addColumn('number', 'Puntaje');
    data.addRows([
        ['Tierra', -10],
        ['Fuego', 20],
        ['Agua', 30],
        ['Aire', -25]
    ]);

    const config = {
        width: 600,
        height: 400,
        colors: ['#C51D34', '#FF4500', '#1E90FF', '#A9A9A9'],
        legend: { position: 'none' }
    };

    const chart = new google.visualization.ColumnChart(div);
    chart.draw(data, config);
}

google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(renderizar);
