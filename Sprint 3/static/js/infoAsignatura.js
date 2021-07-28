google.load("visualization", "1", {packages: ["corechart",'table']});

function drawChart(chartType, containerID, dataArray, options) {
    var data = google.visualization.arrayToDataTable(dataArray,false);
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

function setModal(pos){

	var modal = document.getElementById("myModal-".concat(pos));

	// Get the button that opens the modal
	var btn = document.getElementById("alumno-".concat(pos));

	// Get the <span> element that closes the modal
	var span = document.getElementById("close-".concat(pos));

	// When the user clicks on the button, open the modal
	btn.onclick = function() {
	  modal.style.display = "block";
	}

	// When the user clicks on <span> (x), close the modal
	span.onclick = function() {
	  modal.style.display = "none";
	}

	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
	  if (event.target == modal) {
	    modal.style.display = "none";
	  }
	}


}

