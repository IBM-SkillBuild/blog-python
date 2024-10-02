# configuracion desarrollo
class ConfigDev():
  DEBUG=True
  TESTING=True
  UPLOAD_FOLDER = 'static/uploads'
  UPLOAD_POST = 'static/posts'
  SECRET_KEY="MyApp"
    
 
  
    
# configuracion produccion
class ConfigPro():
  DEBUG = False
  TESTING = False
  SECRET_KEY="MyApp"
  UPLOAD_FOLDER = 'static/uploads'
  UPLOAD_POST = 'static/posts'
  UPLOAD_AUDIO= 'static/audio'
 
  
  