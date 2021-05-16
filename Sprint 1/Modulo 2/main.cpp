#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <fstream>
#include "ResAp.h"
#include "Asignatura.h"
#include "Evaluacion.h"
using namespace std;

vector<Asignatura*> asignaturas;
vector<ResAp*> resultados;
vector<Evaluacion*> evaluaciones;
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

	cout << "Seleccione metodo para ingresar los resultados de aprendizaje:\n1:Desde texto\n2:Desde consola\n[1/2]: ";
	int forma;
	cin >> forma;
	while(forma <1 || forma > 2){
		cout << "Favor ingrese un metodo valido [1/2]: ";
	}
	Asignatura* asignaturaNueva;
	if(forma == 1){		//Metodo con txt
		string nombreArchivo;
		cout << "Ingrese nombre del archivo con los Resultados de Aprendizaje: ";
		cin >> nombreArchivo;
		ifstream archivo(nombreArchivo);
		if(archivo.is_open()){
			asignaturaNueva = new Asignatura(nombre,codigo,archivo);
		}
		else{
			cout << "Error al abrir el archivo\n";
			return;
		}
		archivo.close();
	}
	else{				//Metodo desde consola
		asignaturaNueva = new Asignatura(nombre,codigo);
	}
	asignaturas.push_back(asignaturaNueva);

	system("clear");

}

void nuevaEvaluacion(int opcion){
	//HACER ALGO CON ASIGNATURA SEMESTRE. DE MOMENTO SOLO GUARDA LA EVALUACION EN UN VECTOR
	cout << "Ingrese numero de la evaluacion :"; //Se podria automatizar segun las evaluaciones en AsignaturaSemestre
	int num_evaluacion;
	cin >> num_evaluacion;
	while(num_evaluacion <= 0){
		cout << "Por favor ingrese un valor positivo: ";
		cin >> num_evaluacion;
	}
	evaluaciones.push_back(new Evaluacion(num_evaluacion));
}

int main(){

	int opcion;


	//por ahora lo deje con Resultados de Aprendizaje #. No se si quieren usar archivos de texto.

	/*
	ResAp* r1 = new ResAp("Resultado_de_Aprendizaje_1");
	ResAp* r2 = new ResAp("Resultado_de_Aprendizaje_2");
	ResAp* r3 = new ResAp("Resultado_de_Aprendizaje_3");
	resultados.push_back(r1);
	resultados.push_back(r2);
	resultados.push_back(r3);
	*/
	system("clear");
	bool salir = false;
	while(!salir){

		cout << "Ingresar una de las siguientes opciones:\n1: Nueva Asignatura\n2: Mostrar info. Asignatura\n3: Agregar Evaluacion a Asignatura\n0: Exit\n\nOpcion: ";

		cin >> opcion;
		switch(opcion){
			case 1:
				nuevaAsignatura();
				break;
			case 2:
				system("clear");
				cout << "Porfavor seleccionar una Asignatura\n\n";
				mostrarAsignaturas();
				cin >> opcion;

				system("clear");
				asignaturas[opcion-1]->mostrarResultadosAsociados();
				break;
			case 3:
				system("clear");
				cout << "Porfavor seleccionar una Asignatura\n\n";
				mostrarAsignaturas();
				cin >> opcion;
				nuevaEvaluacion(opcion);
				/*
					TODO: FALTA HACER ALGO CON AsignaturaSemestre
				*/
				system("clear");
				break;
			case 0:
				salir = true;
				break;

		}
		

	}

	return 0;
}
