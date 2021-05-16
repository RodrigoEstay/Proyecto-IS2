#include <iostream>
#include <cstdio>
#include <string>


#include "Asignatura.h"

using namespace std;

Asignatura::Asignatura(string name, int codigoAsignatura, vector<ResAp*> res){

	nombre = name;
	codigoAsignatura = codigoAsignatura;
	resultadosAprendizaje = res;
	
}
Asignatura::Asignatura(string name, int codigoAsignatura, ifstream &archivo){

	nombre = name;
	codigoAsignatura = codigoAsignatura;
	
	string nombreRA;
	while(getline(archivo,nombreRA)){
		resultadosAprendizaje.push_back(new ResAp(nombreRA));
	}
}

Asignatura::Asignatura(string name, int codigoAsignatura){

	nombre = name;
	codigoAsignatura = codigoAsignatura;
	
	int n;
	do{
		cout << "Ingrese cantidad de Resultados de Aprendizaje de la asignatura\n";
		cin >> n;

	}while(n<=0);
	string nombreRA;
	cin.ignore(); //se come el salto de linea
	for(int i=0;i<n;i++){
		cout << "Ingrese resultado de aprendizaje numero " << i+1 <<": ";
		getline(cin,nombreRA);
		resultadosAprendizaje.push_back(new ResAp(nombreRA));
	}
}

void Asignatura::mostrarResultadosAsociados(){

	cout << "Resultados de Aprendizaje asociados a " << nombre << ":\n\n";

	for(int i = 0; i < resultadosAprendizaje.size(); i++){

		cout << i+1 << ".-" << resultadosAprendizaje[i]->nombre << endl;
		
	}

	cout << "\n";

}