# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    origin_sale_order = fields.Char(string='Presupuesto origen')
    #este campo tambien esta en el modelo sale.order.template, cuando se ejecute el evento onchage del field sale_order_template_id
    #este campo se debera setear en el valor que tiene esa plantilla, si se hace una ot sin usar un plantilla entonces el campo debe ser
    #requerido
    service = fields.Selection([('s1', 'S1'), ('s2', 'S2'), ('s3', 'S3'), ('s4', 'S4')], string='Servicio que aplica',required=True)

    def action_new_ot(self):
        if self.opportunity_id:
            return {
                'type':'ir.actions.act_window',
                'res_model':'sale.order',
                'res_id':False,
                'view_mode':'form',
                'context': {
                    'default_partner_id': self.partner_id.id,
                    'default_origin_sale_order': self.name
                }
            }

