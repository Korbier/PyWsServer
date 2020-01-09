#######
# User session
#######

import uuid
from core.module.message import *

class Session:

    def __init__( self, context, websocket ):
        self._context   = context
        self._id        = uuid.uuid4()
        self._websocket = websocket

    def context( self ):
        return self._context

    def id( self ):
        return self._id

    def socket( self ):
        return self._websocket

    # Send a message to all context clients
    async def broadcast( self, message ):
        await self._context.broadcast( self, message )

    # Send a message to this client
    async def send( self, message ):
        await self.socket().send( encode(message) )
