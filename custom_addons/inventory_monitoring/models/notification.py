# -*- coding: utf-8 -*-
from odoo import api, fields, models


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
    is_read = fields.Boolean(string='Read', default=False)

    def mark_as_read(self):
        self.write({'is_read': True})
        return True

    @api.model
    def check_thresholds(self):
        materials = self.env['inventory.monitoring.material'].search([])
        low_materials = materials.filtered(lambda material: material.is_below_min_stock())
        return self._create_low_stock_notifications(low_materials)

    @api.model
    def trigger_alert(self, material):
        if not material:
            return False
        material.ensure_one()
        if not material.is_below_min_stock():
            return False
        return self._create_low_stock_notifications(material)

    @api.model
    def _create_low_stock_notifications(self, materials):
        notification_model = self.sudo()
        materials = materials.filtered(lambda material: material.min_stock > 0)
        if not materials:
            return False

        existing = notification_model.search([
            ('material_id', 'in', materials.ids),
            ('is_read', '=', False),
        ])
        existing_material_ids = set(existing.mapped('material_id').ids)
        for material in materials:
            if material.id in existing_material_ids:
                continue
            uom = material.uom or ''
            message = (
                f"Stock for {material.name} is at {material.current_stock} {uom} "
                f"(min {material.min_stock})."
            )
            notification_model.create({
                'name': f"Low Stock: {material.name}",
                'material_id': material.id,
                'message': message,
            })
        return True
