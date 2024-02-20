import os
from flask import Flask
from flask import render_template, redirect, request, session, send_from_directory,jsonify
from flask_paginate import Pagination #Importando paquete de paginación
from valores import Valores
import psycopg2
from datetime import datetime
import pickle



# instancias
app=Flask(__name__)
mis_valores=Valores()
#configurar parametros App y conexion BBDD en desarrollo 
# (para produccion hay que cambiar a otra clase de archivo config)
app.config.from_object("config.ConfigPro")
basedir = os.path.abspath(os.path.dirname(__file__))
todas_las_categorias=""


"""db = psycopg2.connect(
        host=mis_valores.HOST,
        database=mis_valores.DB,
        user=mis_valores.USER,
        password=mis_valores.PASSWORD,
        sslmode= 'require')"""

#cursor = db.cursor()
"""cursor.execute("DROP TABLE IF EXISTS publicaciones   ")

cursor.execute("CREATE TABLE IF NOT EXISTS publicaciones(
            id    SERIAL PRIMARY KEY,
           nombre varchar (250),
           imagen varchar (250) ,
           descripcion varchar (250) ,
           categoria varchar (250) ,
           archivo varchar (250) ,
           fecha date ,
           habilitado boolean);
 ")"""
 

#db.commit()
#cursor.close()
#db.close() 

#rutas
@app.route("/")

def index():
 
  mis_valores.footer=True
  return render_template("/sitio/index.html",valores=mis_valores)




@app.route("/todas_las_categorias", methods=['POST', 'GET'])
def categorias():

   try:
    with open("categorias.pickle", "rb") as f:
        todas_las_categorias = pickle.load(f)
   except EOFError:
       todas_las_categorias =["error o vacio"]
   return jsonify(todas_las_categorias)

@app.route("/publicaciones", methods=['POST', 'GET'])
def publicaciones():
   global categorias
   per_page=3
   start_index=0
   mis_valores.footer=False
   db = psycopg2.connect(
       host=mis_valores.HOST,
       database=mis_valores.DB,
       user=mis_valores.USER,
       password=mis_valores.PASSWORD,
       sslmode='require')
   cursor = db.cursor()
   try:
    # Contar el número total de registros
    sql = "SELECT count(*) FROM publicaciones"
    data = []
    cursor.execute(sql,data)
    results = cursor.fetchone()
    count = results[-1]

    # Obtener el número de página actual y la cantidad de resultados por página
    page_num = request.args.get('page', 1, type=int)
    per_page = 3
    # Calcular el índice del primer registro y limitar la consulta a un rango de registros
    start_index = (page_num - 1) * per_page + 1
    sql = "SELECT * FROM publicaciones  ORDER BY id DESC LIMIT {} OFFSET {}".format(
        str(per_page), str(start_index-1))
    
    cursor.execute(sql)
    publicaciones=cursor.fetchall()
    # Calcular el índice del último registro
    end_index = min(start_index + per_page, count)
    # end_index = start_index + per_page - 1
    if end_index > count:
        end_index = count
    # Crear objeto paginable
    pagination = Pagination(page=page_num, total=count, per_page=per_page,
                            display_msg=f"Mostrando registros {start_index} - {end_index} de un total de <strong>({count})</strong>" )   
    
   except:
     publicaciones=""
     pagination=""
     sql = "SELECT * FROM publicaciones ORDER BY id DESC LIMIT {} OFFSET {}".format(str(per_page),str(start_index))

   finally:
     cursor.close()  
     db.close()
   
   return render_template("/sitio/publicaciones.html", valores=mis_valores,publicaciones=publicaciones,pagination=pagination,count=count,categorias=categorias)
 

@app.route("/consulta-categorias", methods=['POST', 'GET'])
def consulta():
   if request.args.get('mibusqueda'):
    busqueda = "'%"+ request.args.get('mibusqueda')+ "%'"
    busqueda=busqueda.lower()
   else:
     return "busqueda sin contenido" 
   
   mis_valores.footer = False
   db = psycopg2.connect(
       host=mis_valores.HOST,
       database=mis_valores.DB,
       user=mis_valores.USER,
       password=mis_valores.PASSWORD,
       sslmode='require')
   cursor = db.cursor()
   try:
    
    sql = "SELECT * FROM publicaciones WHERE lower(categoria) LIKE " + \
        busqueda + " OR lower(nombre) LIKE " + busqueda + " ORDER BY id DESC "

    cursor.execute(sql)
    publicaciones = cursor.fetchall()
    count = len(publicaciones)
   
   
   except:
     publicaciones = ""
     pagination = ""
     sql = sql

   finally:
     cursor.close()
     db.close()

   return jsonify({'htmlresponse': render_template("/sitio/busqueda.html", valores=mis_valores, publicaciones=publicaciones,count=count, busqueda=request.args.get('mibusqueda'))})


@app.route("/ultima_publicacion",methods = ['POST', 'GET'])
def ultima_publicacion():
   
   mis_valores.footer=True
   db = psycopg2.connect(
       host=mis_valores.HOST,
       database=mis_valores.DB,
       user=mis_valores.USER,
       password=mis_valores.PASSWORD,
       sslmode='require')
   cursor = db.cursor()
   try:
   
    sql = "SELECT * FROM publicaciones ORDER BY id DESC LIMIT 1 "
    cursor.execute(sql)
    publicaciones=cursor.fetchall()
   except:
    publicaciones=""
   finally:
         cursor.close()  
   
   return render_template("/sitio/publicaciones.html", valores=mis_valores,publicaciones=publicaciones,count=1)



@app.route("/publicaciones_portitulo/<titulo>",methods = ['POST', 'GET'])
def publicaciones_portitulo(titulo):
   per_page = 3
   start_index = 0
   titulo=titulo.lower()
   titulo = "'%"+ titulo+ "%'"
   mis_valores.footer = True
   db = psycopg2.connect(
       host=mis_valores.HOST,
       database=mis_valores.DB,
       user=mis_valores.USER,
       password=mis_valores.PASSWORD,
       sslmode='require')
   cursor = db.cursor()
   try:
    sql = "SELECT * FROM publicaciones WHERE lower(categoria) LIKE " + \
        titulo + " OR lower(nombre) LIKE " + titulo + " ORDER BY id DESC "
    cursor.execute(sql)
    publicaciones = cursor.fetchall()
   except:
    publicaciones=""  
   finally:
         cursor.close()  
   
   return render_template("/sitio/publicaciones.html", valores=mis_valores, publicaciones=publicaciones,pagination=False)


@app.route("/about")
def about():
  mis_valores.footer=True
  return render_template("/sitio/about.html", valores=mis_valores)


@app.route("/admin")
def admin_index():
   
   return render_template("/admin/index.html")
 

@app.route("/admin/publicaciones")
def admin_publicaciones():
  if session['usuario']=="Admin":
     db = psycopg2.connect(
       host=mis_valores.HOST,
       database=mis_valores.DB,
       user=mis_valores.USER,
       password=mis_valores.PASSWORD,
       sslmode='require')
     cursor = db.cursor()
     try:
      sql = "SELECT * FROM publicaciones ORDER BY id DESC "
      cursor.execute(sql)
      publicaciones=cursor.fetchall()
     except:
       publicaciones="" 
     finally:
         cursor.close()
     
     return render_template("/admin/publicaciones.html", publicaciones=publicaciones)
  return redirect("/login")





@app.route("/admin/publicaciones/guardar", methods=['POST'])
def admin_guardar_publicaciones():
  if session['usuario']=="Admin":
    nombre=(request.form['name_post'])
    nombre_imagen=(request.files['name_imagen_post']) 
    html_publicacion = (request.files['html_publicacion'])
    categoria =(request.form['tags'])
    nombre_imagen_nuevo=""
    html_publicacion_nuevo=""
    tiempo=datetime.now()
    hora=tiempo.strftime("%Y%H%M%S")
    fecha=tiempo
    if nombre_imagen.filename !="":
      nombre_imagen_nuevo=nombre_imagen.filename
      nombre_imagen.save(os.path.join(
          basedir, app.config['UPLOAD_FOLDER'], nombre_imagen_nuevo))
    if html_publicacion.filename != "":
       html_publicacion_nuevo =  html_publicacion.filename
       #html_publicacion.save("templates/sitio/posts/" + html_publicacion_nuevo)
       html_publicacion.save(os.path.join(
          basedir, app.config['UPLOAD_POST'], html_publicacion_nuevo))
    descripcion=""
  
    habilitado=True   
    
    db = psycopg2.connect(
        host=mis_valores.HOST,
        database=mis_valores.DB,
        user=mis_valores.USER,
        password=mis_valores.PASSWORD,
        sslmode='require')
    cursor = db.cursor()
    sql = "INSERT INTO publicaciones(nombre, descripcion, categoria,imagen,archivo,fecha,habilitado) VALUES ( %s,%s,%s,%s,%s,%s,%s);"
    datos = (nombre, descripcion,categoria,nombre_imagen_nuevo, html_publicacion_nuevo,fecha,habilitado)
    cursor.execute(sql,datos)
    db.commit()
    cursor.close()
   
    return redirect("/admin/publicaciones")
  return redirect("/login")

@app.route("/admin/publicaciones/update", methods=['POST'])
def admin_update_publicaciones():
  if session['usuario']=="Admin":
    id_post=request.form['id_post']
    nombre=request.form['name_post']
    nombre_imagen=request.files['name_imagen_post'] 
    html_publicacion = request.files['html_publicacion']
    try:
      categoria = (request.form['tags'])
    except:
      categoria=""  
    nombre_imagen_nuevo=""
    html_publicacion_nuevo=""
    tiempo=datetime.now()
    hora=tiempo.strftime("%Y%H%M%S")
    fecha=tiempo
    if nombre_imagen.filename !="":
      nombre_imagen_nuevo=nombre_imagen.filename
      nombre_imagen.save(os.path.join(
          basedir, app.config['UPLOAD_FOLDER'], nombre_imagen_nuevo))
    else:
      nombre_imagen_nuevo = request.form['old_name_imagen_post']
    if html_publicacion.filename != "":
       html_publicacion_nuevo = html_publicacion.filename
       html_publicacion.save(os.path.join(
           basedir, app.config['UPLOAD_POST'], html_publicacion_nuevo))
    else:
      html_publicacion_nuevo = request.form['old_html_publicacion']
    descripcion=""
    
    habilitado=True   
    
    db = psycopg2.connect(
        host=mis_valores.HOST,
        database=mis_valores.DB,
        user=mis_valores.USER,
        password=mis_valores.PASSWORD,
        sslmode='require')
    cursor = db.cursor()
    sql = "UPDATE publicaciones SET  nombre=%s, descripcion=%s, categoria=%s,imagen=%s,archivo=%s,fecha=%s,habilitado=%s where id=%s"
    datos = (nombre, descripcion,categoria,nombre_imagen_nuevo, html_publicacion_nuevo,fecha,habilitado,id_post)
    cursor.execute(sql,datos)
    db.commit()
    cursor.close()
    update_categorias(categoria)
    return redirect("/admin/publicaciones")
  return redirect("/login")
 
@app.route("/admin/publicaciones/borrar", methods=['POST'])
def admin_borrar_publicaciones():
   if session['usuario']=="Admin":

      id_borrar=request.form['id_borrar']
     
     
      db = psycopg2.connect(
          host=mis_valores.HOST,
          database=mis_valores.DB,
          user=mis_valores.USER,
          password=mis_valores.PASSWORD,
          sslmode='require')
      cursor = db.cursor()
      cursor.execute("DELETE from publicaciones WHERE id=%s",(id_borrar,))
      db.commit()
      cursor.close()
      return redirect("/admin/publicaciones")
   return redirect("/login")

@app.route("/admin/publicaciones/editar/", methods=['POST'])
def editar():
     if session['usuario']=="Admin":
        id_editar=request.form['id_editar']
        db = psycopg2.connect(
            host=mis_valores.HOST,
            database=mis_valores.DB,
            user=mis_valores.USER,
            password=mis_valores.PASSWORD,
            sslmode='require')
        cursor = db.cursor()
        cursor.execute("SELECT * from publicaciones WHERE id=%s",(id_editar,))
        publicaciones=cursor.fetchall()
        cursor.close()
        return render_template("admin/editar.html", publicaciones=publicaciones)
     return redirect("/login")

  
  
@app.route("/img/<imagen>")
def ver_imagen_libro(imagen):
  return send_from_directory( app.config['UPLOAD_FOLDER'], imagen)



  
@app.route("/post/<archivo>")
def ver_post_html(archivo):
  
  if archivo !="":
        return send_from_directory( app.config['UPLOAD_POST'], archivo)
  return False
  
@app.route("/login")
def admin_login():
  return render_template("/admin/login.html")


@app.route("/login", methods=['POST'])
def admin_login_post():
  user = request.form['user']
  password = request.form['pass']
  if user=="edugoyo" and password=="edugoyo.1968":
    session['login']=True
    session['usuario']="Admin"
  return redirect("/admin")
  
  
@app.route("/log-out")
def admin_log_out():
   session.clear()
   return redirect("/admin")
 
@app.route("/aside_categorias", methods=['POST', 'GET'])
def aside_categorias():
   try:
      with open("categorias.pickle", "rb") as f:
          categorias = pickle.load(f)
   except EOFError:
       categorias =["error o vacio"]
       
   return jsonify({'htmlresponse': render_template("/sitio/aside-contenido.html", valores=mis_valores,categorias=categorias)})


 
def update_categorias(dato):
   
    
    dato=dato.split(",")
    
    
    try:
      with open("categorias.pickle", "rb") as f:
        todas_las_categorias = pickle.load(f)
    except EOFError:
      todas_las_categorias = []
      return False
     
    todas_las_categorias.extend(dato)
    todas_las_categorias = list(set(todas_las_categorias))
    
    with open("categorias.pickle", "wb") as f:
      pickle.dump(todas_las_categorias, f)
  
   
    
    return True
  
# inicio app derarrollo
if __name__=="__main__":
  # app.run(debug=True) NO NECESARIO 
  # -- SE LEE DESDE ARCHIVO CONFIG-- (cambiar para produccion a otra clase)
  app.run(debug=True)