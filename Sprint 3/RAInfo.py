import functools
import modulo8 as bd
from flask_login import current_user, login_required

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint('evaluacion', __name__)

semester = 1
year = 2021

from main import con

@bp.route("/asignatura/<asignaturaID>/RA/<RAID>")
@login_required
def RAInfo(codigoAsignatura, RAID):

	idProfesor = current_user.id
	asignaturasProfesor = bd.get_CodigosClasesImpartidas(con, idProfesor, semester, year)

	if codigoAsignatura in asignaturasProfesor:
		nombreas = bd.get_nombre_asignatura(con,codigoAsignatura)
		print(nombreas)
		asignatura = {'ID':codigoAsignatura,'name':nombreas}
		alumnos = bd.get_listaAlumnosAsignaturaSemestre(con,codigoAsignatura,semester,year)
		RA = bd.get_ResultadosAsignatura(con,codigoAsignatura)
		return render_template('infoRA.html',asignatura = asignatura, alumnos = alumnos,RAs = RA)
	else:
		return redirect('/')
