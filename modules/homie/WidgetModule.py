import sys

from core.module.module   import Module
from core.module.message  import *

class WidgetModule(Module):

    KEYWORD_WIDGET_FIND       = 'widget/findbyid'     # Usage: widget/findbyid idWidget
    KEYWORD_WIDGET_FINDBYPAGE = 'widget/findbypage'   # Usage: widget/findbypage idPage
    KEYWORD_WIDGET_FINDALL    = 'widget/find/all'     # Usage: widget/all
    KEYWORD_WIDGET_CREATE     = 'widget/create'       # Usage: widget/create label idDevice idNode idProperty
    KEYWORD_WIDGET_DELETE     = 'widget/delete'       # Usage: widget/delete idWidget
    KEYWORD_WIDGET_UPDATE     = 'widget/update'       # Usage: widget/delete idWidget

    KEYWORD_PAGE_FIND    = 'page/find'     # Usage: page/find idPage
    KEYWORD_PAGE_FINDALL = 'page/find/all' # Usage: page/all
    KEYWORD_PAGE_CREATE  = 'page/create'   # Usage: page/create name label
    KEYWORD_PAGE_DELETE  = 'page/delete'   # Usage: page/delete idPage
    KEYWORD_PAGE_ADD     = 'page/add'      # Usage: page/add idPage idWidget
    KEYWORD_PAGE_REMOVE  = 'page/remove'   # Usage: page/remove idPage idWidget

    def getName( self ):
        return 'organizer'

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
