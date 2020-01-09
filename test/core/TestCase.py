import os
import unittest

from core.database.Database import Database
from test.core.TestModule import TestModule

database_init_main = 'Q:/_sandbox_python/platform/modules'
database_init_test = 'Q:/_sandbox_python/platform/test/modules'

class TestCase(unittest.TestCase):

    def __init__( self, modulename, *args, **kwargs ):
        super( TestCase, self ).__init__(*args, **kwargs)
        self._modulename   = modulename
        self._databasename = f'Q:/_sandbox_python/platform/test/modules/{modulename}/data/{self.__class__.__name__}.db'

    def setUp(self):

        if os.path.exists( self._databasename ):
            os.remove( self._databasename )

        self._connection = Database()
        self._connection.connect( self._databasename )

        self._module = TestModule( self._modulename )
        self._module.initialize( self._connection, database_init_main, database_init_test )

    def tearDown(self):
        self._connection.disconnect()
        if os.path.exists( self._databasename ):
            os.remove( self._databasename )

    def connection( self ):
        return self._connection
