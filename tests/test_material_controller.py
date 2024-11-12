import unittest
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestMaterialController(TransactionCase):
    
    def setUp(self):
        super(TestMaterialController, self).setUp()
        self.supplier = self.env['res.partner'].create({
            'name': 'Supplier A',
            'supplier': True,
        })
        self.material = self.env['material.material'].create({
            'material_code': 'M001',
            'material_name': 'Material A',
            'material_type': 'Type A',
            'material_buy_price': 1000.0,
            'related_supplier': self.supplier.id,
        })

    def test_create_material(self):
        new_material_data = {
            'material_code': 'M002',
            'material_name': 'Material B',
            'material_type': 'Type B',
            'material_buy_price': 2000.0,
            'related_supplier': self.supplier.id,
        }
        
        response = self.client.post('/api/material/create', json=new_material_data)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertTrue(response_json['success'])
        self.assertIn('material_id', response_json)

    def test_create_material_missing_field(self):
        new_material_data = {
            'material_code': 'M003',
            'material_name': 'Material C',
            # Missing 'material_type'
            'material_buy_price': 3000.0,
            'related_supplier': self.supplier.id,
        }
        
        response = self.client.post('/api/material/create', json=new_material_data)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIn('error', response_json)

    def test_get_material_data(self):
        response = self.client.get('/api/material/get')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIsInstance(response_json, list)
        self.assertGreater(len(response_json), 0)

    def test_update_material(self):
        update_data = {
            'material_id': self.material.id,
            'material_name': 'Updated Material',
            'material_buy_price': 1500.0,
            'related_supplier': self.supplier.id,
        }
        
        response = self.client.post('/api/material/update', json=update_data)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertTrue(response_json['success'])
        self.material.refresh()
        self.assertEqual(self.material.material_name, 'Updated Material')

    def test_delete_material(self):
        delete_data = {
            'material_id': self.material.id,
        }
        
        response = self.client.post('/api/material/delete', json=delete_data)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertTrue(response_json['success'])
        # Memastikan material sudah terhapus
        deleted_material = self.env['material.material'].browse(self.material.id)
        self.assertFalse(deleted_material.exists())

    def test_delete_material_not_found(self):
        delete_data = {
            'material_id': 9999,
        }
        
        response = self.client.post('/api/material/delete', json=delete_data)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIn('error', response_json)
