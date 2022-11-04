# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    def action_confirm_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'alert_action_confirm_button',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'wizard.confirm',
            'context': {'parent_obj': self.name,
                        'default_abono_porcentaje':self.abono_porcentaje,
                        'default_abono_monto':self.abono_monto,
                        'default_descuento_iva':self.descuento_iva,
                        'default_descuento_neto_porcentaje':self.descuento_neto_porcentaje,
                        'default_descuento_neto_monto':self.descuento_neto_monto,
                        'default_num_cuotas':self.num_cuotas,
                        'default_payment_method':self.payment_method,
                        'default_observaciones':self.observaciones,
                       } 
        }
