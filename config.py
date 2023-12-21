# configuracion desarrollo
class ConfigDev():
  DEBUG=True
  TESTING=True
  UPLOAD_FOLDER = 'static/uploads'
  UPLOAD_POST = 'static/posts'
  SECRET_KEY="MyApp"
  MYSQL_HOST="localhost"
  MYSQL_PORT=3306
  MYSQL_USER = "root"
  MYSQL_PASSWORD = ""
  MYSQL_DB = "sitio_libros"
  
# con BBDD Prueba
class ConfigDevClever():
  DEBUG=True
  TESTING=True
  SECRET_KEY="MyApp"
  UPLOAD_FOLDER = 'static/uploads'
  UPLOAD_POST = 'static/posts'
  MYSQL_HOST="bosodwapbqiuwcmr4zq3-mysql.services.clever-cloud.com"
  MYSQL_PORT=3306
  MYSQL_USER = "uep1zkomcvvfxz4n"
  MYSQL_PASSWORD = "qbt3U3B4zbHfM7H1cTlK"
  MYSQL_DB = "bosodwapbqiuwcmr4zq3"
  
    
# configuracion produccion
class ConfigPro():
  DEBUG = False
  TESTING = False
  SECRET_KEY="MyApp"
  UPLOAD_FOLDER = 'static/uploads'
  UPLOAD_POST = 'static/posts'
  MYSQL_HOST = "bosodwapbqiuwcmr4zq3-mysql.services.clever-cloud.com"
  MYSQL_PORT = 3306
  MYSQL_USER = "uep1zkomcvvfxz4n"
  MYSQL_PASSWORD = "qbt3U3B4zbHfM7H1cTlK"
  MYSQL_DB = "bosodwapbqiuwcmr4zq3"
  
  