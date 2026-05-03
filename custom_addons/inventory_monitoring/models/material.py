# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Material(models.Model):
    _name = 'inventory.monitoring.material'
    _description = 'Inventory Material'

    name = fields.Char(string='Material Name', required=True)
    uom = fields.Char(string='Unit of Measure')
    current_stock = fields.Float(string='Current Stock', default=0.0)
    min_stock = fields.Float(string='Minimum Stock', default=0.0)

    def update_quantity(self, value):
        for rec in self:
            rec.current_stock += value
        return True

    def is_below_min_stock(self):
        self.ensure_one()
        return self.min_stock > 0 and self.current_stock <= self.min_stock

    def _trigger_stock_alerts(self):
        low_materials = self.filtered(lambda material: material.is_below_min_stock())
        if low_materials:
            self.env['inventory.monitoring.notification'].sudo()._create_low_stock_notifications(low_materials)

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._trigger_stock_alerts()
        return record

    def write(self, vals):
        result = super().write(vals)
        if {'current_stock', 'min_stock'} & set(vals):
            self._trigger_stock_alerts()
        return result
