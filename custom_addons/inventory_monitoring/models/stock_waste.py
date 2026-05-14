from odoo import models, fields, api

class StockWaste(models.Model):
    _name = 'inventory.monitoring.stock.waste'
    _description = 'Stock Waste Record'

    material_id = fields.Many2one('inventory.monitoring.material', string='Material', required=True)
    quantity = fields.Float(string='Waste Quantity', required=True)
    uom = fields.Char(related='material_id.uom', string='Unit of Measure', readonly=True)
    description = fields.Text(string='Description')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(StockWaste, self).create(vals_list)
        for record in records:
            record.material_id.update_quantity(-record.quantity)

        return records
