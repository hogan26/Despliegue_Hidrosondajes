# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    
    def action_redirect_coti(self):
        if self.origin_sale_order:
            origin_sale_order = self.env['sale.order'].search([('name','=',self.origin_sale_order)])
            return {
                'type':'ir.actions.act_window',
                'res_model':'sale.order',
                'res_id':origin_sale_order.id,
                'view_mode':'form'                
            }