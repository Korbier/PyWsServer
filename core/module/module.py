import glob
import re

class Module:

    def __init__( self ):
        self._context = None

    def setApplication( self, application ):
        self._application = application

    def getName( self ):
        return None

    def application( self ):
        return self._application

    def start( self ):
        pass

    def stop( self ):
        pass

    async def onConnect( self, session ):
        pass

    async def onDisconnect( self, session ):
        pass

    def onMessage( self, request ):
        pass

    def onConsoleMessage( self, request ):
        return self.onMessage( request )

    def initializeDatabase( self, database, root ):

        regex = re.compile(r'database_([0-9]+).sql')
        files = [f for f in glob.glob( f'{root}/{self.getName()}/init**/database_*.sql', recursive=False)]
        files.sort(reverse=True)

        if len(files) > 0:
            #print( f'[Module {self.getName()}] Applying script {files[0]}' )
            result = database.executeScript( files[0] )
            if result.success():
            #    print( f'[Module {self.getName()}] Script applied successfully')
                pass
            else:
            #   print( f'[Module {self.getName()}] An error occured : \n {result[1]}')
                pass
        else:
        #   print( f'[Module {self.getName()}] No script found')
            pass
