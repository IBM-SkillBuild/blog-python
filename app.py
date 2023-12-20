#modulo principal

#importaciones
import os
from flask import Flask
from flask import render_template,redirect,request,session
from valores import Valores
from flask_mysqldb import MySQL
from flask import send_from_directory
from datetime import datetime

# instancias
app=Flask(__name__)
mis_valores=Valores()

#configurar parametros App y conexion BBDD en desarrollo 
# (para produccion hay que cambiar a otra clase de archivo config)
app.config.from_object("config.ConfigDevClever")
mysql = MySQL(app)




#rutas
@app.route("/")
def index():
 
  mis_valores.footer=True
  return render_template("sitio/index.html",valores=mis_valores)


@app.route("/publicaciones")
def publicaciones():
   mis_valores.footer=False
   cursor = mysql.connection.cursor()
   sql = "SELECT * FROM `publicaciones`ORDER BY  fecha DESC"
   cursor.execute(sql)
   publicaciones=cursor.fetchall()
   cursor.close()
   return render_template("sitio/publicaciones.html", valores=mis_valores,publicaciones=publicaciones)

@app.route("/ultima_publicacion")
def ultima_publicacion():
   mis_valores.footer=False
   cursor = mysql.connection.cursor()
   sql = "SELECT * FROM `publicaciones` ORDER BY fecha DESC LIMIT 1 "
   cursor.execute(sql)
   publicaciones=cursor.fetchall()
   cursor.close()
   return render_template("sitio/publicaciones.html", valores=mis_valores,publicaciones=publicaciones)



@app.route("/publicaciones_portitulo/<titulo>")
def publicaciones_portitulo(titulo):
   mis_valores.footer = False
   cursor = mysql.connection.cursor()
   cursor.execute("SELECT * FROM `publicaciones` WHERE nombre=%s", (titulo,))
   publicaciones = cursor.fetchall()
   cursor.close()
   return render_template("sitio/publicaciones.html", valores=mis_valores, publicaciones=publicaciones)


@app.route("/about")
def about():
  mis_valores.footer=True
  return render_template("sitio/about.html", valores=mis_valores)


@app.route("/admin")
def admin_index():
   
   return render_template("admin/index.html")
 

@app.route("/admin/publicaciones")
def admin_publicaciones():
  if session['usuario']=="Admin":
      cursor = mysql.connection.cursor()
      sql = "SELECT * FROM `publicaciones` ORDER BY fecha DESC"
      cursor.execute(sql)
      publicaciones=cursor.fetchall()
      cursor.close()
      return render_template("admin/publicaciones.html", publicaciones=publicaciones)
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
    fecha=tiempo.strftime('%Y-%m-%d %H:%M:%S')
    if nombre_imagen.filename !="":
      nombre_imagen_nuevo=hora+"_"+nombre_imagen.filename
      nombre_imagen.save("templates/sitio/img/"+ nombre_imagen_nuevo)
    if html_publicacion.filename != "":
       html_publicacion_nuevo = hora+"_"+ html_publicacion.filename
       html_publicacion.save("templates/sitio/posts/" + html_publicacion_nuevo)
    descripcion=""
    categoria=""
    habilitado=True   
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO `publicaciones` (`id`, `nombre`, `descripcion`, `categoria`,`imagen`,`archivo`,`fecha`,`habilitado`) VALUES (NULL, %s,%s,%s,%s,%s,%s,%s);"
    datos = (nombre, descripcion,categoria,nombre_imagen_nuevo, html_publicacion_nuevo,fecha,habilitado)
    cursor.execute(sql,datos)
    mysql.connection.commit()
    cursor.close()
    return redirect("/admin/publicaciones")
  return redirect("/login")

@app.route("/admin/publicaciones/update", methods=['POST'])
def admin_update_publicaciones():
  if session['usuario']=="Admin":
    id_post=(request.form['id_post'])
    nombre=(request.form['name_post'])
    nombre_imagen=(request.files['name_imagen_post']) 
    html_publicacion = (request.files['html_publicacion'])
    nombre_imagen_nuevo=""
    html_publicacion_nuevo=""
    tiempo=datetime.now()
    hora=tiempo.strftime("%Y%H%M%S")
    fecha=tiempo.strftime('%Y-%m-%d %H:%M:%S')
    if nombre_imagen.filename !="":
      nombre_imagen_nuevo=hora+"_"+nombre_imagen.filename
      nombre_imagen.save("templates/sitio/img/"+ nombre_imagen_nuevo)
    if html_publicacion.filename != "":
       html_publicacion_nuevo = hora+"_"+ html_publicacion.filename
       html_publicacion.save("templates/sitio/posts/" + html_publicacion_nuevo)
    descripcion=""
    categoria=""
    habilitado=True   
    cursor = mysql.connection.cursor()
    sql = "UPDATE `publicaciones` SET  `nombre`=%s, `descripcion`=%s, `categoria`=%s,`imagen`=%s,`archivo`=%s,`fecha`=%s,`habilitado`=%s where id=%s"
    datos = (nombre, descripcion,categoria,nombre_imagen_nuevo, html_publicacion_nuevo,fecha,habilitado,id_post)
    cursor.execute(sql,datos)
    mysql.connection.commit()
    cursor.close()
    return redirect("/admin/publicaciones")
  return redirect("/login")
 
@app.route("/admin/publicaciones/borrar", methods=['POST'])
def admin_borrar_publicaciones():
   if session['usuario']=="Admin":
      id_borrar=request.form['id_borrar']
      cursor = mysql.connection.cursor()
      cursor.execute("DELETE from publicaciones WHERE id=%s",(id_borrar,))
      mysql.connection.commit()
      cursor.close()
      return redirect("/admin/publicaciones")
   return redirect("/login")

@app.route("/admin/publicaciones/editar/", methods=['POST'])
def editar():
     if session['usuario']=="Admin":
        id_editar=request.form['id_editar']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from publicaciones WHERE id=%s",(id_editar,))
        publicaciones=cursor.fetchall()
        cursor.close()
        return render_template("admin/editar.html", publicaciones=publicaciones)
     return redirect("/login")

  
  
@app.route("/img/<imagen>")
def ver_imagen_libro(imagen):
  return send_from_directory(os.path.join("templates/sitio/img/"),imagen)


@app.route("/post/<archivo>")
def ver_post_html(archivo):
  return send_from_directory(os.path.join("templates/sitio/posts/"), archivo)

  
@app.route("/login")
def admin_login():
  return render_template("admin/login.html")


@app.route("/login", methods=['POST'])
def admin_login_post():
  user = request.form['user']
  password = request.form['pass']
  if user=="admin" and password=="123":
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