import functools
import modulo8 as bd
from flask_login import current_user, login_required

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint('RAInfo', __name__)

semester = 1
year = 2021

#from main import con
con = bd.connect()


@bp.route("/asignatura/<asignaturaID>/RA/<RAID>")
@login_required
def RAInfo(codigoAsignatura, RAID):

	idProfesor = current_user.id
	asignaturasProfesor = bd.get_CodigosClasesImpartidas(con, idProfesor, semester, year)

	if codigoAsignatura in asignaturasProfesor:

		items = {}
		general = {"sum": 0., "total": 0.}
		alumnos = {}

		puntajes = []
		itemIDs = []	
		itemPuntMax = []
		itemPond = []

		infoRA = bd.get_dondeImparteRA(con, RAID)

		for row in infoRA:

			if row["evalID"] not in items["evalID"]:
				puntajes.extend(bd.get_resultadosEvaluacion(con, row['evalID']))
				items[row["evalID"]] = []

			items[row["evalID"]].append({"ponderacion": row["ponderacion"]})
			general["total"] += float(row["ponderacion"])
			itemIDs.append(row["itemID"])
			itemPuntMax.append(float(row["puntajeMax"]))
			itemPond.append(float(row["ponderacion"]))

		itemPunt = [0 for i in range(len(itemIDs))]
		generalSum = 0

		for res in puntajes:

			ind = itemIDs.index(res["id_item"])
			itemPunt[ind] += res["puntaje_obtenido"]

			if res["id_alumno"] not in alumnos:
				alumnos[res["id_alumno"]] = {"sum": 0., "total": general["total"]}

			alumnos[res["id_alumno"]]["sum"] += (float(res["puntaje_obtenido"]) / itemPuntMax[ind]) * itemPond[ind]

		print(items, general, alumnos)

		return render_template('infoRA.html',items = items, general = general, RA = "PRUEBA PRUEBA LOREM IPSUM")

	else:
		return redirect('/')
