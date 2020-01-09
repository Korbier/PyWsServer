import sys

from core.module.module   import Module
from core.module.message  import *

class AdminModule(Module):
    
    """Module permettant l'administration de l'application"""
    
    ADMIN_MODULES = 'modules' # Usage: modules
    
    def getName( self ):
        return 'admin'

    async def onConnect( self, session ):
        self.application().console().print( f'New connection : {session.id()}')

    async def onDisconnect( self, session ):
        self.application().console().print( f'Connection closed : {session.id()}')

    def onMessage( self, request ):
    
        topic    = request.topic
        args     = request.args
        response = None

        if topic == self.ADMIN_MODULES:
            response = Response( request, True, self.application().modules() )
    
        return response
        
    def onConsoleMessage( self, request ):

        response = super( AdminModule, self ).onConsoleMessage( request )

        if not response:
            return response

        topic   = response.topic
        args    = response.args
        content = response.content

        if response.topic == self.ADMIN_MODULES:
            for module in content:
                self.application().console().print( f'{module.getName()}' )

        return response