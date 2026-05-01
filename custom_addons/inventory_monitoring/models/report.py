# -*- coding: utf-8 -*-
from odoo import fields, models


class Report(models.Model):
    _name = 'inventory.monitoring.report'
    _description = 'Inventory Report'

    name = fields.Char(string='Report Name', required=True)
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    notes = fields.Text(string='Notes')
