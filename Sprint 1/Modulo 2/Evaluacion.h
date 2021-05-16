#ifndef EVALUACION_H
#define EVALUACION_H

#include <vector>
#include "Items.h"
#include "ResAp.h"
class Evaluacion{
private:
	int num_evaluacion;
	int puntos;
	vector<Items*> items;
public:
	Evaluacion(int nevaluacion);
	vector<Items*> get_items();
	void mostrar_RA_asociados();
	vector<ResAp*> get_RA();
	int get_puntos();
	int get_num_evaluacion();
};

#endif