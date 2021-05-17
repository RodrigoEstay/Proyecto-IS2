#ifndef ITEM_H
#define ITEM_H

#include "ResAp.h"
#include <vector>

class Item{

private:
	int numero;
	int puntajeMax;
	int numEvaluacion;
	std::vector<ResAp*> resultadosAsignados;

public:
	Item(int numEvaluacion,int numero, int puntajeMax);
	int getNumero();                                       
	int getPuntajeMax();                                   //retorna puntaje max del item
	void asignarResultadoAprendizaje(ResAp* resAp);        //asignar un resultado de aprendizaje a este item
	std::vector<ResAp*> getResultadosAsignados();          //devuelve lista de todos los resultados asignados a este item
	int getEvaluacion();                                   //retorna el número identificador de la evaluación a la que pertenece este item
};

#endif