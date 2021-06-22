import functools
import modulo8 as bd
from flask_login import current_user, login_required

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

conn = bd.connect()
bp = Blueprint('evaluacion', __name__)

semester = 1
year = 2021

@bp.route("/asignatura/<asignaturaID>/eval")
@login_required
def evaluation(asignaturaID):
	evaluaciones = bd.get_listaEvaluacionesAsignatura(conn,asignaturaID,semester,year)
	asignaturas = {}
	asignaturas['name'] = bd.get_nombre_asignatura(conn,asignaturaID)
	asignaturas['ID'] = asignaturaID

	return render_template('evaluacion/eval.html', evaluaciones=evaluaciones, asignatura=asignaturas)


@bp.route("/asignatura/<asignaturaID>/eval/<int:evalID>/detalles")
@login_required
def detallesEval(asignaturaID, evalID):

	asignatura = bd.get_nombre_asignatura(conn,asignaturaID)
	evalIndex = request.args.get("evalIndex")
	items = bd.get_ItemsEvaluacion(conn,evalID)

	return render_template('evaluacion/addScore.html', asignatura=asignatura, evalIndex=evalIndex, items=items) 


@bp.route("/asignatura/<asignaturaID>/eval/<int:evalID>/modificar", methods=['GET', 'POST'])
@login_required
def modificarEval(asignaturaID, evalID):

	pass 

@bp.route("/asignatura/<asignaturaID>/eval/<int:evalID>/addScore", methods=['GET', 'POST'])
@login_required
def addScore(asignaturaID, evalID):

	if request.method == "POST":

		puntajes = request.form.getlist("scores[]")
		matAlumno = request.form.get("alumno")
		itemsID = request.form.getlist("itemsID[]")

		for i in range(len(puntajes)):
			bd.ingresar_Puntaje(conn, matAlumno, itemsID[i], puntajes[i])

	evalIndex = request.args.get("evalIndex")

	evaluaciones = bd.get_listaEvaluacionesAsignatura(conn,asignaturaID,semester,year)
	asignatura = bd.get_nombre_asignatura(conn,asignaturaID)
	
	items = bd.get_ItemsEvaluacion(conn,evalID)
	
	alumnos = bd.get_listaAlumnosAsignaturaSemestre(conn, asignaturaID, semester, year)

	return render_template('evaluacion/addScore.html', asignatura=asignatura, evalIndex=evalIndex, alumnos=alumnos, items=items)

