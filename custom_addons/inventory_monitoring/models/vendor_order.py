# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class VendorOrder(models.Model):
    _name = 'inventory.monitoring.vendor.order'
    _description = 'Vendor Stock Order'
    _order = 'order_date desc, id desc'

    name = fields.Char(
        string='Order Reference',
        required=True,
        copy=False,
        readonly=True,
        default='New',
    )
    vendor_name = fields.Char(string='Vendor Name', required=True)
    order_date = fields.Date(string='Order Date', required=True, default=fields.Date.today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)

    order_line_ids = fields.One2many(
        'inventory.monitoring.vendor.order.line',
        'order_id',
        string='Order Lines',
    )

    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('inventory.monitoring.vendor.order') or 'New'
        return super().create(vals)

    def action_confirm(self):
        for rec in self:
            if not rec.order_line_ids:
                raise ValidationError('Tambahkan minimal satu item sebelum konfirmasi.')
            rec.state = 'confirmed'

    def action_receive(self):
        for rec in self:
            for line in rec.order_line_ids:
                line.material_id.qty_on_hand += line.qty_received
            rec.state = 'received'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'draft'


class VendorOrderLine(models.Model):
    _name = 'inventory.monitoring.vendor.order.line'
    _description = 'Vendor Order Line'

    order_id = fields.Many2one(
        'inventory.monitoring.vendor.order',
        string='Order',
        required=True,
        ondelete='cascade',
    )
    material_id = fields.Many2one(
        'inventory.monitoring.material',
        string='Material',
        required=True,
    )
    uom = fields.Char(
        string='Unit',
        related='material_id.uom',
        readonly=True,
        store=True,
    )
    qty_ordered = fields.Float(string='Qty Ordered', required=True, default=1.0)
    qty_received = fields.Float(string='Qty Received', default=0.0)

    @api.onchange('qty_ordered')
    def _onchange_qty_ordered(self):
        if self.qty_ordered < 0:
            raise ValidationError('Jumlah tidak boleh negatif.')
