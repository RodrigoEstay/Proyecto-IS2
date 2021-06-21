#ifndef ASIGNATURA_H
#define ASIGNATURA_H

#include <string>
#include <vector>
#include "ResAp.h"
#include "Evaluacion.h"

using namespace std;
	
class ResAp;

class Asignatura{

	public:
		string nombre;
		int codigoAsignatura;
		vector<ResAp*> resultadosAprendizaje;
		vector<Evaluacion*> evaluaciones;
	
	public:
		Asignatura(string nombre, int codigoAsignatura, vector<ResAp*> resultadosAprendizaje);
		void mostrarResultadosAsociados();
		void nuevaEvaluacion(Evaluacion* eval);
		vector<Evaluacion*> mostrarEvaluaciones();
	
};

#endif