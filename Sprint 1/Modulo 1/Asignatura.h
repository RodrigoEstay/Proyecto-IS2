#ifndef ASIGNATURA_H
#define ASIGNATURA_H

#include <string>
#include <vector>
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
		void mostrarResultadosAsociados();
	
};

#endif