# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Report(models.Model):
    _name = 'inventory.monitoring.report'
    _description = 'Inventory Report'

    name = fields.Char(string='Report Name', required=True)
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    notes = fields.Text(string='Notes')
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now, readonly=True)

    @api.model
    def generate_stock_report(self, date_from=None, date_to=None):
        date_from = date_from or fields.Date.today()
        date_to = date_to or date_from

        materials = self.env['inventory.monitoring.material'].search([])
        inbound_lines = self.env['inventory.monitoring.vendor.order.line'].search([
            ('order_id.order_date', '>=', date_from),
            ('order_id.order_date', '<=', date_to),
        ])
        vendor_orders = self.env['inventory.monitoring.vendor.order'].search([
            ('order_date', '>=', date_from),
            ('order_date', '<=', date_to),
        ])

        inbound_by_material = {}
        for line in inbound_lines:
            inbound_by_material.setdefault(line.material_id.id, 0.0)
            inbound_by_material[line.material_id.id] += line.qty_received

        report_lines = []
        report_lines.append(f"Report Period: {date_from} to {date_to}")
        report_lines.append("")
        report_lines.append("Materials Summary:")
        for material in materials:
            inbound_qty = inbound_by_material.get(material.id, 0.0)
            uom = material.uom or ''
            report_lines.append(
                f"- {material.name}: stock {material.current_stock} {uom}, "
                f"min {material.min_stock}, inbound {inbound_qty} {uom}"
            )

        report_lines.append("")
        report_lines.append("Vendor Orders:")
        if vendor_orders:
            for order in vendor_orders:
                report_lines.append(
                    f"- {order.name} | {order.vendor_name} | {order.order_date} | {order.state}"
                )
        else:
            report_lines.append("- No vendor orders recorded in this period.")

        notes = "\n".join(report_lines)
        report_name = f"Stock Report {date_from}"

        return self.create({
            'name': report_name,
            'date_from': date_from,
            'date_to': date_to,
            'notes': notes,
        })

    def fetch_data(self):
        self.ensure_one()
        return self.notes

    def export_report(self):
        return self.action_export_pdf()

    def action_export_pdf(self):
        self.ensure_one()
        return self.env.ref('inventory_monitoring.report_inventory_stock').report_action(self)
