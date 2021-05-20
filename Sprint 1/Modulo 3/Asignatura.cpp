#include <iostream>
#include <cstdio>
#include <string>


#include "Asignatura.h"

using namespace std;

Asignatura::Asignatura(string name, int codigoAsignatura, vector<ResAp*> res){

	nombre = name;
	this->codigoAsignatura = codigoAsignatura;
	resultadosAprendizaje = res;
	evaluaciones = vector<Evaluacion*>();
	
}

void Asignatura::mostrarResultadosAsociados(){

	cout << "Resultados de Aprendizaje asociados a " << nombre << ":\n\n";

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