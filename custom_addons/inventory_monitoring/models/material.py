# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Material(models.Model):
    _name = 'inventory.monitoring.material'
    _description = 'Inventory Material'
    _order = 'stock_priority_rank asc, reorder_qty desc, name asc'

    name = fields.Char(string='Material Name', required=True)
    uom = fields.Char(string='Unit of Measure')
    qty_on_hand = fields.Float(string='Current Stock', default=0.0)
    min_stock = fields.Float(string='Minimum Stock', default=0.0)
    stock_gap = fields.Float(
        string='Stock Gap',
        compute='_compute_stock_metrics',
        store=True,
    )
    reorder_qty = fields.Float(
        string='Suggested Reorder',
        compute='_compute_stock_metrics',
        store=True,
    )
    stock_status = fields.Selection(
        selection=[
            ('low', 'Low'),
            ('safe', 'Safe'),
        ],
        string='Stock Status',
        compute='_compute_stock_metrics',
        store=True,
    )
    stock_coverage_pct = fields.Float(
        string='Stock Coverage (%)',
        compute='_compute_stock_metrics',
        store=True,
    )
    stock_priority = fields.Selection(
        selection=[
            ('critical', 'Critical'),
            ('warning', 'Warning'),
            ('safe', 'Safe'),
        ],
        string='Stock Priority',
        compute='_compute_stock_metrics',
        store=True,
    )
    stock_priority_rank = fields.Integer(
        string='Stock Priority Rank',
        compute='_compute_stock_metrics',
        store=True,
    )

    @api.depends('current_stock', 'min_stock')
    def _compute_stock_metrics(self):
        for rec in self:
            rec.stock_gap = rec.current_stock - rec.min_stock
            rec.reorder_qty = max(rec.min_stock - rec.current_stock, 0.0)
            rec.stock_status = 'low' if rec.current_stock < rec.min_stock else 'safe'
            if rec.min_stock > 0:
                rec.stock_coverage_pct = (rec.current_stock / rec.min_stock) * 100.0
            else:
                rec.stock_coverage_pct = 100.0

            if rec.stock_coverage_pct < 60.0:
                rec.stock_priority = 'critical'
                rec.stock_priority_rank = 1
            elif rec.stock_coverage_pct < 100.0:
                rec.stock_priority = 'warning'
                rec.stock_priority_rank = 2
            else:
                rec.stock_priority = 'safe'
                rec.stock_priority_rank = 3

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
