# -*- coding: utf-8 -*-
{
    'name': 'Arturo Cafe App',
    'version': '1.0.1',
    'summary': 'Monitor and manage Arturo Cafe kitchen inventory, recipes, and stock movements.',
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
    'category': 'Arturo Cafe',
    'author': 'IF3141-K01-G05',
    'depends': ['base', 'stock'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/material_views.xml',
        'views/vendor_order_views.xml',
        'views/recipe_views.xml',
        'views/stock_waste_views.xml',
        'views/pos_transaction_views.xml',
        'views/notification_views.xml',
        'views/report_views.xml',
        'views/report_templates.xml',
        'views/menu.xml',
        'data/notification_cron.xml',
        'data/report_cron.xml',
        'demo/demo_users.xml',
        'demo/demo_material.xml',
        'demo/demo_recipe.xml',
        'demo/demo_stock_waste.xml',
        'demo/demo_pos_transactions.xml',
        'demo/demo_notification.xml',
        'demo/demo_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'inventory_monitoring/static/src/css/dashboard.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
