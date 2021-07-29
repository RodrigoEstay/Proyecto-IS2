import functools
import modulo8 as bd
from flask_login import current_user, login_required

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

#conn = bd.connect()
bp = Blueprint('evaluacion', __name__)

semester = 1
year = 2021

from main import con

@bp.route("/asignatura/<asignaturaID>/eval")
@login_required
def evaluation(asignaturaID):

	idProfesor = current_user.id
	asignaturasProfesor = bd.get_CodigosClasesImpartidas(con, idProfesor, semester, year)

	if asignaturaID in asignaturasProfesor:
		evaluaciones = bd.get_listaEvaluacionesAsignatura(con,asignaturaID,semester,year)
		asignaturas = {}
		asignaturas['name'] = bd.get_nombre_asignatura(con,asignaturaID)
		asignaturas['ID'] = asignaturaID

		return render_template('evaluacion/eval.html', evaluaciones=evaluaciones, asignatura=asignaturas)
	else:
		return redirect('/')


@bp.route("/asignatura/<asignaturaID>/eval/<int:evalID>/detalles")
@login_required
def detallesEval(asignaturaID, evalID):

	idProfesor = current_user.id
	asignaturasProfesor = bd.get_CodigosClasesImpartidas(con, idProfesor, semester, year)

	if asignaturaID in asignaturasProfesor:

		asignatura = {}
		asignatura["nombre"] = bd.get_nombre_asignatura(con,asignaturaID)
		asignatura["ID"] = asignaturaID

		evaluacion = {}
		evaluacion["index"] = request.args.get("evalIndex")
		evaluacion["ID"] = evalID

		items = bd.get_ItemsEvaluacion(con,evalID)
		items = sorted(items, key=lambda k:k["id_item"])

		RAItems = [bd.get_ResultadosItem(con, item["id_item"]) for item in items]
		temp = []
		for raitems in RAItems:
			for raitem in raitems:
				temp.append({'id_resultado':raitem["id_resultado"],'nombre':raitem["nombre"]})

		RAEval = list({v['id_resultado']:v for v in temp}.values())

		#RAEval = bd.get_ResultadosAsignatura(con, asignaturaID)
		comentario = None

		alumnos = bd.get_listaAlumnosAsignaturaSemestre(con, asignaturaID, semester, year)
		resultados = bd.get_resultadosEvaluacion(con,evalID)

		#agrego el campo de tiene o no tiene puntaje
		existe = False


		puntajemax = 0
		for item in items:
			puntajemax += item["puntaje_maximo"]
			

		for alumno in alumnos:

			contador = 1
			puntos = 0

			for item in items:

				existe = False
				for resultado in resultados:

					matricula = resultado.get('id_alumno', 'Noexiste')
					if(matricula == alumno["num_matricula"] and item["id_item"] == resultado["id_item"]):
						existe = True
						puntos += resultado["puntaje_obtenido"]

				if(existe):
					#tiene.append({"num_matricula":alumno["num_matricula"],"tiene":True})
					alumno[contador] = True
				else:
					#tiene.append({"num_matricula":alumno["num_matricula"],"tiene":False})
					alumno[contador] = False

				contador += 1

			if(existe):
				alumno["puntos"] = puntos
				alumno["puntajeMax"] = puntajemax

			else:
				alumno["puntos"] = "-"
				alumno["puntajeMax"] = puntajemax
				

		return render_template('evaluacion/detalles.html', asignatura=asignatura, evaluacion=evaluacion, items=items,RAItems=RAItems, RAEval=RAEval, alumnos=alumnos, resultados=resultados) 
	
	else:
		return redirect('/')


@bp.route("/asignatura/<asignaturaID>/eval/<int:evalID>/modificar", methods=['GET', 'POST'])
@login_required
def modificarEval(asignaturaID, evalID):

	pass 

@bp.route("/asignatura/<asignaturaID>/eval/<int:evalID>/<int:num_alumn>/addScore", methods=['GET', 'POST'])
@login_required
def addScore(asignaturaID, evalID, num_alumn):

	idProfesor = current_user.id
	asignaturasProfesor = bd.get_CodigosClasesImpartidas(con, idProfesor, semester, year)

	if asignaturaID in asignaturasProfesor:
		if request.method == "POST":

			puntajes = request.form.getlist("scores[]")
			matAlumno = request.form.get("alumno")
			itemsID = request.form.getlist("itemsID[]")

			for i in range(len(puntajes)):
				bd.ingresar_Puntaje(con, matAlumno, itemsID[i], puntajes[i])
			num_alumn += 1

		evalIndex = request.args.get("evalIndex")

		evaluaciones = bd.get_listaEvaluacionesAsignatura(con,asignaturaID,semester,year)
		asignatura = bd.get_nombre_asignatura(con,asignaturaID)
		
		items = bd.get_ItemsEvaluacion(con,evalID)
		
		alumnos = bd.get_listaAlumnosAsignaturaSemestre(con, asignaturaID, semester, year)

		for i in alumnos:
			flag = True
			
			for j in items:
				puntaje = bd.consultar_puntaje(con, i['num_matricula'], j['id_item'])
				if puntaje != None:
					i['evaluado'] = True
				else:
					i['evaluado'] = False
				break
	
		#print(alumnos)
		cantAlumnos = len(alumnos)
		
		# while num_alumn <= cantAlumnos and alumnos[num_alumn-1]['evaluado'] == True:
		# 	num_alumn += 1
		
		if num_alumn <= cantAlumnos:
			return render_template('evaluacion/addScore.html', asignatura=asignatura, evalIndex=evalIndex, alumnos=alumnos, items=items, al = alumnos[num_alumn-1], eval_ID = evalID, asignatura_ID = asignaturaID, eval_Index = evalIndex)
		else:
			return render_template('evaluacion/addScore.html', asignatura=asignatura, evalIndex=evalIndex, alumnos=alumnos, items=items, al = alumnos[0], eval_ID = evalID, asignatura_ID = asignaturaID, eval_Index = evalIndex)

	else:
		return redirect('/')
