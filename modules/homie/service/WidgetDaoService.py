from contextlib import closing

from core.database.Database     import Result
from core.database.SqlException import SqlException

from modules.homie.model.Widget import Widget

class WidgetDaoService:

    # 'widget/find'            # Usage: widget/find idWidget
    # 'widget/findbypage'      # Usage: widget/findbypage idPage
    # 'widget/find/all'        # Usage: widget/all
    # 'widget/create'          # Usage: widget/create label idDevice idNode idProperty
    # 'widget/delete'          # Usage: widget/delete idWidget

    def __init__( self, connection ):
        self._connection = connection

    def findById( self, id ):
        """Recherche un widget par son id"""
        result = self._connection.fetchOne('SELECT id, label, device, node, property FROM WIDGET WHERE id=?', (id,) )
        if not result.success() :
            raise WidgetDaoServiceException( f'Une erreur s\'est produite lors de l\'execution de la requete : {result.trace}' )
        elif not result.content:
            raise WidgetDaoServiceException( f'Aucun widget n\'a ete trouve pour l\'id {id}' )
        else:
            c = result.content
            return Widget(c[0], c[1], c[2], c[3], c[4])

    def findByPage( self, pageId ):
        """Recherche les widgets liés à la page fournie"""
        result = self._connection.fetchAll(
            'SELECT WIDGET.id, WIDGET.label, WIDGET.device, WIDGET.node, WIDGET.property'
            + ' FROM WIDGET '
            + ' INNER JOIN PAGE_WIDGET ON WIDGET.id=PAGE_WIDGET.widget AND PAGE_WIDGET.page=?', (pageId,) )
        if not result.success() :
            raise WidgetDaoServiceException( f'Une erreur s\'est produite lors de l\'execution de la requete : {result.trace}' )
        elif not result.content:
            return []
        else:
            records = []
            with closing(result.content) as cursor:
                for record in cursor:
                    records.append( Widget(record[0], record[1], record[2], record[3], record[4]) )
            return records

    def findAll( self ):
        """Retourne tous les widgets"""
        result = self._connection.fetchAll(
            'SELECT WIDGET.id, WIDGET.label, WIDGET.device, WIDGET.node, WIDGET.property FROM WIDGET ' )
        if not result.success() :
            raise WidgetDaoServiceException( f'Une erreur s\'est produite lors de l\'execution de la requete : {result.trace}' )
        elif not result.content:
            return []
        else:
            records = []
            with closing(result.content) as cursor:
                for record in cursor:
                    records.append( Widget(record[0], record[1], record[2], record[3], record[4]) )
            return records

    def create( self, label, device, node, property):
        """Retourne un nouveau widget avec le label fourni et la propriété Homie fournie"""
        result = self._connection.execute( "INSERT INTO WIDGET (label, device, node, property) VALUES(?,?,?,?)", (label, device, node, property) );
        if not result.success():
            raise WidgetDaoServiceException( f'Une erreur s\'est produite lors de l\'execution de la requete : {result.trace}' )
        else:
            return Widget(result.content, label, device, node, property)

    def delete( self, id ):
        """Supprime le widget fourni"""
        self._connection.queue( "DELETE FROM PAGE_WIDGET WHERE widget=?", (id,) )
        self._connection.queue( "DELETE FROM WIDGET WHERE id=?", (id,) )
        result = self._connection.executeQueue();
        if not result.success():
            raise WidgetDaoServiceException( f'Une erreur s\'est produite lors de l\'execution de la requete : {result.trace}' )
        else:
            return True

    def update( self, widget ):
        """Supprime le widget fourni"""
        self._connection.queue( "UPDATE WIDGET SET label=?, device=?, node=?, property=? WHERE id=?", (widget.label, widget.device, widget.node, widget.property, widget.id,) )
        result = self._connection.executeQueue();
        if not result.success():
            raise WidgetDaoServiceException( f'Une erreur s\'est produite lors de l\'execution de la requete : {result.trace}' )
        else:
            return True

class WidgetDaoServiceException(SqlException):
    def __init__(self, message):
        self.message = message
