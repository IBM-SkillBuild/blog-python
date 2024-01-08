# configuracion desarrollo
class ConfigDev():
  DEBUG=True
  TESTING=True
  UPLOAD_FOLDER = 'static/uploads'
  UPLOAD_POST = 'static/posts'
  SECRET_KEY="MyApp"
  MYSQL_HOST = "db4free.net"
  MYSQL_PORT=3306
  MYSQL_USER = "blog_edu_user"
  MYSQL_PASSWORD = "1.6180339"
  MYSQL_DB = "blog_edu"
  
  
# con BBDD Prueba
class ConfigDevClever():
  DEBUG=True
  TESTING=True
  SECRET_KEY="MyApp"
  UPLOAD_FOLDER = 'static/uploads'
  UPLOAD_POST = 'static/posts'
  MYSQL_HOST = "db4free.net"
  MYSQL_PORT = 3306
  MYSQL_USER = "blog_edu_user"
  MYSQL_PASSWORD = "1.6180339"
  MYSQL_DB = "blog_edu"
 
  
    
# configuracion produccion
class ConfigPro():
  DEBUG = False
  TESTING = False
  SECRET_KEY="MyApp"
  UPLOAD_FOLDER = '/static/uploads'
  UPLOAD_POST = '/static/posts'
  MYSQL_HOST = "db4free.net"
  MYSQL_PORT = 3306
  MYSQL_USER = "blog_edu_user"
  MYSQL_PASSWORD = "1.6180339"
  MYSQL_DB = "blog_edu"
 
  
  