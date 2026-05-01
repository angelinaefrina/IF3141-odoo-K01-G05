# -*- coding: utf-8 -*-
from odoo import fields, models


class Recipe(models.Model):
    _name = 'inventory.monitoring.recipe'
    _description = 'Recipe'

    name = fields.Char(string='Recipe Name', required=True)
    line_ids = fields.One2many(
        comodel_name='inventory.monitoring.recipe.line',
        inverse_name='recipe_id',
        string='Recipe Lines',
    )
