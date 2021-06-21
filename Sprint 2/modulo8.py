import psycopg2
import hashlib
from os import system, name

DB_NAME = "restay2016"
DB_USER = "restay2016"
DB_PASSWORD = "IS2equipo4"



# get_listaAlumnosAsignaturaSemestre(con,asignatura,semestre,year):
# 	num_matricula, nombre

# get_listaAsignaturasSemestre(con,asignatura,semestre,year):
# 	codigo_asignatura, nombre

# get_listaEvaluacionesAsignatura(con,asignatura,semestre,year):
# 	id_evaluacion, puntaje_maximo

# get_ItemsEvaluacion(con,evaluacion):
# 	id_item, puntaje_maximo, enunciado

# get_ResultadosAsignatura(con,asignatura):
# 	id_resultado, nombre

# get_ResultadosItem(con, item):
# 	id_resultado, nombre, comentario

# get_ClasesImpartidas(con,prof_id,semestre,year):
# 	nombre_asignatura, codigo, num_alumnos

# get_puntajesObtenidos(con,alumno,evaluacion):
# 	id_item, puntaje_obtenido



def connect():
	conn=None
	try:
		print('Attempting to connect to database...')
		conn = psycopg2.connect(host="plop.inf.udec.cl",database=DB_NAME,user=DB_USER,password=DB_PASSWORD)
		cur = conn.cursor()
		print('PostgreSQL database version:')
		cur.execute('SELECT version()')
		db_version = cur.fetchone()
		print(db_version)
	except(Exception,psycopg2.DatabaseError) as error:
		print(error)
	finally:
		return conn

def get_nombre_asignatura(con, codigo):

	cur = con.cursor()
	nombreas = ""
	try:
	#asignatura_semestre.codigo_asignatura = %s AND asignatura_semestre.codigo_asignatura=asignatura.codigo
		cur.execute('SELECT asignatura.nombre FROM asignatura WHERE asignatura.codigo = %s',(codigo,))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al comunicarse con la base de datos")
		print(error)
	else:
		nombreas = cur.fetchone()[0]

	cur.close()
	return nombreas
def close(connection):
	if connection is not None:
		connection.close()


def get_listaAlumnosAsignaturaSemestre(con,asignatura,semestre,year):
	cur = con.cursor()
	lista = []
	try:		
		cur.execute('SELECT alumno.num_matricula, alumno.nombre FROM alumno,cursa WHERE alumno.num_matricula = cursa.id_alumno AND cursa.codigo_asignatura =%s AND cursa.semestre = %s AND cursa.año = %s',(asignatura,semestre,year))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al comunicarse con la base de datos")
		print(error)
	else:
		for row in cur:
			lista.append({"num_matricula":row[0],"nombre":row[1]})
	cur.close()
	return lista


def get_listaAsignaturasSemestre(con,asignatura,semestre,year):
	cur = con.cursor()
	lista = []
	try:		
		cur.execute('SELECT asignatura.codigo,asignatura.nombre FROM asignatura,asignatura_semestre WHERE asignatura_semestre.codigo_asignatura = %s AND asignatura_semestre.semestre= %s AND asignatura_semestre.año = %s AND asignatura_semestre.codigo_asignatura=asignatura.codigo',(asignatura,semestre,year))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al comunicarse con la base de datos")
		print(error)
	else:
		for row in cur:
			lista.append({"codigo_asignatura":row[0],"nombre":row[1]})
	cur.close()
	return lista

def get_listaEvaluacionesAsignatura(con,asignatura,semestre,year):
	cur = con.cursor()
	lista = []
	try:		
		cur.execute('SELECT numero,puntaje_maximo FROM evaluacion WHERE evaluacion.codigo_asignatura = %s AND evaluacion.semestre = %s AND evaluacion.año = %s ',(asignatura,semestre,year))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al comunicarse con la base de datos")
		print(error)
	else:
		for row in cur:
			lista.append({"id_evaluacion":row[0],"puntaje_maximo":row[1]})
	cur.close()
	return lista

def get_ItemsEvaluacion(con,evaluacion):
	cur = con.cursor()
	lista = []
	try:		
		cur.execute('SELECT numero, puntaje_max, enunciado FROM item WHERE numero_eval = %s',(evaluacion,))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al comunicarse con la base de datos")
		print(error)
	else:
		for row in cur:
			lista.append({"id_item":row[0],"puntaje_maximo":row[1],"enunciado":row[2]})
	cur.close()
	return lista

def get_ResultadosAsignatura(con,asignatura):
	cur = con.cursor()
	lista = []
	try:		
		cur.execute('SELECT id_resultado,nombre FROM resultado_aprendizaje WHERE codigo_asignatura = %s',(asignatura))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al comunicarse con la base de datos")
		print(error)
	else:
		for row in cur:
			lista.append({"id_resultado":row[0],"nombre":row[1]})
	cur.close()
	return lista

def get_ResultadosItem(con, item):
	cur = con.cursor()
	lista = []
	try:		
		cur.execute('SELECT asignado_a.id_resultado_aprendizaje,resultado_aprendizaje.nombre,asignado_a.comentario FROM resultado_aprendizaje,asignado_a WHERE asignado_a.id_item = %s AND resultado_aprendizaje.id_resultado=asignado_a.id_resultado_aprendizaje',(item))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al comunicarse con la base de datos")
		print(error)
	else:
		for row in cur:
			lista.append({"id_resultado":row[0],"nombre":row[1],"comentario":row[2]})
	cur.close()
	return lista


def get_ClasesImpartidas(con,prof_id,semestre,year):
	cur = con.cursor()
	lista = []
	try:		
		cur.execute('SELECT A.nombre, I.codigo_asignatura, C.num_alumnos FROM imparte as I INNER JOIN (SELECT codigo_asignatura, COUNT(id_alumno) as num_alumnos FROM cursa GROUP BY codigo_asignatura) C ON C.codigo_asignatura=I.codigo_asignatura INNER JOIN (SELECT codigo, nombre FROM asignatura) A ON A.codigo=I.codigo_asignatura WHERE I.id_profesor = %s AND I.semestre = %s AND I.año = %s',(prof_id,semestre,year))
		#cur.execute('SELECT C.nombre,C.codigo_asignatura, COUNT(C.id_alumno) FROM (SELECT cursa.codigo_asignatura,asignatura.nombre,cursa.id_alumno, cursa.semestre,cursa.año FROM cursa, imparte,asignatura WHERE imparte.id_profesor=%s AND cursa.semestre=%s AND cursa.año=%s AND cursa.semestre=imparte.semestre AND cursa.año=imparte.año AND asignatura.codigo=cursa.codigo_asignatura) AS C GROUP BY C.codigo_asignatura, C.nombre',(prof_id,semestre,year))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al comunicarse con la base de datos")
		print(error)
	else:
		for row in cur:
			lista.append({"nombre_asignatura":row[0],"codigo":row[1],"num_alumnos":row[2]})
	cur.close()
	return lista

def get_puntajesObtenidos(con,alumno,evaluacion):
	cur = con.cursor()
	lista = []
	try:		
		cur.execute('SELECT puntaje_alumno.id_item, puntaje_alumno.puntaje_obtenido FROM puntaje_alumno,posee_item WHERE posee_item.id_evaluacion = %s AND posee_item.id_item = puntaje_alumno.id_item AND puntaje_alumno.id_alumno = %s ',(evaluacion,alumno))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al comunicarse con la base de datos")
		print(error)
	else:
		for row in cur:
			lista.append({"id_item":row[0],"puntaje_obtenido":row[1]})
	cur.close()
	return lista

def nueva_Evaluacion(con,codigo_asignatura,semestre,year,puntaje_max):
	cur=con.cursor()
	try:		
		cur.execute('INSERT INTO evaluacion (codigo_asignatura, semestre,año,puntaje_maximo) VALUES (%s, %s, %s, %s)',(codigo_asignatura,semestre,year,puntaje_max))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al insertar datos: ")
		print(error)
	else:
		con.commit()
	cur.close()

def nuevo_Item(con,evaluacion,puntaje_max,enunciado):
	cur=con.cursor()
	try:		
		cur.execute('INSERT INTO item (numero_eval,puntaje_maximo,enunciado) VALUES (%s, %s, %s)',(evaluacion,puntaje_max,enunciado))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al insertar datos: ")
		print(error)
	else:
		con.commit()
	cur.close()

def asociar_ResultadoItem(con,item,resultado,comentario,puntaje):
	cur=con.cursor()
	try:		
		cur.execute('INSERT INTO asignado_a (id_resultado_aprendizaje,id_item,comentario,puntaje) VALUES (%s, %s) ON CONFLICT ON CONSTRAINT asignado_a_pkey DO UPDATE SET comentario = EXCLUDED.comentario, puntaje = EXCLUDED.puntaje',(resultado,item,comentario,puntaje))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al insertar datos: ")
		print(error)
	else:
		con.commit()
	cur.close()

def ingresar_Puntaje(con,alumno,item,puntaje):
	cur=con.cursor()
	try:		
		cur.execute('INSERT INTO puntaje_alumno (id_alumno,id_item,puntaje_obtenido) VALUES (%s, %s, %s) ON CONFLICT ON CONSTRAINT puntaje_alumno_pkey DO UPDATE SET puntaje_obtenido = EXCLUDED.puntaje_obtenido',(alumno,item,puntaje))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al insertar datos: ")
		print(error)
	else:
		con.commit()
	cur.close()


def login(con,email,password):
	cur=con.cursor()
	hashpass = hashlib.md5(password)
	success = False
	lista = []
	try:		
		cur.execute('SELECT profesor.rut FROM profesor WHERE profesor.email = %s AND profesor.password = %s',(email,hashpass))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al comunicarse con la base de datos")
		print(error)
	else:
		if cur.rowcount==0:
			success=True
	
	cur.close()
	return success

def borrar_item(con, numeval, numitem):

	lista = get_ItemsEvaluacion(con, numeval)
	print("Lista:")
	idItem = lista[numitem-1]['id_item']

	cur=con.cursor()

	try:		
		cur.execute('DELETE FROM item WHERE numero = %s',(idItem,))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al borrar datos: ")
		print(error)
	else:
		con.commit()
		print("Se borro el item", numitem, "de la evaluacion", numeval)

	cur.close()


def agregarAlumno(con, numMatricula, nombre):	

	cur=con.cursor()

	try:		
		cur.execute('INSERT INTO alumno (num_matricula,nombre) VALUES (%s, %s)',(numMatricula, nombre))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al insertar datos: ")
		print(error)
	else:
		con.commit()
		print("Se ha ingresado el Alumno:", nombre)

	cur.close()

def agregarProfesor(con, rut, nombre, email, password):	

	cur=con.cursor()

	try:		
		cur.execute('INSERT INTO profesor (rut,nombre,email,password) VALUES (%s, %s, %s, %s)',(rut, nombre, email, password))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al insertar datos: ")
		print(error)
	else:
		con.commit()
		print("Se ha ingresado el Pofesor:",nombre)

	cur.close()

def agregarAsignatura(con, codigo, nombre):

	cur=con.cursor()

	try:		
		cur.execute('INSERT INTO asignatura (codigo,nombre) VALUES (%s, %s)',(codigo,nombre))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al insertar datos: ")
		print(error)
	else:
		con.commit()
		print("Se ha ingresado la asignatura:",nombre)

	cur.close()

def agregarAsignaturaSemestre(con, codigo, semestre, año):

	cur=con.cursor()

	try:		
		cur.execute('INSERT INTO asignatura_semestre (codigo_asignatura,semestre,año) VALUES (%s, %s, %s)',(codigo,semestre,año))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al insertar datos: ")
		print(error)
	else:
		con.commit()
		print("Se ha ingresado la asignatura semestral:", codigo)

	cur.close()

def agregarResultadoAprendizaje(con, codigo, nombre):

	cur=con.cursor()

	try:		
		cur.execute('INSERT INTO asignatura_semestre (codigo_asignatura,nombre) VALUES (%s, %s)',(codigo, nombre))
	except(Exception,psycopg2.DatabaseError) as error:
		print("Fallo al insertar datos: ")
		print(error)
	else:
		con.commit()
		print("Se ha ingresado el resultado de aprendizaje:", nombre,"\nAsociado a la asignatura:",codigo)

	cur.close()

