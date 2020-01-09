import sys

from datetime             import datetime
from core.module.module   import Module
from core.module.message  import *

from modules.property.service.PropertyDaoService import PropertyDaoService

class PropertyModule(Module):

    """Module permettant la mise à disposition de propriétés à la portée applicative"""

    KEYWORD_LIST  = 'list'  # Usage: list
    KEYWORD_GET   = 'get'   # Usage: get propertyName
    KEYWORD_SET   = 'set'   # Usage: set propertyName propertyValue
    KEYWORD_UNSET = 'unset' # Usage: unset propertyName

    def getName( self ):
        return 'property'

    def setApplication( self, application ):
        super( PropertyModule, self ).setApplication( application )
        self._service  = PropertyDaoService( self.application().database() )

    def initializeDatabase( self, database, root ):
        super( PropertyModule, self ).initializeDatabase(database, root)
        if self._service.isWritable( 'createdAt' ):
            self._service.uncheckedSet( 'createdAt', datetime.now(), False )
        self._service.uncheckedSet( 'startedAt', datetime.now(), False )

    def start( self ):
        pass

    def onMessage( self, request ):

        topic    = request.topic
        args     = request.args
        response = None

        if topic == self.KEYWORD_LIST:
            result   = self._service.findAll()
            response = Response( request, result.success(), result.content )

        if topic == self.KEYWORD_GET:
            result   = self._service.get( args[0] )
            response = Response( request, result.success(), result.content )

        if topic == self.KEYWORD_SET:
            result   = self._service.set( args[0], args[1] )
            response = BroadcastResponse( request, result.success(), result.content )

        if topic == self.KEYWORD_UNSET:
            result   = self._service.unset( args[0] )
            response = BroadcastResponse( request, result.success(), result.content )

        return response

    def onConsoleMessage( self, request ):

        response = super( PropertyModule, self ).onConsoleMessage( request )

        if not response:
            return response

        topic   = response.topic
        args    = response.args
        content = response.content

        if response.topic == self.KEYWORD_LIST:
            for property in content:
                self.application().console().print( f'{property} = {content[property][0]}' )

        if response.topic == self.KEYWORD_GET:
            self.application().console().print( f'{args[0]} = {content}' )

        if response.topic == self.KEYWORD_SET:
            self.application().console().print( f'property {args[0]} set to value "{args[1]}"' )

        if response.topic == self.KEYWORD_UNSET:
            self.application().console().print( f'property {args[0]} removed' )

        return response
