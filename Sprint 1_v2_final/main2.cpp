#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <fstream>
#include <unordered_map>
#include <filesystem>
#include "ResAp.h"
#include "Asignatura.h"
#include "Evaluacion.h"
#include "Item.h"

using namespace std;

vector<Asignatura*> asignaturas;
vector<ResAp*> resultados;
unordered_map<int,vector<Evaluacion*> > evaluaciones;
vector<Asignatura*> placeholders;

void clear_screen(){   
//ejecuta "cls" si el OS es windows, "clear" si no lo es (por portabilidad)

	#ifdef _WIN32
		system("cls");
	#else
		system("clear");
	#endif
}

vector<Asignatura*> crear_placeholders(){      
//crea instancias de asignaturas que tienen resultados de aprendizaje ya asignados, para pruebas
	vector<Asignatura*> asignaturas;
	for (auto& dirEntry: filesystem::recursive_directory_iterator("ramos")) {
	    if (!dirEntry.is_regular_file()) {
	        continue;
	    }

	    ifstream arch(dirEntry.path());
	    if(arch.is_open()){
	    	
	    	vector<ResAp*> resultados;
	    	string nombre;
	    	int codigo;
	    	getline(arch,nombre,'\r');
	    	arch >> codigo;
	    	asignaturas.push_back(new Asignatura(nombre,codigo,arch));
	    }
	}

	return asignaturas;	
}

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

void infoAsignaturas(){
	mostrarAsignaturas();
	cout << "Seleccione una asignatura:  ";
	int op;
	cin >> op;
	while(op <= 0 || op > asignaturas.size()){
		cout << "Por favor ingrese un número válido: " << endl;
		cin >> op;
	}
	cout << "\n\n";
	clear_screen();
	asignaturas[op-1]->mostrarResultadosAsociados();
	vector<Evaluacion*> evals = asignaturas[op-1]->mostrarEvaluaciones();
	for(int i=0;i<evals.size();i++){
		cout << "Evaluacion "<< evals[i]->get_num_evaluacion() << endl;
		evals[i]->mostrarInformacion();
	}

}

void asignar_RA(int indexEvaluacion, int indexAsignatura){  
/*menú donde se muestra la info de la evaluación, los items que tiene, los resultados de aprendizaje ya asignados a cada item,
y la lista de resultados correspondientes a la asignatura. Se ingresa un par de números correspondientes al item al que se quiere
asignar un resultado de aprendizaje, y el número del resultado de aprendizaje a asignar*/
	int numItem; 
	int numRA;
	int codeA = asignaturas[indexAsignatura]->codigoAsignatura;
	vector<Item*> items = asignaturas[indexAsignatura]->accederEvaluacion(indexEvaluacion)->get_items();
	vector<ResAp*> resultadosAsignatura = asignaturas[indexAsignatura]->resultadosAprendizaje;
	vector<ResAp*> resultadosAprendizaje;
	while(true){
		clear_screen();
		cout<<"Evaluacion "<<asignaturas[indexAsignatura]->accederEvaluacion(indexEvaluacion)->get_num_evaluacion()<<"\n\n";

		cout<<"Items: \n";
		for(int i=0 ; i<items.size() ; i++){           //imprime lista de items y los resultados de aprendizaje asignados a cada uno
			cout<<"\n" << i+1<<". Item "<<items[i]->getNumero()<<", Puntaje "<<items[i]->getPuntajeMax()<<endl;
			resultadosAprendizaje = items[i]->getResultadosAsignados();
			cout<<"    Resultados:"<<endl;
			for(int j=0 ; j<resultadosAprendizaje.size() ; j++){
				cout<<"     " << j+1 <<". "<<resultadosAprendizaje[j]->nombre<<"\n";
			}
		}
		cout << endl;

		asignaturas[indexAsignatura]->mostrarResultadosAsociados();


		cout<<"Ingresar numero de item y resultado de aprendizaje. 0 0 para salir:"<<endl; 
		//input: ingresar num de item y num de resultado de aprendizaje, si el input es válido se asocia el RA al item, sino se pide volver a ingresar input
		while(true){
			cin >> numItem >> numRA;
			if(numItem==0&&numRA==0){
				return;
			}
			if(numItem<0||numRA<1||numItem>items.size()||numRA>asignaturas[indexAsignatura]->resultadosAprendizaje.size()){
				cout<<"Ingresar valor valido"<<endl;
			} else{

				items[numItem-1]->asignarResultadoAprendizaje(asignaturas[indexAsignatura]->resultadosAprendizaje[numRA-1]);
				break;
			}
		}		
	}
}


void crearNuevaEvaluacion(int opcion){
	if(opcion > asignaturas.size()){
		cout << "Valor invalido.\n\n";
		return;
	}

	int code = asignaturas[opcion - 1]->codigoAsignatura;

	

	int num_ev = asignaturas[opcion-1]->cantidadEval()+1;

	cout << ". " << asignaturas[opcion-1]->nombre << " .\n\n";
	cout << "Ingrese número de Items para la Evaluación " << num_ev << ":  ";
	asignaturas[opcion-1]->nuevaEvaluacion(new Evaluacion(num_ev));
	asignar_RA(num_ev-1, opcion-1);
}

void registrarPuntajes(int opcionAsignatura){
	int code = asignaturas[opcionAsignatura - 1]->codigoAsignatura;

	if(asignaturas[opcionAsignatura-1]->cantidadEval()==0){
		cout << "La asignatura " << asignaturas[opcionAsignatura-1]->nombre <<" no tiene evaluaciones.\n\n";
		return;
	}

	cout << "Por favor seleccione una Evaluación: \n\n";

	for(int i=0 ; i<asignaturas[opcionAsignatura-1]->cantidadEval(); i++){
		cout << i+1 << ".- Evaluación " << asignaturas[opcionAsignatura-1]->accederEvaluacion(i)->get_num_evaluacion() << endl;
	}
	cout << endl;
	int opcion;
	cin >> opcion;
	
	while(opcion <= 0 || opcion >asignaturas[opcionAsignatura-1]->cantidadEval()){
		cout << "Por favor ingrese un valor válido: ";
		cin >> opcion;
	}
	
	vector<Item*> it = asignaturas[opcionAsignatura-1]->accederEvaluacion(opcion-1)->get_items();

	for(int i=0 ; i<it.size() ; i++){
		cout << "Ingrese puntaje para Item " << it[i]->getNumero() << ":    (Máximo " << it[i]->getPuntajeMax() << " puntos)" << endl;
		int puntaje;
		cin >> puntaje;
		while(puntaje > it[i]->getPuntajeMax() || puntaje <= 0){
			cout << "Por favor ingrese un valor válido: ";
			cin >> puntaje;
		}
		it[i]->asignarPuntaje(puntaje);
	}

	cout << "\n\nPuntaje asignado a la Evaluación " << opcion << "\n\n";
	for(int i=0 ; i<it.size() ; i++){
		cout << "Item " << it[i]->getNumero() << ": " <<  it[i]->getPuntajeObtenido() << "/" << it[i]->getPuntajeMax() << endl;
	}
	cout << "\n\n";

}

// -----------------------------------------------------------------


//------------------------------------------------------------------




int main(){

	int opcion;

	clear_screen();
	bool salir = false;
	asignaturas = crear_placeholders();
	while(!salir){
		cout << "______________________________________________________________" << endl;
		cout << "\n\n    .:: MENU PRINCIPAL ::. \n\n\n";

		cout << "Ingresar una de las siguientes opciones:\n\n1: Mostrar info. Asignatura\n2: Agregar Evaluacion a Asignatura\n3: Registrar Puntaje \n\n0: Exit\n\nOpcion: ";

		cin >> opcion;
		cout << "______________________________________________________________" << endl;

		
		switch(opcion){
			
			case 1:
				cout << "\n\n";
				infoAsignaturas();
				break;
			case 2:
				clear_screen();
				cout << "Porfavor seleccionar una Asignatura\n\n";
				mostrarAsignaturas();
				if(!(cin >> opcion)){
					cout << "Valor invalido.\n\n";
					cin.clear();
					cin.ignore(100, '\n');
					break;
				}
				crearNuevaEvaluacion(opcion);
				
				break;
			case 3:
				clear_screen();
				cout << "Por favor seleccionar una Asignatura\n\n";
				mostrarAsignaturas();
				cin >> opcion;
				while(opcion <= 0 || opcion > asignaturas.size()){
					cout << "Por favor ingrese un número válido: " << endl;
					cin >> opcion;
				}
				registrarPuntajes(opcion);
				break;

			case 0:
				salir = true;
				break;

			default:
				cin >> opcion;
				break;	
		}
		

	}

	return 0;
}
