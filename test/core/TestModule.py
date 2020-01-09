from core.module.module   import Module

class TestModule(Module):

    def __init__( self, name ):
        super( TestModule, self ).__init__()
        self._name = name;

    def getName( self ):
        return self._name

    def initialize( self, connection, main_script, test_script ):
        self.initializeDatabase( connection, main_script )
        self.initializeDatabase( connection, test_script )
