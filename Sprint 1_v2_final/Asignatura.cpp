#include <iostream>
#include <cstdio>
#include <string>
#include <fstream>


#include "Asignatura.h"

using namespace std;

Asignatura::Asignatura(string name, int codigoAsignatura, vector<ResAp*> res){

	nombre = name;
	this->codigoAsignatura = codigoAsignatura;
	resultadosAprendizaje = res;
	evaluaciones = vector<Evaluacion*>();
	
}

Asignatura::Asignatura(string name, int codigoAsignatura, ifstream &archivo){

	nombre = name;
	this->codigoAsignatura = codigoAsignatura;
	
	string nombreRA;
	while(getline(archivo,nombreRA,'\r')){
		if(nombreRA.size()<3) continue;
		if(nombreRA[0] == '\n'){
			nombreRA.erase(0,1);
		}
		resultadosAprendizaje.push_back(new ResAp(nombreRA));
	}
}

Asignatura::Asignatura(string name, int codigoAsignatura){

	nombre = name;
	this->codigoAsignatura = codigoAsignatura;
	
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
	string mensaje = "Resultados de Aprendizaje asociados a "+ nombre;
	//cout << mensaje << nombre << " :" << endl;
	cout << mensaje <<endl << endl;
	for(int i = 0; i < resultadosAprendizaje.size(); i++){

		cout << i+1 << ".-" << resultadosAprendizaje[i]->nombre << endl;

	}

	cout << "\n";

}
void Asignatura::nuevaEvaluacion(Evaluacion* eval){
	evaluaciones.push_back(eval);
}
vector<Evaluacion*> Asignatura::mostrarEvaluaciones(){
	return evaluaciones;
}

Evaluacion* Asignatura::accederEvaluacion(int indice){
	return evaluaciones[indice];
}

int Asignatura::cantidadEval(){
	return evaluaciones.size();
}