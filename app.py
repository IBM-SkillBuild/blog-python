#modulo principal
#importaciones.
import os
from flask import Flask
from flask import render_template, redirect, request, session, send_from_directory
from valores import Valores
import psycopg2
from datetime import datetime
# instancias
app=Flask(__name__)
mis_valores=Valores()

#configurar parametros App y conexion BBDD en desarrollo 
# (para produccion hay que cambiar a otra clase de archivo config)
app.config.from_object("config.ConfigPro")
basedir = os.path.abspath(os.path.dirname(__file__))
#firebase=firebase.FirebaseApplication("https://eduardo-cabrera.firebaseio.com/",None)
#recibido=firebase.delete("/datos",None)
tiempo=datetime.now()
fecha=tiempo
data = {'id': 3, 
        'nombre': "mi visita",
        'imagen': "2023075934_huawei-3.jpg",
        'descripcion':"",
        'categoria': "",
        'archivo': "2023133116_HUAWEI.html",
        'fecha':fecha,
        'habilitado':True}
#emviado = firebase.post("/datos", data)


db = psycopg2.connect(
        host=mis_valores.HOST,
        database=mis_valores.DB,
        user=mis_valores.USER,
        password=mis_valores.PASSWORD,
        sslmode= 'require')




#cursor.execute("""DROP TABLE IF EXISTS publicaciones   """)

#cursor.execute("""CREATE TABLE IF NOT EXISTS publicaciones(
          #  id    SERIAL PRIMARY KEY,
          #  nombre varchar (250),
          #  imagen varchar (250) ,
          #  descripcion varchar (250) ,
          #  categoria varchar (250) ,
          #  archivo varchar (250) ,
          #  fecha date ,
         #   habilitado boolean);
          #  """)


#rutas
@app.route("/")
def index():
 
  mis_valores.footer=True
  return render_template("/sitio/index.html",valores=mis_valores)


@app.route("/publicaciones", methods=['POST', 'GET'])
def publicaciones():
   
   mis_valores.footer=False
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
   
   return render_template("/sitio/publicaciones.html", valores=mis_valores,publicaciones=publicaciones)
 


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
   
   return render_template("/sitio/publicaciones.html", valores=mis_valores,publicaciones=publicaciones)



@app.route("/publicaciones_portitulo/<titulo>",methods = ['POST', 'GET'])
def publicaciones_portitulo(titulo):
   mis_valores.footer = True
   db = psycopg2.connect(
       host=mis_valores.HOST,
       database=mis_valores.DB,
       user=mis_valores.USER,
       password=mis_valores.PASSWORD,
       sslmode='require')
   cursor = db.cursor()
   try:
    cursor.execute("SELECT * FROM publicaciones WHERE nombre=%s", (titulo,))
    publicaciones = cursor.fetchall()
   except:
    publicaciones=""  
   finally:
         cursor.close()  
   
   return render_template("/sitio/publicaciones.html", valores=mis_valores, publicaciones=publicaciones)


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
    nombre_imagen_nuevo=""
    html_publicacion_nuevo=""
    tiempo=datetime.now()
    hora=tiempo.strftime("%Y%H%M%S")
    fecha=tiempo
    if nombre_imagen.filename !="":
      nombre_imagen_nuevo=hora+"_"+nombre_imagen.filename
      # nombre_imagen.save("templates/sitio/img/"+ nombre_imagen_nuevo)
      nombre_imagen.save(os.path.join(
          basedir, app.config['UPLOAD_FOLDER'], nombre_imagen_nuevo))
    if html_publicacion.filename != "":
       html_publicacion_nuevo = hora+"_"+ html_publicacion.filename
       #html_publicacion.save("templates/sitio/posts/" + html_publicacion_nuevo)
       html_publicacion.save(os.path.join(
          basedir, app.config['UPLOAD_POST'], html_publicacion_nuevo))
    descripcion=""
    categoria=""
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
    data={
          "nombre":nombre,
          "descripcion":descripcion,
          "categoria":categoria,
          "imagen":nombre_imagen_nuevo,
          "archivo":html_publicacion_nuevo,
          "fecha":fecha,
          "habilitado":habilitado}
    #enviado=firebase.post("/datos",data)
    return redirect("/admin/publicaciones")
  return redirect("/login")

@app.route("/admin/publicaciones/update", methods=['POST'])
def admin_update_publicaciones():
  if session['usuario']=="Admin":
    id_post=request.form['id_post']
    nombre=request.form['name_post']
    nombre_imagen=request.files['name_imagen_post'] 
    html_publicacion = request.files['html_publicacion']
    nombre_imagen_nuevo=""
    html_publicacion_nuevo=""
    tiempo=datetime.now()
    hora=tiempo.strftime("%Y%H%M%S")
    fecha=tiempo
    if nombre_imagen.filename !="":
      nombre_imagen_nuevo=hora+"_"+nombre_imagen.filename
      nombre_imagen.save(os.path.join(
          basedir, app.config['UPLOAD_FOLDER'], nombre_imagen_nuevo))
    else:
      nombre_imagen_nuevo = request.form['old_name_imagen_post']
    if html_publicacion.filename != "":
       html_publicacion_nuevo = hora+"_"+ html_publicacion.filename
       html_publicacion.save(os.path.join(
           basedir, app.config['UPLOAD_POST'], html_publicacion_nuevo))
    else:
      html_publicacion_nuevo = request.form['old_html_publicacion']
    descripcion=""
    categoria=""
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
  
# inicio app derarrollo
if __name__=="__main__":
  # app.run(debug=True) NO NECESARIO 
  # -- SE LEE DESDE ARCHIVO CONFIG-- (cambiar para produccion a otra clase)
  app.run()