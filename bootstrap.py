import sys

#sys.path.append('Q:/_sandbox_python/_platform/websockets-7.0/src')
#sys.path.append('Q:/_sandbox_python/_platform/paho-mqtt-1.4.0/src')
sys.path.append('.') # Permet les includes depuis le repertoire courant, pas terrible

from core.application                import Application
from modules.property.PropertyModule import PropertyModule
from modules.admin.AdminModule       import AdminModule
from modules.loto.LotoModule         import LotoModule
#from modules.homie.HomieModule       import HomieModule

if __name__ == "__main__":
    application = Application( 'data/application.db' )
    application.addModule( AdminModule() )
    application.addModule( PropertyModule() )
    application.addModule( LotoModule() )
    application.run( 'localhost', 6789 )
