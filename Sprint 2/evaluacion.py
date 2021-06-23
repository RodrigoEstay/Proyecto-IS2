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

import models
from main import con

@bp.route("/asignatura/<asignaturaID>/eval")
@login_required
def evaluation(asignaturaID):

	idProfesor = models.Users.get_id(current_user)
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

	idProfesor = models.Users.get_id(current_user)
	asignaturasProfesor = bd.get_CodigosClasesImpartidas(con, idProfesor, semester, year)

	if asignaturaID in asignaturasProfesor:

		asignatura = bd.get_nombre_asignatura(con,asignaturaID)
		evalIndex = request.args.get("evalIndex")

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

		return render_template('evaluacion/detalles.html', asignatura=asignatura, evalIndex=evalIndex, items=items,
			RAItems=RAItems, RAEval=RAEval) 
	
	else:
		return redirect('/')


@bp.route("/asignatura/<asignaturaID>/eval/<int:evalID>/modificar", methods=['GET', 'POST'])
@login_required
def modificarEval(asignaturaID, evalID):

	pass 

@bp.route("/asignatura/<asignaturaID>/eval/<int:evalID>/addScore", methods=['GET', 'POST'])
@login_required
def addScore(asignaturaID, evalID):

	idProfesor = models.Users.get_id(current_user)
	asignaturasProfesor = bd.get_CodigosClasesImpartidas(con, idProfesor, semester, year)

	if asignaturaID in asignaturasProfesor:
		if request.method == "POST":

			puntajes = request.form.getlist("scores[]")
			matAlumno = request.form.get("alumno")
			itemsID = request.form.getlist("itemsID[]")

			for i in range(len(puntajes)):
				bd.ingresar_Puntaje(con, matAlumno, itemsID[i], puntajes[i])

		evalIndex = request.args.get("evalIndex")

		evaluaciones = bd.get_listaEvaluacionesAsignatura(con,asignaturaID,semester,year)
		asignatura = bd.get_nombre_asignatura(con,asignaturaID)
		
		items = bd.get_ItemsEvaluacion(con,evalID)
		
		alumnos = bd.get_listaAlumnosAsignaturaSemestre(con, asignaturaID, semester, year)

		return render_template('evaluacion/addScore.html', asignatura=asignatura, evalIndex=evalIndex, alumnos=alumnos, items=items)

	else:
		return redirect('/')
