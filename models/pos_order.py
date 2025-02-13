from odoo import models, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _get_report_data(self, data):
        res = super(PosOrder, self)._get_report_data(data)
        
        # Obtener fechas del informe
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        # ===== Datos de Tickets Consumidos =====
        ticket_logs = self.env['ticket.scanning.log'].search([
            ('status', '=', 'aprobado'),
            ('consumption_date', '>=', start_date),
            ('consumption_date', '<=', end_date)
        ])
        
        # Agrupar por producto
        product_data = {}
        for log in ticket_logs:
            product_id = log.product_id.id
            if product_id not in product_data:
                product_data[product_id] = {
                    'name': log.product_id.name,
                    'qty': 0
                }
            product_data[product_id]['qty'] += 1
        
        res['ticket_scanning_data'] = list(product_data.values())
        
        return res