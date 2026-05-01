# -*- coding: utf-8 -*-
from odoo import fields, models


class Material(models.Model):
    _name = 'inventory.monitoring.material'
    _description = 'Inventory Material'

    name = fields.Char(string='Material Name', required=True)
    uom = fields.Char(string='Unit of Measure')
    current_stock = fields.Float(string='Current Stock', default=0.0)
    min_stock = fields.Float(string='Minimum Stock', default=0.0)
