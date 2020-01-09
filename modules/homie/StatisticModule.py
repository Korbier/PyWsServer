import sys

from core.module.module   import Module
from core.module.message  import *

class SupervisorModule(Module):

    def getName( self ):
        return 'statistic'

    def onMessage( self, request ):

        topic    = request.topic
        args     = request.args
        response = None

        return response

    def onConsoleMessage( self, request ):

        response = super( PropertiesModule, self ).onConsoleMessage( request )

        if not response:
            return response

        topic   = response.topic
        args    = response.args
        content = response.content


        return response
