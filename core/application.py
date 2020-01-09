from core.database.Database  import Database
from core.websocket.server   import WebsocketServer
from core.console.console    import Console

class Application:

    def __init__( self, database ):
        self._modules  = []
        self._database = Database()
        self._database.connect( database )

    def database( self ):
        return self._database

    def console( self ):
        return self._console

    def websocket( self ):
        return self._websocket

    def modules( self ):
        return self._modules

    def addModule( self, module ):
        module.setApplication( self )
        module.initializeDatabase( self.database(), 'modules' )
        module.start()
        self._modules.append( module )

    def run( self, host, port ):

        self._websocket = WebsocketServer( self, host, port )
        self._console   = Console( self )

        self._websocket.start()
        self._console.start()

        self._console.join()

        self._websocket.stop()
        self._database.disconnect()
