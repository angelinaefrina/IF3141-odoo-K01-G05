from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class StockWaste(models.Model):
    _name = 'inventory.monitoring.stock.waste'
    _description = 'Stock Waste Record'

    material_id = fields.Many2one('inventory.monitoring.material', string='Material', required=True)
    quantity = fields.Float(string='Waste Quantity', required=True, default=1.0)
    uom = fields.Char(related='material_id.uom', string='Unit of Measure', readonly=True)
    description = fields.Text(string='Description')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError("Gagal menyimpan! Kuantitas limbah harus lebih besar dari 0.")
            
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            material = self.env['inventory.monitoring.material'].browse(vals.get('material_id'))
            waste_qty = vals.get('quantity', 0)

            if waste_qty <= 0:
                raise UserError("Jumlah harus lebih besar dari 0!")
            if waste_qty > material.current_stock:
                raise UserError(
                    f"Pencatatan gagal! Anda mencoba mencatat limbah {material.name} sebanyak {waste_qty} {material.uom}, "
                    f"tetapi sisa stok saat ini hanya {material.current_stock} {material.uom}."
                )

        records = super(StockWaste, self).create(vals_list)
        for record in records:
            record.material_id.update_quantity(-record.quantity)

        return records
