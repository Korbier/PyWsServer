import unittest
import sys
import os

sys.path.append('Q:/_sandbox_python/_platform/websockets-7.0/src')
sys.path.append('Q:/_sandbox_python/_platform/paho-mqtt-1.4.0/src')
sys.path.append('Q:/_sandbox_python/platform')

from test.core.TestCase                     import TestCase
from modules.homie.service.WidgetDaoService import WidgetDaoService

class WidgetDaoServiceTest(TestCase):

    def __init__( self, *args, **kwargs ):
        super( WidgetDaoServiceTest, self ).__init__( 'homie', *args, **kwargs )

    def setUp(self):
        super( WidgetDaoServiceTest, self ).setUp()
        self._service = WidgetDaoService( self.connection() )

    def service(self):
        return self._service

    def test_findById( self ):
        widget = self.service().findById( 1 )
        self.assertEqual(widget.id,       1)
        self.assertEqual(widget.label,    'My first widget')
        self.assertEqual(widget.device,   'device1')
        self.assertEqual(widget.node,     'node1')
        self.assertEqual(widget.property, 'property1')

    def test_findByPage( self ):
        widgets = self.service().findByPage( 1 )
        self.assertEqual( len(widgets), 3 )

    def test_findAll( self ):
        widgets = self.service().findAll()
        self.assertEqual( len(widgets), 5 )

    def test_create( self ):
        widget = self.service().create( 'test', 'device', 'node', 'property' )
        self.assertIsNotNone( widget.id );
        widget2 = self.service().findById( widget.id )
        self.assertEqual(widget2.id,        widget.id)
        self.assertEqual(widget2.label,    'test')
        self.assertEqual(widget2.device,   'device')
        self.assertEqual(widget2.node,     'node')
        self.assertEqual(widget2.property, 'property')

    def test_delete( self ):
        result = self.service().delete(1)
        self.assertTrue( result )
        widgets = self.service().findAll()
        self.assertEqual( len(widgets), 4 )

    def test_update( self ):
        widget = self.service().findById( 1 )
        widget.label = 'Modified label'
        self.service().update( widget )
        widget2 = self.service().findById( 1 )
        self.assertEqual( widget2.label, 'Modified label' )


if __name__ == '__main__':
    unittest.main()
