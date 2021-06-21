from flask import Flask, render_template

app = Flask(__name__)
import evaluacion
import modulo8 as bd
app.register_blueprint(evaluacion.bp)

semester = 1
year = 2021
idProf = "2"
con = bd.connect()

@app.route('/asignatura/')
def asignaturas(idProfesor = None):
	ramos =	bd.get_ClasesImpartidas(con, idProf, 1, 2021)
	
	'''
	ramos.append({'nombre':'Ingenieria Software de Software II','semestre':'1', 'anio':'2021','cantEstudiantes':'20'})
	ramos.append({'nombre':'Ingenieria Software','semestre':'1', 'anio':'2021','cantEstudiantes':'20'})
	ramos.append({'nombre':'Ingenieria Software','semestre':'1', 'anio':'2021','cantEstudiantes':'20'})
	ramos.append({'nombre':'Ingenieria Software','semestre':'1', 'anio':'2021','cantEstudiantes':'20'})
	ramos.append({'nombre':'Ingenieria Software','semestre':'1', 'anio':'2021','cantEstudiantes':'20'})
	ramos.append({'nombre':'Ingenieria Software','semestre':'1', 'anio':'2021','cantEstudiantes':'20'})
	ramos.append({'nombre':'Ingenieria Software','semestre':'1', 'anio':'2021','cantEstudiantes':'20'})
	'''
	return render_template('asignaturas.html',profesor = idProfesor, ramos = ramos, semester = semester, year = year)

@app.route('/asignatura/<codigoAsignatura>')
def infAsignatura(codigoAsignatura = None):
	nombreas= bd.get_nombre_asignatura(con,codigoAsignatura)
	print(nombreas)
	asignatura = {'codigo':codigoAsignatura,'nombre':nombreas}
	alumnos = bd.get_listaAlumnosAsignaturaSemestre(con,codigoAsignatura,semester,year)
	
	return render_template('infAsignatura.html',asignatura = asignatura, alumnos = alumnos)

	#evaluacion.addScore 
if __name__ == '__main__':
	app.run(debug=True)
