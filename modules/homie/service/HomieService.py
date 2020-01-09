from contextlib import closing

class HomieService:

    def __init__( self ):
        pass

class HomieService(Exception):
    def __init__(self, message):
        self.message = message
