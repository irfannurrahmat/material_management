from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Material(models.Model):
    _name = 'material.material'
    _description = 'Material Info'

    material_code = fields.Char(string="Material Code", required=True)
    material_name = fields.Char(string="Material Name", required=True)
    material_type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton'),
    ], string="Material Type", required=True)
    material_buy_price = fields.Float(string="Material Buy Price", required=True)
    related_supplier = fields.Many2one('res.partner', string='Related Supplier', required=True)
    
    @api.constrains('material_buy_price')
    def _check_material_buy_price(self):
        for i in self:
            if i.material_buy_price < 100:
                raise ValidationError("Pembelian Material tidak boleh dibawah 100")