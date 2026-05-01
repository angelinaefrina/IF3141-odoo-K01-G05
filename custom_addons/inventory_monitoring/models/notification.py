# -*- coding: utf-8 -*-
from odoo import fields, models


class Notification(models.Model):
    _name = 'inventory.monitoring.notification'
    _description = 'Stock Notification'

    name = fields.Char(string='Notification Title', required=True)
    material_id = fields.Many2one(
        comodel_name='inventory.monitoring.material',
        string='Material',
    )
    message = fields.Text(string='Message')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
