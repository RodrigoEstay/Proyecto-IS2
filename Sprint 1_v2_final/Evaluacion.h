#ifndef EVALUACION_H
#define EVALUACION_H

#include <vector>

#include "ResAp.h"
#include "Item.h"

class Evaluacion{

private:
	int num_evaluacion;
	int puntos;
	vector<Item*> items;

public:
	Evaluacion(int nevaluacion);
	vector<Item*> get_items();
	void mostrar_RA_asociados();
	vector<ResAp*> get_RA();
	int get_puntos();
	int get_num_evaluacion();
	void registrarPuntaje();
	void mostrarInformacion();
};

#endif