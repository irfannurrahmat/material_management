from odoo import http
from odoo.http import request, Response
from odoo.exceptions import ValidationError
import json
import requests


class MaterialController(http.Controller):
    
    @http.route('/api/material/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_material(self, **post_data):
        data = request.jsonrequest

        required_fields = ['material_code', 'material_name', 'material_type', 'material_buy_price', 'related_supplier']
        for field in required_fields:
            if field not in data:
                return {"error": f"{field} tidak ditemukan"}
        
        try:
            supplier = request.env['res.partner'].sudo().browse(int(data.get('related_supplier')))
            if not supplier.exists():
                return {"error": "Supplier tidak ditemukan"}

            material = request.env['material.material'].sudo().create({
                'material_code': data.get('material_code'),
                'material_name': data.get('material_name'),
                'material_type': data.get('material_type'),
                'material_buy_price': float(data.get('material_buy_price')),
                'related_supplier': supplier.id,
            })

            return {"success": True, "material_id": material.id}

        except ValidationError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Error: {str(e)}"}


    @http.route('/api/material/get', type='http', auth='public', methods=['GET'], csrf=False)
    def get_material_data(self, **kwargs):
        material_type = kwargs.get('material_type', False)

        domain = []
        if material_type:
            domain.append(('material_type', '=', material_type))

        materials = request.env['material.material'].sudo().search(domain)

        material_data = []
        for material in materials:
            material_data.append({
                'material_code': material.material_code,
                'material_name': material.material_name,
                'material_type': material.material_type,
                'material_buy_price': material.material_buy_price,
                'related_supplier': material.related_supplier.name if material.related_supplier else '',
            })

        return request.make_response(json.dumps(material_data), headers={'Content-Type': 'application/json'})

    @http.route('/api/material/update', type='json', auth='public', methods=['POST'], csrf=False)
    def update_material(self, **post_data):
        data = request.jsonrequest
        material_id = data.get('material_id')

        if not material_id:
            return {"error": "material_id is required"}

        try:
            material = request.env['material.material'].sudo().browse(int(material_id))
            if not material.exists():
                return {"error": "Material tidak ada"}

            update_data = {
                key: value for key, value in data.items() 
                if key in ['material_code', 'material_name', 'material_type', 'material_buy_price', 'related_supplier']
            }

            if 'related_supplier' in update_data:
                supplier = request.env['res.partner'].sudo().browse(int(update_data['related_supplier']))
                if not supplier.exists():
                    return {"error": "Supplier not found"}
                update_data['related_supplier'] = supplier.id

            material.write(update_data)
            return {"success": True, "message": "Material updated berhasil"}

        except ValidationError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Error: {str(e)}"}

    @http.route('/api/material/delete', type='json', auth='public', methods=['POST'], csrf=False)
    def delete_material(self, **post_data):
        data = request.jsonrequest
        material_id = data.get('material_id')

        if not material_id:
            return {"error": "material_id is required"}

        try:
            material = request.env['material.material'].sudo().browse(int(material_id))
            if not material.exists():
                return {"error": "Material tidak ditemukan"}

            material.unlink()
            return {"success": True, "message": "Material deleted berhasil"}

        except Exception as e:
            return {"error": f"Error: {str(e)}"}