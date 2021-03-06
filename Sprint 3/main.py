from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash

from login import LoginForm

import evaluacion
import RAInfo
import modulo8 as bd
import ast
import copy

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

login_manager = LoginManager(app)
login_manager.login_view = "login"

app.register_blueprint(evaluacion.bp)
app.register_blueprint(RAInfo.bp)

semester = 1
year = 2021

con = bd.connect()

from Users import User

@login_manager.user_loader
def load_user(id):
	user = bd.get_datos_profesor(con, id)
	return User(user[0], user[1], user[2], user[3])


@app.route("/")
def index():
    return redirect(url_for('login'))


@app.route('/login/', methods = ['GET', 'POST'])
def login():
	form = LoginForm()

	if request.method == 'POST':
		if form.validate_on_submit():
			if bd.login(con, form.email.data):
				password_user = bd.get_password_profesor(con, form.email.data)
				if check_password_hash(password_user[0], form.password.data):
					rutProfesor = bd.get_rut_profesor(con, form.email.data)
					datosProfesor = bd.get_datos_profesor(con, rutProfesor[0])
					user = User(datosProfesor[0], datosProfesor[1], datosProfesor[2], datosProfesor[3])
					login_user(user, remember = form.remember_me.data)
					next_page = request.args.get('next', None)
					if not next_page or url_parse(next_page).netloc != '':
						next_page = url_for('asignaturas')
					return redirect(next_page)
	return render_template('login/login.html', formul = form)
	

@app.route('/asignatura/<codigoAsignatura>/addEval', methods=['GET', 'POST'])
def addEval(codigoAsignatura=None):
	idProfesor = current_user.id
	nombreProfesor = current_user.name
	asignaturasProfesor = bd.get_CodigosClasesImpartidas(
	    con, idProfesor, semester, year)

	if codigoAsignatura in asignaturasProfesor:

		if request.method == 'POST':
			# SACAR DATOS DE LA EVALUACION
			puntajes = []
			cantItems = int(request.form.get("numItems"))
			ptotal = 0
			#resultados = []
			enunciados = []
			#comentarios = []
			rees = [] #[id,comentario,ponderacion]
			nRes = request.form.getlist("numRA");
			for i in range(1, cantItems+1):
				puntajes.append(int(request.form.get("puntaje"+str(i))))
				ptotal += puntajes[-1]
				#resultados.append(request.form.getlist("RA-"+str(i)+"[]"))
				#comentarios.append((request.form.getlist("COM-"+str(i)+"[]")))
				enunciados.append((request.form.get("EN-"+str(i))))
				aux = []
				for j in range(0,int(nRes[i-1])):
					aux.append(request.form.getlist("RES-"+str(i)+"-"+str(j+1)))
				rees.append(aux)
				print(aux)
			
			idEval = bd.nueva_Evaluacion(con, codigoAsignatura, semester, year, ptotal)
			for i in range(1, cantItems+1):
				idItem = bd.nuevo_Item(con, idEval, puntajes[i-1], enunciados[i-1])
				for res in rees[i-1]:
					#res = ast.literal_eval(res)
					#print(res)
					bd.asociar_ResultadoItem(
					    con, idItem, res[0], res[1], res[2])

			return redirect(url_for('evaluacion.evaluation', asignaturaID=codigoAsignatura))

		nombreas = bd.get_nombre_asignatura(con, codigoAsignatura)
		asignatura = {'codigo': codigoAsignatura, 'nombre': nombreas}

		cantEval = len(bd.get_listaEvaluacionesAsignatura(
		    con, codigoAsignatura, semester, year))

		RA = bd.get_ResultadosAsignatura(con, codigoAsignatura)
		return render_template('addEval2.html', asignatura=asignatura, nEval=cantEval + 1, RAs=RA)
		# return render_template('addEval.html',asignatura = asignatura,nEval = cantEval + 1, RAs = RA)

	else:
		return redirect('/')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))
    
@app.route('/asignaturas/')
@login_required
def asignaturas():
	idProfesor = current_user.id
	nombreProfesor = current_user.name
	ramos =	bd.get_ClasesImpartidas(con, idProfesor, 1, 2021)
	
	return render_template('asignaturas.html',profesor = idProfesor, ramos = ramos, semester = semester, year = year)


@app.route('/asignatura/<codigoAsignatura>/alumnos/<idAlumno>')
@login_required
def infAlumno(codigoAsignatura = None, idAlumno = None):
	idProfesor = current_user.id
	nombreProfesor = current_user.name
	asignaturasProfesor = bd.get_CodigosClasesImpartidas(con, idProfesor, semester, year)

	if codigoAsignatura in asignaturasProfesor:
		nombreas = bd.get_nombre_asignatura(con,codigoAsignatura)
		nombreal = bd.get_nombre_alumno(con, idAlumno)
		alum = {'num_matricula':idAlumno, 'nombre':nombreal}
		asignatura = {'codigo':codigoAsignatura,'nombre':nombreas}
		RA = bd.get_ResultadosAsignatura(con,codigoAsignatura)
		evaluaciones = bd.get_listaEvaluacionesAsignatura(con,codigoAsignatura,semester,year)
		notasEval = []
		items = []
		resItem = []
		for ev in evaluaciones:
			aux = bd.get_ItemsEvaluacion(con,ev["id_evaluacion"])
			for it in aux:
				it["obtenido"] = bd.get_puntajesItem(con,idAlumno,it["id_item"])
			notasEval.append(aux)
			items.extend(aux)

		for it in items:
			resItem.append(bd.get_ResultadosItem(con, it["id_item"]))
		
		promAlumnos = {}		#PARA CALCULAR EL PROMEDIO DEL CURSO
		indiceRA = {}			#INDICE EN CADA LISTA DE EN DONDE ESTA EL RA
		tablas = []
		for idx,ra in enumerate(RA):
			promAlumnos[ra["id_resultado"]] = 0
			indiceRA[ra["id_resultado"]] = idx
			tablas.append([['Categoria','valor'],['Puntaje m??ximo',0],['Puntaje promedio',0],['Puntaje alumno',0]])
		alumnos = bd.get_listaAlumnosAsignaturaSemestre(con,codigoAsignatura,semester,year)
		flag = False
		for alumno in alumnos:
			
			for idx,it in enumerate(items):
				puntos = bd.get_puntajesItem(con,alumno["num_matricula"],it["id_item"])
				if puntos < 0:
					puntos = 0
				for raItem in resItem[idx]:
					idr = raItem["id_resultado"]
					pond = raItem["ponderacion"]
					sumar = puntos*pond/100
					#alumno["dataArray"][indiceRA[idr]][1] = alumno["dataArray"][indiceRA[idr]][1] + sumar
					if alumno["num_matricula"] == idAlumno:
						tablas[indiceRA[idr]][3][1] = tablas[indiceRA[idr]][3][1] + sumar
					promAlumnos[idr] = promAlumnos[idr] + sumar 
					if flag == False:
						tablas[indiceRA[idr]][1][1] = tablas[indiceRA[idr]][1][1] + it["puntaje_maximo"]*pond/100 
			flag = True
		
		for idr in promAlumnos:
			promAlumnos[idr] = promAlumnos[idr]/len(alumnos)
			tablas[indiceRA[idr]][2][1] = promAlumnos[idr]

		return render_template('detallesAlumno.html',asignatura = asignatura, alumno = alum, notasEval = notasEval, tablas = tablas)
	else:
		return redirect('/')

@app.route('/asignatura/<codigoAsignatura>/')
@login_required
def infAsignatura(codigoAsignatura = None):

	idProfesor = current_user.id
	nombreProfesor = current_user.name
	asignaturasProfesor = bd.get_CodigosClasesImpartidas(con, idProfesor, semester, year)

	if codigoAsignatura in asignaturasProfesor:
		nombreas = bd.get_nombre_asignatura(con,codigoAsignatura)
		#print(nombreas)
		asignatura = {'codigo':codigoAsignatura,'nombre':nombreas}
		alumnos = bd.get_listaAlumnosAsignaturaSemestre(con,codigoAsignatura,semester,year)

		#OBTENER DATOS PARA HACER GRAFICOS
		#obtener evaluaciones
		evaluaciones = bd.get_listaEvaluacionesAsignatura(con,codigoAsignatura,semester,year)
		#obtener items de evaluaciones
		items = []
		#obtener resultados de cada item
		resItem = []
		for ev in evaluaciones:
			
			items.extend(bd.get_ItemsEvaluacion(con,ev["id_evaluacion"]))
			
		for it in items:
			resItem.append(bd.get_ResultadosItem(con, it["id_item"]))
		
		RA = bd.get_ResultadosAsignatura(con,codigoAsignatura)

		promAlumnos = {}		#PARA CALCULAR EL PROMEDIO DEL CURSO
		indiceRA = {}			#INDICE EN CADA LISTA DE EN DONDE ESTA EL RA
		base = [['Name', 'Rendimiento alumno', 'Rendimiento general del curso']]
		for idx,ra in enumerate(RA):
			promAlumnos[ra["id_resultado"]] = 0
			indiceRA[ra["id_resultado"]] = idx+1
			base.append([ra["nombre"],0,0])

		#AGREGAR DATOS PARA GRAFICO
		for alumno in alumnos:
			alumno["dataArray"] = copy.deepcopy(base)
			for idx,it in enumerate(items):
				puntos = bd.get_puntajesItem(con,alumno["num_matricula"],it["id_item"])
				if puntos < 0:
					puntos = 0
				for raItem in resItem[idx]:
					idr = raItem["id_resultado"]
					pond = raItem["ponderacion"]
					sumar = puntos*pond/100
					alumno["dataArray"][indiceRA[idr]][1] = alumno["dataArray"][indiceRA[idr]][1] + sumar
					promAlumnos[idr] = promAlumnos[idr] + sumar 
		
		for idr in promAlumnos:
			promAlumnos[idr] = promAlumnos[idr]/len(alumnos)
		for alumno in alumnos:
			for ra in RA:
				alumno["dataArray"][indiceRA[ra["id_resultado"]]][2] = promAlumnos[ra["id_resultado"]] 

		return render_template('infAsignatura.html',asignatura = asignatura, alumnos = alumnos,RAs = RA)
	else:
		return redirect('/')

if __name__ == "__main__":
    app.run(debug = True)
