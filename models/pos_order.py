from odoo import models, api

class SaleDetailsReportInherit(models.AbstractModel):
    _inherit = 'report.point_of_sale.report_saledetails'  # <--- Ojo aquí

    @api.model
    def _get_report_values(self, docids, data=None):
        # Llamar método original
        res = super()._get_report_values(docids, data=data)

        # Recuperar fechas del wizard
        start_date = data.get('date_start')
        end_date = data.get('date_stop')

        # Buscar tus tickets
        ticket_logs = self.env['ticket.scanning.log'].search([
            ('status', '=', 'approved'), 
            ('consumption_date', '>=', start_date),
            ('consumption_date', '<=', end_date),
        ])

        # Agrupar
        product_data = {}
        for log in ticket_logs:
            pid = log.product_id.id
            if pid not in product_data:
                product_data[pid] = {
                    'name': log.product_id.name,
                    'qty': 0,
                }
            product_data[pid]['qty'] += 1

        # Agregarlo al diccionario para que el QWeb pueda usar 'ticket_scanning_data'
        res['ticket_scanning_data'] = list(product_data.values())
        return res
