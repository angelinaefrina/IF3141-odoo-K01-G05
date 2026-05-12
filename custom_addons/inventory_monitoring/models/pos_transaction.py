from odoo import models, fields, api

class PosTransaction(models.Model):
    _name = 'inventory.monitoring.pos.transaction'
    _description = 'POS Sales Transaction'

    recipe_id = fields.Many2one('inventory.monitoring.recipe', string='Menu Sold', required=True)
    quantity_sold = fields.Integer(string='Quantity Sold', required=True, default=1)
    date = fields.Datetime(string='Transaction Date', default=fields.Datetime.now)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(PosTransaction, self).create(vals_list)
        for record in records:
            if record.recipe_id:
                for line in record.recipe_id.line_ids:
                    total_material_needed = line.quantity * record.quantity_sold
                    line.material_id.update_quantity(-total_material_needed)

        return records