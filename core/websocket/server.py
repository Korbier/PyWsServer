import asyncio
import websockets
from contextlib import suppress
from threading import Thread

from core.websocket.context  import Context
from core.module.message  import *

class WebsocketServer(Thread):

    def __init__( self, application, host, port ):
        super(WebsocketServer, self).__init__()
        self._context     = Context(host, port)
        self._application = application
        self._eventloop   = None
        self._poll_task   = None

    def context( self ):
        return self._context

    def broadcast( self, response ):
        asyncio.get_event_loop().run_until_complete( self._context.broadcast( None, response ) )

    def run( self ):
        self._eventloop = asyncio.new_event_loop()
        asyncio.set_event_loop( self._eventloop )
        try:
            self._poll_task = asyncio.ensure_future(self._poll())
            self._eventloop.run_until_complete(websockets.serve( self._handle, self._context.host(), self._context.port()))
            self._eventloop.run_forever()
            self._poll_task.cancel()
            with suppress(asyncio.CancelledError):
                self._eventloop.run_until_complete(self._poll_task)
        finally:
            self._eventloop.close()

    def stop( self ):
        self._eventloop.call_soon_threadsafe( self._eventloop.stop )

    async def _poll(self):
        while True:
            await asyncio.sleep(1.0)

    async def _fireConnectEvent( self, session ):
        for module in self._application._modules:
            await module.onConnect( session );

    async def _fireDisconnectEvent( self, session ):
        for module in self._application._modules:
            await module.onDisconnect( session );

    async def _fireMessageEvent( self, session, request ):
        decoded = decode( request )
        for module in self._application._modules:
            if module.getName() == decoded.module:
                response = module.onMessage( decoded )
                if response:
                    if response.isBroadcast():
                        await session.broadcast( response )
                    else:
                        await session.send( response )

    async def _handle(self, websocket, path):
        await self._context.open( websocket )
        try:
            await self._fireConnectEvent( self._context.get( websocket ) )
            async for wsMessage in websocket:
                await self._fireMessageEvent( self._context.get( websocket ), wsMessage )
        finally:
            await self._fireDisconnectEvent( self._context.get( websocket ) )
            await self._context.close( websocket )
