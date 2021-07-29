google.load("visualization", "1", {packages: ["corechart",'table']});

function drawChart(chartType, containerID, dataArray, options) {
    var data = google.visualization.arrayToDataTable(dataArray,false);
    data.addColumn({type:'string',role:'style'});
    data.setCell(0,2,'color: #092C48');
    data.setCell(1,2,'color: #4682B4');
    data.setCell(2,2,'color: #ADD8E6');
    var containerDiv = document.getElementById(containerID);
    var chart = false;

    if (chartType.toUpperCase() == 'BARCHART') {
        chart = new google.visualization.BarChart(containerDiv);
    }
    else if (chartType.toUpperCase() == 'COLUMNCHART') {
        chart = new google.visualization.ColumnChart(containerDiv);
    }
    else if (chartType.toUpperCase() == 'PIECHART') {
        chart = new google.visualization.PieChart(containerDiv);
    }
    else if (chartType.toUpperCase() == 'TABLECHART')
    {
        chart = new google.visualization.Table(containerDiv);
    }

    if (chart == false) {
        return false;
    }

    chart.draw(data, options);
}