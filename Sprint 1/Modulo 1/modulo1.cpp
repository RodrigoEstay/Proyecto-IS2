#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <string>

#include "ResAp.h"
#include "Asignatura.h"

using namespace std;

vector<Asignatura*> asignaturas;
vector<ResAp*> resultados;

void mostrarAsignaturas(){

	cout << "Asignaturas:\n\n";

	for(int i = 0; i < asignaturas.size(); i++){

		Asignatura a = *asignaturas[i];

		cout << i+1 << ".-" << a.nombre << endl;

	}
	cout << "\n";

}

void mostrarResultados(){

	cout << "Resultados de Aprendizaje:\n\n";

	for(int i = 0; i < resultados.size(); i++){

		ResAp a = *resultados[i];

		cout << i+1 << ".- " << a.nombre << endl;

	}
	cout << "\n";

}

void nuevaAsignatura(){

	string nombre;
	int codigo;
	int r = -3;

	/*
	res es un vector que le paso a la Nueva Asignatura que contiene los
	Resultados de Aprendizaje asociados.
	*/
	vector<ResAp*> res;

	system("clear");
	cout << "Nueva Asignatura\n\n\nnombre: ";

	getline(cin >> ws, nombre);

	cout << "\ncodigo de Asignatura: ";

	cin >> codigo;

	cout << "\n";

	mostrarResultados();
	cout << "0 para terminar\n";
	cout << "\nResultados de aprendizaje asociados: ";


	//Seleccion de Resultados de Aprendizaje
	while(true){

		cin >> r;

		if(r > 0 && r <= resultados.size()){

			res.push_back(resultados[r-1]);

		}
		else if(r < 0 && r > resultados.size()){

			cout << "Porfavor ingresar un numero de Resultado de Aprendizaje valido\n";

		}else{

			break;

		}
	}

	Asignatura* asignaturaNueva = new Asignatura(nombre, codigo, res);

	asignaturas.push_back(asignaturaNueva);

	system("clear");

}

int main(){

	int opcion;


	//por ahora lo deje con Resultados de Aprendizaje #. No se si quieren usar archivos de texto.

	ResAp* r1 = new ResAp("Resultado_de_Aprendizaje_1");
	ResAp* r2 = new ResAp("Resultado_de_Aprendizaje_2");
	ResAp* r3 = new ResAp("Resultado_de_Aprendizaje_3");
	resultados.push_back(r1);
	resultados.push_back(r2);
	resultados.push_back(r3);

	system("clear");

	while(1){

		cout << "Ingresar una de las siguientes opciones:\n1: Nueva Asignatura\n2: Mostrar info. Asignatura\n0: Exit\n\nOpcion: ";

		cin >> opcion;

		if(opcion == 1){

			nuevaAsignatura();

		}else if(opcion == 2){

			system("clear");
			cout << "Porfavor seleccionar una Asignatura\n\n";
			mostrarAsignaturas();
			cin >> opcion;

			system("clear");
			asignaturas[opcion-1]->mostrarResultadosAsociados();

		}else if(opcion == 0){

			break;

		}

	}

	return 0;
}
