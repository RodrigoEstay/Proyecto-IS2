var cantItem = 1
var cantidadRA = [0];
function agregarItem(){
	cantItem++;
	cantidadRA.push(0);
	document.getElementById("numItems").value = cantItem;
	var temp = document.getElementById("item");
  	
  	var e = document.createElement('div');
	e.innerHTML = temp.innerHTML;
	e.innerHTML = e.innerHTML.replace(/{NITEM}/g,cantItem);

    
	document.getElementById('lista-items').appendChild(e);
} 