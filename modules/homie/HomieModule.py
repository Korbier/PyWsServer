import sys

from core.module.module   import Module
from core.module.message  import *

from modules.homie.service.MqttService import MqttService

class HomieModule(Module):

    def getName( self ):
        return 'homie'

    def setApplication( self, application ):
        super( HomieModule, self ).setApplication( application )
        self._mqtt               = MqttService()

    def start( self ):
        # self._mqtt.run()
        pass

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
