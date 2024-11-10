import os
from flask import Flask
from flask import render_template, redirect, request, session, send_from_directory,jsonify
from flask_paginate import Pagination #Importando paquete de paginación
from valores import Valores
import psycopg2
from datetime import datetime
import pickle
import requests
from speechify.speechify import  SpeechifyAPI
import uuid





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

#cursor = db.cursor()
#cursor.execute("DROP TABLE IF EXISTS usuarios  ")
#cursor.execute("CREATE TABLE usuarios(id serial PRIMARY KEY, nombre varchar(250), pass varchar(250));")
#sql = "INSERT INTO usuarios(nombre, pass) VALUES ( %s,%s);"
#datos = ("Edugoyo", "Edugoyo.1968")
#cursor.execute(sql,datos)
#db.commit()
#cursor.close()
   




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
  
  
  
@app.route("/usuarios/",methods = ['POST', 'GET'])
def usuarios():
   
   db = psycopg2.connect(
       host=mis_valores.HOST,
       database=mis_valores.DB,
       user=mis_valores.USER,
       password=mis_valores.PASSWORD,
       sslmode='require')
   cursor = db.cursor()
   try:
    sql = "SELECT * FROM usuarios"
    cursor.execute(sql)
    usuario = cursor.fetchall()
   except:
    usuario=""  
   finally:
         cursor.close()  
   return jsonify(usuario)
 
 
 
@app.route("/primitiva/", methods=['GET'])
def primitiva():
         

          date = datetime.now()
          fecha_hoy = date.strftime('%Y%m%d')
          num_sorteos=0
          lista=request.args.get('lista')
          
        
          contador=0     
          url = f"https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=LAPR&celebrados=true&fechaInicioInclusiva=20230923&fechaFinInclusiva={fecha_hoy}"
          data = requests.get(url)
          datos = data.json()
          num_sorteos=len(datos)
          ultima_semana=datos[0]['combinacion'][0:27].split(" - ")
          for sorteo in datos:
            try:
              if ( str(lista) in sorteo['combinacion'][0:27] ):
                contador +=1 
                sorteo["sale"]="sale el uno"  
            except:
              pass
          return render_template("/componentes/listado-primitiva.html",primitiva=datos,contador=contador,num_sorteos=num_sorteos,lista=lista,ultima_semana=ultima_semana)        
        
       
@app.route("/logica/", methods=['GET'])
def logica():
         
          
          date = datetime.now()
          fecha_hoy = date.strftime('%Y%m%d')
          num_sorteos=0
          lista=request.args.get('lista')
          lista=lista.split(",")
          lista.sort()  
          ok=""
          numeros_de_la_primitiva=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49']
          contador_de_grupos=[]
          contador_de_ausencias=[0,0,0,0,0,0]
          contador=[0,0,0,0,0,0]    
          numeros=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
          amigos=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]
          enemigos=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]
          consecutivos=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]
          lista_contador_de_consecutivos=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]

          veces_grupo="0"
          sugerencias=[" "," "," "," "," "," "]
          url = f"https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=LAPR&celebrados=true&fechaInicioInclusiva=20230923&fechaFinInclusiva={fecha_hoy}"
          data = requests.get(url)
          datos = data.json()
          num_sorteos=len(datos)
          
          for sorteo in datos:
             combinaciones= sorteo['combinacion'][0:27].split(" - ")
             for i in combinaciones:
               numeros[int(i)] +=1
          
                 
                  
                   
          for sorteo in datos:
            combinaciones= sorteo['combinacion'][0:27].split(" - ")
            for i in range(0,len(lista)): 
              if  str(lista[i]) in combinaciones :
               
                for item in combinaciones:
                  amigos[i].append(item)
                conjunto=set(amigos[i])  
                amigos[i]= [*conjunto]
                amigos[i].sort()
                enemigos[i] = [element for element in numeros_de_la_primitiva if element not in amigos[i]]
               
                contador[i]=contador[i]+1
               
              if contador[i]==0:
                  contador_de_ausencias[i]=contador_de_ausencias[i]+1
             
              sorteo["sale"]=f"sale numero {lista[i]}"  
             
              if contador[i]<15:
                 sugerencias[i]="Ha salido poco. Le doy muchas posibilidades"
              else:
                 sugerencias[i]="Hay mejores candidatos. A Este le doy pocas posibilidades"
              if contador_de_ausencias[i]>10:
                sugerencias[i]="Yo le doy muchas posibilidades"   
              elif contador_de_ausencias[i]>15:
                sugerencias[i]="Está deseando salir. Yo le doy muchas posibilidades" 
              else:
                 sugerencias[i]="Diría que tienes pocas posibilidades" 
              if contador[i]<7 | contador_de_ausencias[i]>20:
                sugerencias[i]=sugerencias[i]+" YO LO USARIA"  
              if contador_de_ausencias[i]<6:
                sugerencias[i]="Demasiado reciente. NO LO USARIA"   
             
          
            
         
          contador_de_consecutivos=0
          for sorteo in datos:  
               combinaciones= sorteo['combinacion'][0:27].split(" - ")
               contador_de_consecutivos +=1
              
               for item in lista:
                 i=int(item)
                 if item in combinaciones:
                 
                  lista_contador_de_consecutivos[i].append(contador_de_consecutivos)
                  if len(lista_contador_de_consecutivos[i])>1:
                    if lista_contador_de_consecutivos[i][-1] - lista_contador_de_consecutivos[i][-2]==1:
                      consecutivos[i].append(sorteo['fecha_sorteo'])
                  ok="se ha encontrado"
                 else:
                  ok="no se ha encontrado" 
                  break
                 
               if ok=="se ha encontrado":
                 contador_de_grupos.append(sorteo['fecha_sorteo'])
                 veces_grupo=len(contador_de_grupos)  
            
          return render_template("/componentes/logica-primitiva.html",primitiva=datos,
                                 contador=contador,num_sorteos=num_sorteos,
                                 lista=lista,combinaciones=combinaciones,
                                 contador_de_ausencias=contador_de_ausencias,
                                 ok=ok, contador_de_grupos=contador_de_grupos,
                                 sugerencias=sugerencias,veces=numeros, veces_grupo=veces_grupo,
                                 amigos=amigos,enemigos=enemigos,consecutivos=consecutivos)        
@app.route("/tabla/", methods=['GET'])
def tabla():
    date = datetime.now()
    fecha_hoy = date.strftime('%Y%m%d')
    url = f"https://www.loteriasyapuestas.es/servicios/buscadorSorteos?game_id=LAPR&celebrados=true&fechaInicioInclusiva=20230923&fechaFinInclusiva={fecha_hoy}"
    data = requests.get(url)
    datos = data.json()
    numeros=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for sorteo in datos:
             combinaciones= sorteo['combinacion'][0:27].split(" - ")
             for i in combinaciones:
               numeros[int(i)] +=1
          
    return render_template("/componentes/tabla.html",veces=numeros)      

listado_ocurrencias=[]    
posiciones=[]              
@app.route("/frase_quijote/", methods=['POST'])
def frase_quijote():
    busqueda= request.form['buscador']
    busqueda=busqueda.lower()
    if  busqueda=="":
       return render_template("/componentes/datos-quijote.html",
                             listado_ocurrencias=listado_ocurrencias,
                             posiciones=posiciones,registro=0)   
    inicio=0
    fin=0
    encontrado=""
        
    with open('./static/txt/quijote.txt', 'r', encoding="utf8") as archivo:
       quijote = archivo.read()
       quijote=quijote.lower()
    
    
    posicion = 0
    posiciones.clear()
    listado_ocurrencias.clear()
    while posicion != -1:
      posicion = quijote.find(busqueda,posicion)
      if posicion != -1:
        posiciones.append(posicion)
        posicion += 1
     
    
    contador=0
    for item in posiciones:
        
        encontrado=item
    
 
        for i in range(encontrado-1, 0, -1):
            if quijote[i]=="." :
              inicio=i+1
              break
          
        for i in range(encontrado+1,len(quijote),1):
            if quijote[i]=="." :
              fin=i+1
              break
            
        paragraph=quijote[inicio:fin]    
       
        listado_ocurrencias.append([paragraph,contador])
        contador +=1
       
       
        
    return render_template("/componentes/datos-quijote.html",
                             listado_ocurrencias=listado_ocurrencias,
                             posiciones=posiciones,registro=0)             

@app.route("/tts/", methods=['GET'])
def tts():
     registro = request.args.get('registro')
     registro=int(registro)
    
     # Create an instance of the Speechify API
     speechify_api = SpeechifyAPI() 
     audio_file = speechify_api.generate_audio_files(listado_ocurrencias[registro][0], "juan", "azure", "es-CR")     
     return render_template("/componentes/audio-quijote.html",
                            source=audio_file,texto=listado_ocurrencias[registro][0])       
     
@app.route("/crear_audio/<text>", methods=['GET'])
def crear_audio(text):
       
     # Create an instance of the Speechify API
     speechify_api = SpeechifyAPI() 
     audio_file = speechify_api.generate_audio_files(text, "juan", "azure", "es-CR")     
     return  jsonify({"audio_url": "https://blog-edu-tech.koyeb.app/static/audio/"+audio_file}),200 

UPLOAD_PATH = 'static/audio/'

@app.route('/borrar_audio', methods=['GET'])
def borrar_audio(): 
  for filename in os.listdir(UPLOAD_PATH):
    file_path = os.path.join(UPLOAD_PATH, filename)
    try:
      if os.path.isfile(file_path) or os.path.islink(file_path): os.unlink(file_path)
      print(f"{file_path} borrado exitosamente.")
    
    except Exception as e: print(f"No se pudo borrar {file_path}. Razón: {e}")
   
  return jsonify({"message": "Todos los archivos han sido borrados"}), 200
  
  
  
@app.route("/anterior/", methods=['GET'])
def anterior():
   registro=int(request.args.get('registro_anterior'))
   if registro ==-1:registro=len(posiciones)-1
  
   return render_template("/componentes/datos-quijote.html",
                             listado_ocurrencias=listado_ocurrencias,
                             posiciones=posiciones,registro=registro)     
  
@app.route("/siguiente/", methods=['GET'])
def siguiente():
   registro=int(request.args.get('registro_siguiente'))
   if registro>len(posiciones)-1:registro=0
   
   return render_template("/componentes/datos-quijote.html",
                             listado_ocurrencias=listado_ocurrencias,
                             posiciones=posiciones,registro=registro)     
  

      
# inicio app derarrollo
if __name__=="__main__":
  # app.run(debug=True) NO NECESARIO 
  # -- SE LEE DESDE ARCHIVO CONFIG-- (cambiar para produccion a otra clase)
  app.run(debug=True,port=3000)