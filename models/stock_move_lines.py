from odoo import models, fields, api

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    lot_ids = fields.Many2many("stock.lot", compute='_compute_lot_ids')

    @api.depends('move_id', 'move_id.picking_id', 'move_id.product_id')
    def _compute_lot_ids(self):
        for same in self:
            if same.move_id.picking_id.partner_id and same.move_id.product_id:
                supplier_code = same.move_id.picking_id.partner_id.supplier_code
                internal_ref = same.move_id.product_id.default_code
                lot_ids = self.env['stock.lot'].search([
                    ('vendor.supplier_code', '=', supplier_code),
                    ('product_id.default_code', '=', internal_ref)
                ])
                same.lot_ids = lot_ids