# -*- coding: utf-8 -*-
from odoo import fields, models


class RecipeLine(models.Model):
    _name = 'inventory.monitoring.recipe.line'
    _description = 'Recipe Line'

    recipe_id = fields.Many2one(
        comodel_name='inventory.monitoring.recipe',
        string='Recipe',
        required=True,
        ondelete='cascade',
    )
    material_id = fields.Many2one(
        comodel_name='inventory.monitoring.material',
        string='Material',
        required=True,
    )
    quantity = fields.Float(string='Quantity', default=1.0)
