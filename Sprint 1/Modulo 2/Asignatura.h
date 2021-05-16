#ifndef ASIGNATURA_H
#define ASIGNATURA_H

#include <string>
#include <vector>
#include <fstream>
#include "ResAp.h"

using namespace std;
	
class ResAp;

class Asignatura{

	public:
		string nombre;
		int codigoAsignatura;
		vector<ResAp*> resultadosAprendizaje;
		
	
	public:
		Asignatura(string nombre, int codigoAsignatura, vector<ResAp*> resultadosAprendizaje);
		Asignatura(string nombre, int codigoAsignatura, ifstream &archivo);
		Asignatura(string nombre, int codigoAsignatura);
		void mostrarResultadosAsociados();
	
};

#endif