# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    @api.depends('order_line.price_total','total_tax_discount')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax - (amount_tax*(order.total_tax_discount/100)),
                'amount_total': amount_untaxed + (amount_tax - (amount_tax*(order.total_tax_discount/100))),
            })
    
    total_tax_discount = fields.Integer(string="Descuento (%)",default=0)
    
    