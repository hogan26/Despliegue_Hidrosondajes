# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit='purchase.order'

    purchase_order_type_entry = fields.Selection([('factura','Ingreso de factura'),('cotizacion','Cotización de ventas')],string='Tipo de entrada')
    
    def button_confirm_date_validation(self):            
        datetime_order = fields.Datetime.to_string(self.date_order)
        date_order_datetime = fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(datetime_order)))[:10]
        date_order = fields.Date.from_string(date_order_datetime)
        return {
            'type': 'ir.actions.act_window',
            'name': 'purchase_date_order_verification_confirm_button',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'wizard.date.purchase',
            'context': {
                        'parent_obj': self.name,
                        'default_date_order':self.date_order,
                       } 
        }
        