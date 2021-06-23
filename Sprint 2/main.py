from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy

from login import LoginForm

import evaluacion
import modulo8 as bd
import ast


dbdir = 'postgresql://restay2016:IS2equipo4@plop.inf.udec.cl/restay2016'

app = Flask(__name__) 
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}

login_manager = LoginManager(app)
login_manager.login_view = "login"
db_alchemy = SQLAlchemy(app)

app.register_blueprint(evaluacion.bp)

import models

semester = 1
year = 2021
#idProf = "2"
con = bd.connect()

@login_manager.user_loader
def load_user(user_id):
    return models.Users.get_by_id(user_id)

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route('/asignatura/<codigoAsignatura>/addEval', methods = ['GET', 'POST'])
def addEval(codigoAsignatura = None):

	if request.method == 'POST':
		#SACAR DATOS DE LA EVALUACION
		puntajes = []
		cantItems = int(request.form.get("numItems"))
		ptotal = 0
		resultados = []
		enunciados = []
		comentarios = []
		for i in range(1,cantItems+1):
			puntajes.append(int(request.form.get("puntaje"+str(i))))
			ptotal+=puntajes[-1]
			resultados.append(request.form.getlist("RA-"+str(i)+"[]"))
			comentarios.append((request.form.getlist("COM-"+str(i)+"[]")))
			enunciados.append((request.form.get("EN-"+str(i))))
		print(comentarios)
		print(resultados)
		idEval = bd.nueva_Evaluacion(con,codigoAsignatura,semester,year,ptotal)
		for i in range(1,cantItems+1):
			idItem = bd.nuevo_Item(con, idEval ,puntajes[i-1],enunciados[i-1])
			for res in resultados[i-1]:
				res = ast.literal_eval(res)
				print(res)
				bd.asociar_ResultadoItem(con,idItem,res[0],comentarios[i-1][int(res[1])-1],1)
			
		return redirect(url_for('evaluacion.evaluation',asignaturaID = codigoAsignatura))


	nombreas= bd.get_nombre_asignatura(con,codigoAsignatura)
	print(nombreas)
	asignatura = {'codigo':codigoAsignatura,'nombre':nombreas}

	cantEval = len(bd.get_listaEvaluacionesAsignatura(con,codigoAsignatura,semester,year))

	RA = bd.get_ResultadosAsignatura(con,codigoAsignatura)
	return render_template('addEval2.html',asignatura = asignatura,nEval = cantEval + 1, RAs = RA)
	#return render_template('addEval.html',asignatura = asignatura,nEval = cantEval + 1, RAs = RA)


@app.route("/login/", methods = ['GET', 'POST'])
def login():
    
    form = LoginForm()
        #if current_user.is_authenticated:
        #    return redirect(url_for('index'))
    if request.method == 'POST':
        if form.validate_on_submit():
            user = models.Users.get_by_email(form.email.data)
            if user is not None and check_password_hash(user.password, form.password.data):
                login_user(user, remember = form.remember_me.data)
                next_page = request.args.get('next', None)
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('asignaturas')
                return redirect(next_page)
    return render_template("login.html", formul = form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))
    
@app.route('/asignaturas/')
@login_required
def asignaturas():
	idProfesor = models.Users.get_id(current_user)
	ramos =	bd.get_ClasesImpartidas(con, idProfesor, 1, 2021)
	
	return render_template('asignaturas.html',profesor = idProfesor, ramos = ramos, semester = semester, year = year)


@app.route('/asignatura/<codigoAsignatura>/')
@login_required
def infAsignatura(codigoAsignatura = None):
	nombreas = bd.get_nombre_asignatura(con,codigoAsignatura)
	print(nombreas)
	asignatura = {'codigo':codigoAsignatura,'nombre':nombreas}
	alumnos = bd.get_listaAlumnosAsignaturaSemestre(con,codigoAsignatura,semester,year)
	RA = bd.get_ResultadosAsignatura(con,codigoAsignatura)
	return render_template('infAsignatura.html',asignatura = asignatura, alumnos = alumnos,RAs = RA)


if __name__ == "__main__":
    db_alchemy.create_all()
    app.run(debug = True)