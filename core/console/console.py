import asyncio
import websockets

from threading import Thread
from core.module.message import *

class Console(Thread):

    def __init__( self, application ):
        super(Console, self).__init__()
        self._application = application

    def run( self ):
        asyncio.set_event_loop( asyncio.new_event_loop() )
        stopRequested = False;
        while not stopRequested:
            stopRequested = self._process( self._read() )

    def print( self, message ):
        print( f'   {message}' )

    def _read( self ):
        return input('>> ')

    def _process( self, input ):

        if input == 'exit':
            return True

        explode = input.split(' ')
        module  = explode[0];
        command = explode[1];
        args    = explode[2:];

        request   = Request( module, command, args );
        processed = False

        for module in self._application._modules:

            if module.getName() == request.module:
                response = module.onConsoleMessage( request )
                if response:
                    processed = True
                    if response.isBroadcast():
                        self._application.websocket().broadcast( response )
                        self.print( 'Response broadcasted to connected client')

        if not processed:
            self.print( 'unknown command' )

        return False
