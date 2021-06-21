#include <iostream>
#include "Evaluacion.h"
#include <vector>
#include <set>
using namespace std;

Evaluacion::Evaluacion(int nevaluacion){
	num_evaluacion = nevaluacion;

	cout << "Ingrese la cantidad de items de la evaluacion: ";
	int cantidad;
	cin >> cantidad;
	while(cantidad<=0){
		cout << "Por favor ingrese un valor positivo: ";
		cin >> cantidad;
	}
	puntos = 0;
	for(int i=0;i<cantidad;i++){
		int pje;
		cout << "Ingrese el puntaje maximo del item "<< i+1 <<": ";
		cin >> pje;
		while(pje<=0){
			cout << "Por favor ingrese un valor positivo: ";
			cin >> pje;
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