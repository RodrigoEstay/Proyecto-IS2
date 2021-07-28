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
def RAInfo(asignaturaID, RAID):

	idProfesor = current_user.id
	asignaturasProfesor = bd.get_CodigosClasesImpartidas(con, idProfesor, semester, year)

	if asignaturaID in asignaturasProfesor:

		items = {}
		general = {"sum": 0., "total": 0.}
		alumnos = {}

		puntajes = []
		itemIDs = []	
		itemPuntMax = []
		itemPond = []

		infoRA = bd.get_dondeImparteRA(con, RAID)

		for row in infoRA:

			if row["evalID"] not in items:
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

			if res["id_item"] in itemIDs:
				ind = itemIDs.index(res["id_item"])
			else:
				continue

			itemPunt[ind] += res["puntaje_obtenido"]

			if res["id_alumno"] not in alumnos:
				alumnos[res["id_alumno"]] = {"sum": 0.}

			cumpl = (float(res["puntaje_obtenido"]) / itemPuntMax[ind]) * itemPond[ind]
			alumnos[res["id_alumno"]]["sum"] += cumpl
			generalSum += cumpl

		general["sum"] = generalSum / float(len(alumnos))
		print(items, general, alumnos)

		asignatura = bd.get_nombre_asignatura(con,asignaturaID)
		nombreRA = bd.get_nombreRA(con, RAID)

		return render_template('infoRA.html',items = items, general = general, RA = nombreRA, asignatura = asignatura, alumnos = alumnos)

	else:
		return redirect('/')
