#include <string>
#include <vector>
#include "Item.h"

Item::Item(int numEvaluacion, int numero, int puntajeMax){
	this->numero = numero;
	this->puntajeMax = puntajeMax;
	this->numEvaluacion = numEvaluacion;
	resultadosAsignados = std::vector<ResAp*>();

}

int Item::getNumero(){  

	return numero;
}
int Item::getPuntajeMax(){  
	return puntajeMax;
}
void Item::asignarResultadoAprendizaje(ResAp* resAp){  
	bool yaAsignado = false;
	for(int i=0;i<resultadosAsignados.size();i++){        //revisa si el resultado de aprendizaje ya existe en la lista
		if (resultadosAsignados[i]->nombre==resAp->nombre){
			yaAsignado = true;
			break;
		}
	}
	if(yaAsignado==false){
		resultadosAsignados.push_back(resAp);   //si no existe se asigna
	}
	
}
std::vector<ResAp*> Item::getResultadosAsignados(){ 
	return resultadosAsignados;
}
int Item::getEvaluacion(){  
	return numEvaluacion;
}