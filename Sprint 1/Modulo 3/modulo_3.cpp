#include <iostream>
#include <string>
#include <stdlib.h>

#include "ResAp.h"
#include "Item.h"
#include "Evaluacion.h"
#include "Asignatura.h"



using namespace std;


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
	vector<ResAp*> resultados;
	vector<ResAp*> resultados2;
	ResAp* r1 = new ResAp("Resultado_de_Aprendizaje_1");
	ResAp* r2 = new ResAp("Resultado_de_Aprendizaje_2");
	ResAp* r3 = new ResAp("Resultado_de_Aprendizaje_3");
	ResAp* r4 = new ResAp("Resultado_de_Aprendizaje_4");
	ResAp* r5 = new ResAp("Resultado_de_Aprendizaje_5");
	resultados.push_back(r1);
	resultados.push_back(r2);
	resultados.push_back(r3);
	resultados2.push_back(r4);
	resultados2.push_back(r5);

	asignaturas.push_back(new Asignatura("IS2",503355,resultados));
	asignaturas.push_back(new Asignatura("IA",503356,resultados2));

	return asignaturas;	
}

void menu_asignar_RA(int indexEvaluacion, Evaluacion* eval, Asignatura* asignatura){  
/*menú donde se muestra la info de la evaluación, los items que tiene, los resultados de aprendizaje ya asignados a cada item,
y la lista de resultados correspondientes a la asignatura. Se ingresa un par de números correspondientes al item al que se quiere
asignar un resultado de aprendizaje, y el número del resultado de aprendizaje a asignar*/
	int numItem; 
	int numRA;
	vector<Item*> items = eval->get_items();
	vector<ResAp*> resultadosAsignatura = asignatura->resultadosAprendizaje;
	vector<ResAp*> resultadosAprendizaje;
	while(true){
		clear_screen();
		cout<<"Evaluacion "<<eval->get_num_evaluacion()<<endl;

		cout<<"Items: "<<endl;
		for(int i=0;i<items.size();i++){           //imprime lista de items y los resultados de aprendizaje asignados a cada uno
			cout<<i<<". Item "<<items[i]->getNumero()<<", Puntaje "<<items[i]->getPuntajeMax()<<endl;
			resultadosAprendizaje = items[i]->getResultadosAsignados();
			cout<<"   Resultados:"<<endl;
			for(int j=0;j<resultadosAprendizaje.size();j++){
				cout<<j+1<<". "<<resultadosAprendizaje[j]->nombre<<endl;
			}
		}


		cout<<"\n\n Resultados de aprendizaje de esta asignatura:"<<endl;      //imprime resultados de aprendizaje correspondientes a la asignatura de la evaluación
		asignatura->mostrarResultadosAsociados();


		cout<<"Ingresar numero de item y resultado de aprendizaje. 0 0 para salir:"<<endl; 
		//input: ingresar num de item y num de resultado de aprendizaje, si el input es válido se asocia el RA al item, sino se pide volver a ingresar input
		while(true){
			cin>>numItem>>numRA;
			if(numItem==0&&numRA==0){
				return;
			}
			if(numItem<0||numRA<1||numItem>items.size()||numRA>asignatura->resultadosAprendizaje.size()){
				cout<<"Ingresar valor valido"<<endl;
			} else{

				items[numItem]->asignarResultadoAprendizaje(asignatura->resultadosAprendizaje[numRA-1]);
				break;
			}
		}		
	}
}

void menu_elegir_eval(int indexAsignatura){
//menú que se abre una vez escogida una asignatura. Muestra lista de evaluaciones de la asignatura, permite elegir una evaluación o ingresar una nueva.
	int index = 0;
	
	while(true){
		clear_screen();
		cout<<"Asignatura: "<<placeholders[indexAsignatura]->nombre<<endl;
		vector<Evaluacion*> evals = placeholders[indexAsignatura]->mostrarEvaluaciones();
		cout<<"Escoger una opcion:"<<endl;
		for(int i=0;i<evals.size();i++){
			cout<<i+1<<". Evaluacion "<<evals[i]->get_num_evaluacion()<<endl;
		}

		cout<<"0. Crear nueva evaluacion\n100. Salir"<<endl;
		while(true){
			cin>>index;
			if(index<-1||(index>evals.size()+1&&index!=100)){
				cout<<"Por favor ingresar un valor valido"<<endl;
			} else{
				break;
			}
		}
		if(index==100){
			break;
		}else if (index==0){
			Evaluacion* eval = new Evaluacion(evals.size()+1);
			placeholders[indexAsignatura]->nuevaEvaluacion(eval);
		}
		else{
			menu_asignar_RA(index-1, evals[index-1],placeholders[indexAsignatura]);
		}
	}	
}


void menu_principal(){
//muestra lista de asignaturas para seleccionar una. Si el input es válido se procede al menú de elegir evaluación.
	cout<<"entrando a menu principal"<<endl;
	int index = 0;
	while(true){
		clear_screen();
		cout<<"Seleccionar una asignatura:"<<endl;
		for (int i=0; i<placeholders.size();i++){
			cout<<i+1<<" "<<placeholders[i]->nombre<<" "<<placeholders[i]->codigoAsignatura<<endl;
		}
		cout<<"0. Salir"<<endl;
		while(true){
			cin>>index;
			if(index<0||index>placeholders.size()+1){
				cout<<"Por favor ingresar un valor valido"<<endl;
			} else{
				break;
			}
		}
		if(index==0){
			break;
		}else{
			menu_elegir_eval(index-1);
		}
	}
}

int main(){
	
	clear_screen();
	placeholders =crear_placeholders();
	menu_principal();
	return 0;
}
