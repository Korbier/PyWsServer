import json

def encode( message ):
    encoded = json.dumps( message, default=lambda o: o.__dict__,  sort_keys=True, indent=4 )
    return encoded

def decode( jsonMessage ):

    data = json.loads( jsonMessage )
    request = Request( data['module'], data['topic'] )

    if 'args' in data:
        request.setArgs( data['args'] )

    return request

class Request:

    def __init__( self, module, topic, args = [] ):
        self.module = module
        self.topic  = topic
        self.args  = args

    def setArgs( self, args ):
        self.args = args

    def clearArgs( self ):
        self.args.clear()

class Response:

    def __init__( self, request, result, content = None ):
        self.module  = request.module
        self.topic   = request.topic
        self.args    = request.args
        self.result  = result
        self.content = content

    def isBroadcast( self ):
        return False

class BroadcastResponse(Response):

    def isBroadcast( self ):
        return True
