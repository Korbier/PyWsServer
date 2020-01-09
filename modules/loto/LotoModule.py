import sys

from datetime             import datetime
from core.module.module   import Module
from core.module.message  import *

from modules.loto.service.LotoDaoService import LotoDaoService

class LotoModule(Module):

    """Module Loto"""

    KEYWORD_SELECT   = 'select'   # Usage: select 'number'
    KEYWORD_UNSELECT = 'unselect' # Usage: unselect 'number'
    KEYWORD_CLEAR    = 'clear'    # Usage: clear
    KEYWORD_LIST     = 'list'     # Usage: list

    def getName( self ):
        return 'loto'

    def setApplication( self, application ):
        super( LotoModule, self ).setApplication( application )
        self._service  = LotoDaoService()

    def start( self ):
        pass

    def onMessage( self, request ):

        topic    = request.topic
        args     = request.args
        response = None

        if topic == self.KEYWORD_SELECT:
            result   = self._service.select( args[0] )
            response = BroadcastResponse( request, result.success(), result.content )

        if topic == self.KEYWORD_UNSELECT:
            result   = self._service.unselect()
            response = BroadcastResponse( request, result.success(), result.content )

        if topic == self.KEYWORD_CLEAR:
            result   = self._service.clear()
            response = BroadcastResponse( request, result.success(), result.content )

        if topic == self.KEYWORD_LIST:
            result   = self._service.list()
            response = Response( request, result.success(), result.content )

        return response

    def onConsoleMessage( self, request ):
        response = super( LotoModule, self ).onConsoleMessage( request )
        return response
