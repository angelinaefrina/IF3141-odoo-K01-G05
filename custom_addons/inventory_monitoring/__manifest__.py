# -*- coding: utf-8 -*-
{
    'name': 'Inventory Monitoring',
    'version': '1.0.0',
    'summary': 'Monitor and manage kitchen inventory, recipes, and stock movements.',
    'description': """
        Inventory Monitoring Module
        ===========================
        Custom module for managing kitchen inventory with role-based access control.

        Roles:
        - Kitchen Team : Manage stocks, handle inbound & waste
        - Head Chef    : Manage recipes, set minimum stock levels
        - Supervisor   : Receive and view notifications
        - Manager      : View inventory reports
    """,
    'category': 'Inventory Monitoring',
    'author': 'IF3141-K01-G05',
    'depends': ['base', 'stock'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/material_views.xml',
        'views/vendor_order_views.xml',
        'views/recipe_views.xml',
        'views/menu.xml',
        'demo/demo_users.xml',
        'demo/demo_material.xml',
        'demo/demo_recipe.xml',
        'demo/demo_notification.xml',
        'demo/demo_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
