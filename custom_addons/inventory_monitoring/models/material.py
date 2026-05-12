# -*- coding: utf-8 -*-
from odoo import fields, models


class Material(models.Model):
    _name = 'inventory.monitoring.material'
    _description = 'Inventory Material'

    name = fields.Char(string='Material Name', required=True)
    uom = fields.Char(string='Unit of Measure')
    qty_on_hand = fields.Float(string='Current Stock', default=0.0)
    min_stock = fields.Float(string='Minimum Stock', default=0.0)

    def update_quantity(self, value):
        # update (add or substract) stock quantity
        for record in self:
            record.qty_on_hand += value
            if record.qty_on_hand <= record.min_stock:
                inventory_monitoring_notification = self.env['inventory.monitoring.notification']
                inventory_monitoring_notification.create({
                    'name': f'Stok Menipis : {record.name}',
                    'material_id': record.id,
                    'message': f'Stok {record.name} sudah mencapai batas minimum, mohon segera restock! Stok Sekarang: {record.qty_on_hand} {record.uom}.',
                })
