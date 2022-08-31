# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    
    def redirect_coti_opportunity(self):
        if self.opportunity_id:            
            return {
                'type':'ir.actions.act_window',
                'res_model':'crm.lead',
                'res_id':self.opportunity_id.id,
                'view_mode':'form'
            }