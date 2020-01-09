from contextlib import closing
from core.database.Database     import Result
from core.database.SqlException import SqlException

import collections

class LotoDaoService:

    def __init__( self ):
        self._values = {}
        
    def select( self, number ):
        self._values[number] = number
        return Result( True, list(self._values.keys()) )

    def unselect( self ):
        cle = list(self._values.keys())[-1]
        self._values.pop( cle )
        return Result( True, list(self._values.keys()) )

    def clear( self ):
        self._values  = {}
        return Result( True, list(self._values.keys()) )

    def list( self ):
        return Result( True, list(self._values.keys()) )
