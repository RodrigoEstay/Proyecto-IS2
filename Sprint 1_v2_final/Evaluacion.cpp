#include <iostream>
#include "Evaluacion.h"
#include <vector>
#include <set>
#include "ResAp.h"
using namespace std;

Evaluacion::Evaluacion(int nevaluacion){
	num_evaluacion = nevaluacion;

	int cantidad;
	while(1){	
		if(cin >> cantidad && cantidad > 0){
			break;
		}
		else{
			cout << "Por favor ingrese un valor positivo: ";
			cin.clear();
			cin.ignore(100, '\n');
		}
	}
	puntos = 0;
	for(int i=0;i<cantidad;i++){
		int pje;
		cout << "Ingrese el puntaje maximo del item "<< i+1 <<": ";
		while(1){
			if(cin >> pje && pje > 0){
				break;
			}
			else{
				cout << "Por favor ingrese un valor positivo: ";
				cin.clear();
				cin.ignore(100, '\n');
			}
		}
		puntos+=pje;
		items.push_back(new Item(num_evaluacion,i+1,pje));
	}
}

vector<Item*> Evaluacion::get_items(){
	return items;
}

void Evaluacion::mostrar_RA_asociados(){
	vector<ResAp*> RA_asociados = get_RA();
	cout << "Los resultados asociados a esta evaluacion son:\n";
	for(int i=0;i<RA_asociados.size();i++){
		cout << i+1 << ".-" << RA_asociados[i]->nombre << endl;
	}
	cout << endl; 
}

vector<ResAp*> Evaluacion::get_RA(){
	set<ResAp*> cRA;			//conjunto para no repetir resultados de aprendizaje
	for(int i=0;i<items.size();i++){
		vector<ResAp*> RA_item = items[i]->getResultadosAsignados();
		for(int j=0;j<RA_item.size();j++){
			cRA.insert(RA_item[j]);
		}
	}
	vector<ResAp*> RA;
	for(auto ra : cRA){
		RA.push_back(ra);
	}
	
	return RA;
}

int Evaluacion::get_puntos(){
	return puntos;
}

int Evaluacion::get_num_evaluacion(){
	return num_evaluacion;
}

void Evaluacion::registrarPuntaje(){
	for(int i=0 ; i<items.size() ; i++){
		cout << "Ingrese un puntaje para el Item " << i << " 	__/" << items[i]->getPuntajeMax() << endl;
		int puntaje;
		while(1){	
			if(cin >> puntaje && puntaje <= items[i]->getPuntajeMax() && puntaje >= 0){
				break;
			}
			else{
				cout << "Por favor ingrese un valor valido: ";
				cin.clear();
				cin.ignore(100, '\n');
			}
		}
		items[i]->asignarPuntaje(puntaje);
	}

	for(int i=0 ; i<items.size() ; i++){
		cout << "Puntaje asignado: " << endl;
		cout << "Item " << i << ": " << items[i]->getPuntajeObtenido() << "/" << items[i]->getPuntajeMax();
	}


}

void Evaluacion::mostrarInformacion(){
	cout<<"Items: \n";
	for(int i=0 ; i<items.size() ; i++){           //imprime lista de items y los resultados de aprendizaje asignados a cada uno
		cout<<"\n" << i+1<<". Item "<<items[i]->getNumero()<<", Puntaje ["<<items[i]->getPuntajeObtenido()<<"/"<<items[i]->getPuntajeMax()<<"]"<<endl;
		vector<ResAp*> resultadosAprendizaje = items[i]->getResultadosAsignados();
		cout<<"    Resultados:"<<endl;
		for(int j=0 ; j<resultadosAprendizaje.size() ; j++){
			cout<<"     " << j+1 <<". "<<resultadosAprendizaje[j]->nombre<<"\n";
		}
	}
	cout << endl;
}