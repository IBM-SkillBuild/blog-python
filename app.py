import os
from flask import Flask
from flask import render_template, redirect, request, session, send_from_directory,jsonify,make_response, send_file, url_for
from flask_paginate import Pagination #Importando paquete de paginación
from valores import Valores
import psycopg2
from datetime import datetime
import pickle
import requests
from speechify.speechify import  SpeechifyAPI
from flask_cors import CORS
import random
from io import BytesIO
import time
from moviepy.editor import concatenate_audioclips, AudioFileClip







# instancias
app=Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST"]}})
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

@app.route("/doc")
def documentacion():
   return render_template("/sitio/api.html")
 
@app.route("/mostrar_api_audio")
def mostrar_api_audio():
   return render_template("/sitio/api-audio.html")
 
@app.route("/mostrar_api_foto_user_hombre")
def mostrar_api_foto_user_hombre():
   return render_template("/sitio/api-foto-user-hombre.html")
 
@app.route("/mostrar_api_foto_user_mujer")
def mostrar_api_foto_user_mujer():
   return render_template("/sitio/api-foto-user-mujer.html") 

@app.route("/mostrar_api_widget_hora_madrid")
def mostrar_api_widget_hora_madrid():
   return render_template("/sitio/api-clock.html") 


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


 
def dividir_texto(texto, longitud_aproximada=3000):
    """
    Divide el texto en trozos de longitud aproximada, respetando los puntos.
    """
    if not texto or len(texto.strip()) == 0:
        return []
    
    texto = texto.strip()
    trozos = []
    inicio = 0
    
    while inicio < len(texto):
        fin = min(inicio + longitud_aproximada, len(texto))
        
        if fin < len(texto):
            # Buscar el último punto dentro del rango
            ultimo_punto = texto.rfind('.', inicio, fin)
            
            if ultimo_punto != -1:
                fin = ultimo_punto + 1  # Incluir el punto
            else:
                # Si no hay punto, buscar el siguiente
                siguiente_punto = texto.find('.', fin)
                if siguiente_punto != -1:
                    fin = siguiente_punto + 1
                else:
                    # Si no hay puntos, buscar el último espacio
                    ultimo_espacio = texto.rfind(' ', inicio, fin)
                    if ultimo_espacio != -1:
                        fin = ultimo_espacio + 1
        
        trozo = texto[inicio:fin].strip()
        if trozo:  # Solo agregar trozos no vacíos
            trozos.append(trozo)
        
        inicio = fin
        
        # Prevenir bucle infinito
        if inicio >= len(texto):
            break
    
    # Si no se pudo dividir, devolver el texto completo
    if not trozos:
        trozos = [texto]
    
    print(f"Texto dividido en {len(trozos)} trozos:")
    for i, trozo in enumerate(trozos, 1):
        print(f"  Trozo {i}: {len(trozo)} caracteres")
    
    return trozos

def limpiar_archivos_temporales(archivos):
    """
    Limpia archivos temporales de manera segura
    """
    for archivo in archivos:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                print(f"Archivo temporal eliminado: {archivo}")
            except Exception as e:
                print(f"Error eliminando archivo temporal {archivo}: {str(e)}")

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
 
UPLOAD_PATH = 'static/audio/'
     
@app.route("/crear_audio/<text>", methods=['GET'])
def crear_audio(text):
       
     # Create an instance of the Speechify API
     speechify_api = SpeechifyAPI() 
     audio_file = speechify_api.generate_audio_files(text, "juan", "azure", "es-CR")     
     return  jsonify({"audio_url": "https://blog-edu-tech.koyeb.app/static/audio/"+audio_file}),200 
   
@app.route("/generar_audio/<text>", methods=['GET'])
def generar_audio(text):
    # Crear una instancia de la API Speechify
    speechify_api = SpeechifyAPI()
    audio_file = speechify_api.generate_audio_files(text, "juan", "azure", "es-CR")
    
    # Ruta completa del archivo en el servidor
    audio_path = os.path.join(os.getcwd(), "static/audio", audio_file)
    
    # Asegurarse de que el directorio exista (por si acaso)
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    
    # Verificar que el archivo exista
    max_wait = 10  # Máximo tiempo de espera en segundos
    wait_interval = 0.1  # Intervalo de verificación en segundos
    elapsed = 0
    
    while not os.path.exists(audio_path) and elapsed < max_wait:
        time.sleep(wait_interval)
        elapsed += wait_interval
    
    if not os.path.exists(audio_path):
        return "Error: El archivo de audio no se generó a tiempo", 500
    
    # Construir la URL del archivo
    url_audio = f"https://blog-edu-tech.koyeb.app/static/audio/{audio_file}"
    
    # Devolver HTML con el audio listo para reproducirse
    return f"""
    <h1>Audio Generado by Edu</h1>
    <audio id="audio" controls src="{url_audio}" autoplay></audio>
    """
                               
    
@app.route("/generar_audio_voces", methods=['POST'])
def generar_audio_voces():
    # Obtener parámetros del body de la petición
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "error": "Se requiere un JSON en el body de la petición"}), 400
    
    text = data.get('text', '')
    voz = data.get('voz', 'juan')  # Valor por defecto
    proveedor = data.get('proveedor', 'azure')  # Valor por defecto
    idioma = data.get('idioma', 'es-CR')  # Valor por defecto
    
    # Validar que el texto no esté vacío
    if not text:
        return jsonify({"success": False, "error": "El parámetro 'text' es obligatorio"}), 400
    
    print(f"Procesando texto de {len(text)} caracteres con voz: {voz}, proveedor: {proveedor}, idioma: {idioma}")
    
    # Crear una instancia de la API Speechify
    speechify_api = SpeechifyAPI()
    
    try:
        # Dividir el texto en trozos si es muy largo
        trozos = dividir_texto(text)
        print(f"Texto dividido en {len(trozos)} trozos")
        
        archivos_temporales = []
        timestamp = int(time.time())
        
        # Generar archivos de audio para cada trozo
        for contador, trozo in enumerate(trozos, 1):
            try:
                print(f"Generando audio para trozo {contador}/{len(trozos)} ({len(trozo)} caracteres)")
                
                audio_file = speechify_api.generate_audio_files(trozo, voz, proveedor, idioma)
                print(f"Archivo generado: {audio_file}")
                
                # Renombrar el archivo generado con un identificador único
                nombre_temporal = f"audio-{contador}-{timestamp}.mp3"
                ruta_temporal = os.path.join(os.getcwd(), "static/audio", nombre_temporal)
                
                # Renombrar el archivo original
                ruta_original = os.path.join(os.getcwd(), "static/audio", audio_file)
                
                # Esperar a que el archivo exista (máximo 30 segundos)
                max_wait = 30
                wait_interval = 0.5
                elapsed = 0
                
                while not os.path.exists(ruta_original) and elapsed < max_wait:
                    time.sleep(wait_interval)
                    elapsed += wait_interval
                
                if not os.path.exists(ruta_original):
                    raise Exception(f"El archivo {audio_file} no se generó después de {max_wait} segundos")
                
                # Verificar que el archivo no esté vacío
                if os.path.getsize(ruta_original) == 0:
                    raise Exception(f"El archivo {audio_file} está vacío")
                
                os.rename(ruta_original, ruta_temporal)
                archivos_temporales.append(ruta_temporal)
                print(f"Trozo {contador} procesado exitosamente")
                
            except Exception as e:
                print(f"Error en trozo {contador}: {str(e)}")
                # Limpiar archivos temporales en caso de error
                limpiar_archivos_temporales(archivos_temporales)
                return jsonify({
                    "success": False, 
                    "error": f"Error al generar audio del trozo {contador}: {str(e)}",
                    "trozo_fallido": contador,
                    "total_trozos": len(trozos)
                }), 500
        
        print(f"Todos los trozos generados. Archivos temporales: {len(archivos_temporales)}")
        
        # Si solo hay un trozo, devolver directamente
        if len(archivos_temporales) == 1:
            nombre_final = os.path.basename(archivos_temporales[0])
            url_audio = f"https://blog-edu-tech.koyeb.app/static/audio/{nombre_final}"
            
            return jsonify({
                "success": True,
                "audio_url": url_audio,
                "filename": nombre_final,
                "trozos_generados": len(trozos),
                "params": {
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "voz": voz,
                    "proveedor": proveedor,
                    "idioma": idioma
                }
            })
        
        # Si hay múltiples trozos, concatenarlos
        try:
            print("Iniciando concatenación de audio...")
            
            # Crear clips de audio y concatenarlos
            clips = []
            for archivo in archivos_temporales:
                try:
                    clip = AudioFileClip(archivo)
                    clips.append(clip)
                    print(f"Clip cargado: {archivo}")
                except Exception as e:
                    print(f"Error cargando clip {archivo}: {str(e)}")
                    raise e
            
            if not clips:
                raise Exception("No se pudieron cargar ningún clip de audio")
            
            audio_final = concatenate_audioclips(clips)
            print("Audio concatenado exitosamente")
            
            # Generar nombre único para el archivo final
            nombre_final = f"audio-final-{timestamp}.mp3"
            ruta_final = os.path.join(os.getcwd(), "static/audio", nombre_final)
            
            # Guardar el audio final
            audio_final.write_audiofile(ruta_final, verbose=False, logger=None)
            print(f"Audio final guardado: {ruta_final}")
            
            # Verificar que el archivo final existe y no está vacío
            if not os.path.exists(ruta_final) or os.path.getsize(ruta_final) == 0:
                raise Exception("El archivo final no se generó correctamente")
            
            # Limpiar archivos temporales
            limpiar_archivos_temporales(archivos_temporales)
            
            # Cerrar los clips para liberar memoria
            for clip in clips:
                try:
                    clip.close()
                except:
                    pass
            try:
                audio_final.close()
            except:
                pass
            
            # Construir la URL del archivo final
            url_audio = f"https://blog-edu-tech.koyeb.app/static/audio/{nombre_final}"
            
            print("Proceso completado exitosamente")
            
            return jsonify({
                "success": True,
                "audio_url": url_audio,
                "filename": nombre_final,
                "trozos_generados": len(trozos),
                "params": {
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "voz": voz,
                    "proveedor": proveedor,
                    "idioma": idioma
                }
            })
            
        except Exception as e:
            print(f"Error en concatenación: {str(e)}")
            # Limpiar archivos temporales en caso de error
            limpiar_archivos_temporales(archivos_temporales)
            return jsonify({
                "success": False, 
                "error": f"Error al concatenar audio: {str(e)}",
                "archivos_generados": len(archivos_temporales),
                "total_trozos": len(trozos)
            }), 500
            
    except Exception as e:
        print(f"Error general: {str(e)}")
        return jsonify({"success": False, "error": f"Error general: {str(e)}"}), 500

@app.route("/generar_audio_voces_get", methods=['GET'])
def generar_audio_voces_get():
    """
    Versión GET con limitaciones de longitud para compatibilidad.
    Para textos largos, usar la versión POST.
    """
    # Obtener parámetros de la URL
    text = request.args.get('text', '')
    voz = request.args.get('voz', 'juan')  # Valor por defecto
    proveedor = request.args.get('proveedor', 'azure')  # Valor por defecto
    idioma = request.args.get('idioma', 'es-CR')  # Valor por defecto
    
    # Validar que el texto no esté vacío
    if not text:
        return jsonify({"success": False, "error": "El parámetro 'text' es obligatorio"}), 400
    
    # Limitar la longitud para GET (máximo 2000 caracteres)
    if len(text) > 2000:
        return jsonify({
            "success": False, 
            "error": "Para textos largos (>2000 caracteres), usar POST en /generar_audio_voces",
            "texto_recibido": len(text),
            "limite": 2000
        }), 400
    
    # Crear una instancia de la API Speechify
    speechify_api = SpeechifyAPI()
    
    try:
        # Dividir el texto en trozos si es muy largo
        trozos = dividir_texto(text)
        archivos_temporales = []
        
        # Generar archivos de audio para cada trozo
        for contador, trozo in enumerate(trozos, 1):
            try:
                audio_file = speechify_api.generate_audio_files(trozo, voz, proveedor, idioma)
                
                # Renombrar el archivo generado con un identificador único
                nombre_temporal = f"audio-{contador}-{int(time.time())}.mp3"
                ruta_temporal = os.path.join(os.getcwd(), "static/audio", nombre_temporal)
                
                # Renombrar el archivo original
                ruta_original = os.path.join(os.getcwd(), "static/audio", audio_file)
                if os.path.exists(ruta_original):
                    os.rename(ruta_original, ruta_temporal)
                    archivos_temporales.append(ruta_temporal)
                
            except Exception as e:
                # Limpiar archivos temporales en caso de error
                for archivo in archivos_temporales:
                    if os.path.exists(archivo):
                        os.remove(archivo)
                return jsonify({"success": False, "error": f"Error al generar audio del trozo {contador}: {str(e)}"}), 500
        
        # Si solo hay un trozo, devolver directamente
        if len(archivos_temporales) == 1:
            nombre_final = archivos_temporales[0].split('/')[-1]
            url_audio = f"https://blog-edu-tech.koyeb.app/static/audio/{nombre_final}"
            
            return jsonify({
                "success": True,
                "audio_url": url_audio,
                "filename": nombre_final,
                "trozos_generados": len(trozos),
                "params": {
                    "text": text,
                    "voz": voz,
                    "proveedor": proveedor,
                    "idioma": idioma
                }
            })
        
        # Si hay múltiples trozos, concatenarlos
        try:
            # Crear clips de audio y concatenarlos
            clips = [AudioFileClip(archivo) for archivo in archivos_temporales]
            audio_final = concatenate_audioclips(clips)
            
            # Generar nombre único para el archivo final
            nombre_final = f"audio-final-{int(time.time())}.mp3"
            ruta_final = os.path.join(os.getcwd(), "static/audio", nombre_final)
            
            # Guardar el audio final
            audio_final.write_audiofile(ruta_final, verbose=False, logger=None)
            
            # Limpiar archivos temporales
            for archivo in archivos_temporales:
                if os.path.exists(archivo):
                    os.remove(archivo)
            
            # Cerrar los clips para liberar memoria
            for clip in clips:
                clip.close()
            audio_final.close()
            
            # Construir la URL del archivo final
            url_audio = f"https://blog-edu-tech.koyeb.app/static/audio/{nombre_final}"
            
            return jsonify({
                "success": True,
                "audio_url": url_audio,
                "filename": nombre_final,
                "trozos_generados": len(trozos),
                "params": {
                    "text": text,
                    "voz": voz,
                    "proveedor": proveedor,
                    "idioma": idioma
                }
            })
            
        except Exception as e:
            # Limpiar archivos temporales en caso de error
            for archivo in archivos_temporales:
                if os.path.exists(archivo):
                    os.remove(archivo)
            return jsonify({"success": False, "error": f"Error al concatenar audio: {str(e)}"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "error": f"Error general: {str(e)}"}), 500
                               
    




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
  
@app.route('/foto-mujer')
def get_foto_female():
    # URL de la API
    num_foto = random.randint(1, 99)
    url = f'https://randomuser.me/api/portraits/med/women/{num_foto}.jpg'

    # Hacer la solicitud GET
    response = requests.get(url)

    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Crear un archivo en memoria
        img = BytesIO(response.content)
        img.seek(0)
        
        # Crear una respuesta personalizada para añadir los encabezados
        response = make_response(send_file(img, mimetype='image/jpeg'))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    else:
        filepath = os.path.join(os.getcwd(), 'foto-mujer.jpeg')
        response = make_response(send_file(filepath, mimetype='image/jpeg'))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

@app.route('/foto-hombre')
def get_foto_male():
    # URL de la API
    num_foto = random.randint(1, 100)
    url = f'https://randomuser.me/api/portraits/med/men/{num_foto}.jpg'

    # Hacer la solicitud GET
    response = requests.get(url)

    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Crear un archivo en memoria
        img = BytesIO(response.content)
        img.seek(0)
        
        # Crear una respuesta personalizada para añadir los encabezados
        response = make_response(send_file(img, mimetype='image/jpeg'))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    else:
        filepath = os.path.join(os.getcwd(), 'foto-hombre.jpeg')
        response = make_response(send_file(filepath, mimetype='image/jpeg'))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return 
    
@app.route('/widget-hora-madrid')
def widget():
    return """
    <table style="width:180px;height:180px">
    <tr><td style="text-align: center;"><canvas id="canvas_tt67b8c1c981673" width="175" height="175"></canvas></td></tr>
    <tr><td style="text-align: center; font-weight: bold"><a href="" style="text-decoration: none" class="clock24" id="tz24-1740161481-c1141-eyJzaXplIjoiMTc1IiwiYmdjb2xvciI6IjAwOTlGRiIsImxhbmciOiJlcyIsInR5cGUiOiJhIiwiY2FudmFzX2lkIjoiY2FudmFzX3R0NjdiOGMxYzk4MTY3MyJ9" title="Madrid Hora" target="_blank" rel="nofollow"></a></td></tr>
</table>
<script type="text/javascript" src="//w.24timezones.com/l.js" async></script>
  
    """
# Lista original de objetos capcha (sin cambios)
imagenes = [
    {"nombre_archivo": "rhykleu.jpg", "contenido_foto": "cogeló"},
    {"nombre_archivo": "frkustge.webp", "contenido_foto": "un tonto convencido"},
    {"nombre_archivo": "yrftgdcjey.jpg", "contenido_foto": "el saber si ocupa lugar"},
    {"nombre_archivo": "judgvjeus.jpeg", "contenido_foto": "estoy a puntito"},
    {"nombre_archivo": "bsyhedirud.jpg", "contenido_foto": "magia"},
    {"nombre_archivo": "okusiethn.jpg", "contenido_foto": "no encuentro al capitán"},
    {"nombre_archivo": "wbudyhetfd.webp", "contenido_foto": "parece sal"},
    {"nombre_archivo": "plodyhr.jpeg", "contenido_foto": "que coincidencia"},
    {"nombre_archivo": "nhdijthf.jpg", "contenido_foto": "yo te lo dije"},
    {"nombre_archivo": "urjjduu.webp", "contenido_foto": "ya nunca te diré nada"},
    {"nombre_archivo": "yujhtyaaa.jpg", "contenido_foto": "es un canalla"},
    {"nombre_archivo": "dhhhhuu.webp", "contenido_foto": "esa moneda es mía"},
]

@app.route('/captcha', methods=['GET'])
def captcha():
    imagenes_reducidas = imagenes.copy()
    mitad = len(imagenes_reducidas) // 2
    while len(imagenes_reducidas) > mitad:
        imagenes_reducidas.pop(random.randint(0, len(imagenes_reducidas) - 1))
    
    lista_fotos = [img["nombre_archivo"] for img in imagenes_reducidas]
    elemento_seleccionado = random.choice(imagenes_reducidas)
    contenido_foto = elemento_seleccionado["contenido_foto"]
    
    return render_template('componentes/captcha.html', 
                         lista_de_fotos=lista_fotos, 
                         contenido_foto=contenido_foto)

@app.route('/validar_captcha', methods=['POST'])
def validar_captcha():
    nombre_archivo = request.form.get('nombre_archivo')
    contenido_foto = request.form.get('contenido_foto')
   
    for img in imagenes:
        if img["nombre_archivo"] == nombre_archivo and img["contenido_foto"] == contenido_foto:
            return '''
                <p style="color: green;">¡CAPTCHA válido!</p>
                <script>
                    setTimeout(() => {
                        const overlay = document.querySelector('.overlay');
                        if (overlay) {
                            overlay.remove();
                        }
                        // Opcional: Redirigir a la página deseada después de validar
                        //document.getElementById('htmx-back').innerHTML = '';
                        //window.location.href = "https://blog-edu-tech.koyeb.app";
                    }, 1000);
                </script>
            '''
    
    # Si el CAPTCHA falla (fuera del for)
    
    return redirect(url_for('captcha'))

@app.route('/esperar', methods=['POST', 'GET'])
def esperar():
    print("llega a esperar")
    return '''
  <div id="htmx-back">
    <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 20px; border: 1px solid #ccc; z-index: 1001;">
        <p style="color: red;">Reseteando intentos fallidos. Espera <span id="contador">3</span> segundos.</p>
        <script>
            (function() {
                // Reiniciar intentos_fallidos en localStorage
                localStorage.setItem('intentos_fallidos', '0');

                // Temporizador de 3 segundos
                let segundos = 3;
                const contador = document.getElementById('contador');
                
                // Limpiar cualquier intervalo previo (por si acaso)
                if (window.existingInterval) {
                    clearInterval(window.existingInterval);
                }

                // Iniciar el temporizador
                window.existingInterval = setInterval(() => {
                    segundos--;
                    contador.textContent = segundos;
                    if (segundos <= 0) {
                        clearInterval(window.existingInterval);
                        loadCaptcha();
                    }
                }, 1000);
            })();
        </script>
    </div>
</div>
    '''
        




    
      
# inicio app derarrollo
if __name__=="__main__":
  # app.run(debug=True) NO NECESARIO 
  # -- SE LEE DESDE ARCHIVO CONFIG-- (cambiar para produccion a otra clase)
  app.run(debug=True,port=5000)
  
#   exponer puerto en url cloudflared 
#   cloudflared-windows-amd64.exe tunnel --url http://localhost:5000