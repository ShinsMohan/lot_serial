from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

class StockLot(models.Model):
    _inherit = 'stock.lot'

    vendor = fields.Many2one('res.partner', string='Vendor')
    supplier_batch_number = fields.Char(string='Supplier Batch Number')
    expiration_date = fields.Date(string='Expiration Date')
    austerilan_percentage = fields.Float(string='Austerilan Percentage')    

    @api.model
    def create(self, vals):
        self._check_expiration_date(vals.get('expiration_date'))
        if 'name' not in vals:
            vals['name'] = self._generate_name(vals)
        return super(StockLot, self).create(vals)

    def _generate_name(self, vals, record=None):
        vendor = self.env['res.partner'].browse(vals.get('vendor')) if not record else record.vendor
        product = self.env['product.product'].search([('id', '=', record.product_id.id)]) if record else self.env['product.product'].browse(vals.get('product_id'))
        supplier_batch_number = vals.get('supplier_batch_number', '') if not record else record.supplier_batch_number
        supplier_code = vendor.supplier_code if vendor else ''
        default_code = product.default_code if product else ''
        return f"{supplier_code} - {default_code} - {supplier_batch_number}"

    def _check_expiration_date(self, expiration_date):
        if expiration_date:
            expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d %H:%M:%S').date()
            if expiration_date < datetime.now().date() + timedelta(weeks=4):
                raise exceptions.ValidationError("The expiration date must be at least 4 weeks from today.")

    @api.onchange('vendor', 'product_id', 'supplier_batch_number')
    def _onchange_related_fields(self):
        if self.vendor or self.product_id or self.supplier_batch_number:
            self.name = self._generate_name({}, self)