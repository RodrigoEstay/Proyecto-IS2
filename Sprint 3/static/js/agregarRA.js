function agregarRA(nItem){
	cantidadRA[nItem-1]++;
	document.getElementById("numRA-".concat(nItem.toString())).value = cantidadRA[nItem-1];

	var temp = document.getElementById("RA");
  	
  	var e = document.createElement('div');
	e.innerHTML = temp.innerHTML;
	e.innerHTML = e.innerHTML.replace(/{NRES}/g,cantidadRA[nItem-1]).replace(/{NITEM}/g,nItem);

    
	document.getElementById('lista-RA-'.concat(nItem.toString())).appendChild(e);
} 