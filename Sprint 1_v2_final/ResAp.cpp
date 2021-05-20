#include <iostream>
#include <cstdio>
#include <string>


#include "ResAp.h"

using namespace std;

ResAp::ResAp(string name){
	
	nombre = name;

}

string ResAp::getNombre(){
	return nombre;
}