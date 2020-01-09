#######
# Global context
#

import asyncio
from core.websocket.session import Session

class Context:

    def __init__( self, host, port ):
        self._host = host
        self._port = port
        self._sessions = {}

    def sessions( self ):
        return self._sessions

    def host( self ):
        return self._host

    def port( self ):
        return self._port

    async def open( self, websocket ):
        session = Session( self, websocket )
        self._sessions[session.id()] = session
        return session

    async def close( self, websocket ):
        session = next((self._sessions[s] for s in self._sessions if self._sessions[s].socket() == websocket), None)
        if session != None:
            del self._sessions[session.id()]

    def get( self, websocket ):
        return next((self._sessions[s] for s in self._sessions if self._sessions[s].socket() == websocket), None)

    async def broadcast( self, sender, message ):
        if self._sessions:       # asyncio.wait doesn't accept an empty list
            await asyncio.wait([self._sessions[uuid].send(message) for uuid in self._sessions])
