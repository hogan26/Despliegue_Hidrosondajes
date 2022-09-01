# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
    
    @api.onchange('product_id')
    def onchange_set_tax(self):
        purchase_tax = self.env['account.tax'].search([('name','=','IVA 19% Compra')])
        for line in self:
            if line.tax_seted != 1:
                line.update({'taxes_id':purchase_tax,'tax_seted':1})
    
    tax_seted = fields.Integer(string="impuesto seteado automaticamente")