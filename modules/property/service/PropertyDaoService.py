from contextlib import closing
from core.database.Database     import Result
from core.database.SqlException import SqlException

class PropertyDaoService:

    def __init__( self, connection ):
        self._connection = connection

    def findAll( self ):
        properties = {}
        fetchresult = self._connection.fetchAll( 'SELECT name, value, writable FROM PROPERTIES ORDER BY name' )
        if fetchresult.success:
            with closing(fetchresult.content) as cursor:
                for record in cursor:
                    properties[record[0]] = (record[1], True if record[2] == 1 else False)
        return Result( True, properties )

    def isWritable( self, name ):
        value = self._connection.fetchOne( 'SELECT writable FROM PROPERTIES WHERE name=?', (name,) )
        if value.success():
            return Result( True, True if value.content[0] == 1 else False )
        else:
            return Result( False, None )

    def get( self, name ):
        return self._connection.fetchOne( 'SELECT value FROM PROPERTIES WHERE name=?', (name,) )

    def set( self, name, value ):
        writable = self.isWritable( name )
        if writable.success() and writable.content:
            return self.uncheckedSet( name, value, True )
        else:
            return Result( False, None )

    def unset( self, name):
        if self.isWritable( name ):
            return self.uncheckedUnset( name )
        else:
            return Result( False, None )

    def uncheckedSet( self, name, value, writable ):
        iWritable = 1 if writable else 0
        return self._connection.execute( '''REPLACE INTO PROPERTIES(name, value, writable) VALUES(?,?,?)''', (name, value, iWritable, ) )

    def uncheckedUnset( self, name ):
        return self._connection.execute( '''DELETE FROM PROPERTIES WHERE name = ?''', (name, ) )

class PropertiesDaoServiceSqlException(SqlException):
    def __init__(self, message):
        self.message = message
