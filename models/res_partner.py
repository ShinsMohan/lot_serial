from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    supplier_code = fields.Char(string='Supplier Code')