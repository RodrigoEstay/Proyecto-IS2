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

void Asignatura::mostrarResultadosAsociados(){

	cout << "Resultados de Aprendizaje asociados a " << nombre << ":\n\n";

	for(int i = 0; i < resultadosAprendizaje.size(); i++){

		cout << i+1 << ".-" << resultadosAprendizaje[i]->nombre << endl;

	}

	cout << "\n";

}