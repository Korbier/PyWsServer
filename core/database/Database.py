import sys
import traceback
import sqlite3
from contextlib import closing

class Database:

    def connect( self, url ):
        self._database   = url
        self._connection = sqlite3.connect( url, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES, check_same_thread=False )
        self._connection.isolation_level = None
        self._commands =  []

    def disconnect( self ):
        self._connection.close()

    def queue( self, command, args = [] ):
        self._commands.append(SqlCommand(command, args))

    def executeQueue( self ):
        with closing( self._connection.cursor() ) as cursor:
            try:
                for command in self._commands:
                    cursor.execute( command.command(), command.args() )
                self._connection.commit()
                return Result( True, None )
            except:
                self._connection.rollback()
                return Result( False, None, traceback.format_exc() )

    def execute( self, request, args = () ):
        with closing( self._connection.cursor() ) as cursor:
            try:
                cursor.execute( request, args )
                self._connection.commit()
                return Result( True, cursor.lastrowid )
            except:
                self._connection.rollback()
                return Result( False, None, traceback.format_exc() )

    def fetch( self, request, args = () ):
        try:
            cursor = self._connection.cursor()
            cursor.execute( request )
            return Result( True, ResultSet(cursor, pagesize) )
        except:
            return Result( False, None, traceback.format_exc() )

    def fetchAll( self, request, args = () ):
        try:
            cursor = self._connection.cursor()
            cursor.execute( request, args )
            return Result( True, cursor )
        except:
            return Result( False, None, traceback.format_exc() )

    def fetchOne( self, request, args = () ):
        with closing( self._connection.cursor() ) as cursor:
            try:
                cursor.execute( request, args )
                return Result( True, cursor.fetchone() )
            except:
                return Result( False, None, traceback.format_exc() )

    def executeScript( self, filename ):
        with open( filename, 'r' ) as file:
            if file.mode == 'r':
                with closing( self._connection.cursor() ) as cursor:
                    try:
                        cursor.executescript( file.read() )
                        self._connection.commit()
                        return Result( True, None )
                    except:
                        self._connection.rollback()
                        return Result( False, None, traceback.format_exc() )

class Result:

    def __init__( self, result, content, trace = None ):
        self.result  = result
        self.content = content
        self.trace   = trace

    def failed( self ):
        return not self.result

    def success( self ):
        return self.result

class ResultSet:

    def __init__( self, cursor, step ):
        self._cursor  = cursor
        self._step    = step
        self._current = None

    def hasNext( self ):
        if self._step != None:
            self._current = self._cursor.fetchmany( self._step )
        else:
            self._current = self._cursor.fetchall()

        return len( self._current ) > 0

    def next( self ):
        return self._current;

    def close( self ):
        self._cursor.close()

class SqlCommand:

    def __init__(self, command, args ):
        self._command = command
        self._args    = args

    def command( self ):
        return self._command

    def args( self ):
        return self._args
