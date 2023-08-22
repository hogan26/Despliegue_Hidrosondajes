# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api
from odoo.tools import float_round
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit='sale.order'    
    
    
    total_tax_discount = fields.Integer(string="Descuento IVA (%)",default=0)
    total_tax_amount_discount = fields.Integer(string="Descuento IVA ($)",default=0)
    untaxed_percentage_discount = fields.Integer(string="Descuento neto (%).",default=0)
    untaxed_amount_discount = fields.Integer(string="Descuento neto ($).",default=0)
    tax_client = fields.Float(string="Impuestos")
    amount_total_client = fields.Float(string="Total.")
    code = fields.Float(string="Código") 


    @api.onchange('total_tax_discount','total_tax_amount_discount')
    def onchange_tax_discount(self):
        _logger.info('dentro de onchange_tax_discount')
        # for order in self:
        amount_untaxed = amount_tax = tax_client = 0.0            
        for line in self.order_line:
            amount_untaxed += line.price_subtotal               
            
        if self.total_tax_discount:
            code_value = 0
            amount_tax = round((amount_untaxed * 19)/100)
            discount_amount = round(amount_tax - (amount_tax * (self.total_tax_discount/100)))
            code_value = amount_untaxed + discount_amount
            _logger.info('descuento porcentaje = {}, order_id = {}'.format(code_value,self.name))
            
        if self.total_tax_amount_discount:
            code_value = 0
            amount_tax = round((amount_untaxed * 19)/100)
            if self.total_tax_amount_discount>amount_tax:
                raise ValidationError("No puedo aplicar un descuento mayor al monto total")
            else: 
                discount_amount = amount_tax - self.total_tax_amount_discount
                code_value = amount_untaxed + discount_amount
                _logger.info('descuento monto fijo = {}, order_id = {}'.format(code_value,self.name))
            
        if (self.total_tax_discount !=0 and self.untaxed_percentage_discount==0) or (self.total_tax_amount_discount !=0 and self.untaxed_percentage_discount==0):
            # sale_order_id = self.env['sale.order'].search([('name','=',order.name)])
            self.update({'code': code_value})            
        else:
            # sale_order_id = self.env['sale.order'].search([('name','=',order.name)])
            self.update({'code': 0})

    @api.onchange('untaxed_amount_discount')
    def _onchange_amount_discount(self):
        for order in self:
            if order.untaxed_amount_discount < 0:
                order.untaxed_amount_discount = 0

            total_amount = sum(line.price_subtotal for line in order.order_line)
            order.amount_total = total_amount - order.untaxed_amount_discount + int(order.amount_tax)


    """ version anterior del código

# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    
    @api.depends('order_line.price_total','total_tax_discount','total_tax_amount_discount','untaxed_percentage_discount',         'untaxed_amount_discount')
    def _amount_all(self):        
        for order in self:
            amount_untaxed = amount_tax = tax_client = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                tax_client += line.price_tax
                
            if self.untaxed_percentage_discount:
                #total_tax_discount = untaxed_percentage_discount
                order.update({
                    'total_tax_discount': self.untaxed_percentage_discount,                    
                })
                amount_untaxed = amount_untaxed - (amount_untaxed * (self.untaxed_percentage_discount/100))
                
            if self.total_tax_discount:
                amount_tax = amount_tax - (amount_tax * (self.total_tax_discount/100))
                
            if self.total_tax_amount_discount:
                amount_tax = amount_tax - self.total_tax_amount_discount
                
            if self.untaxed_amount_discount:
                amount_untaxed = amount_untaxed - self.untaxed_amount_discount
                amount_tax = amount_untaxed * 0.19                
                
            if (self.total_tax_discount !=0 and self.untaxed_percentage_discount==0) or (self.total_tax_amount_discount !=0 and self.untaxed_percentage_discount==0):       
                order.update({
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_untaxed + amount_tax,
                    'tax_client': tax_client,
                    'amount_total_client': amount_untaxed + tax_client,
                    'code': amount_untaxed + amount_tax,                    
                })            
            else:
                order.update({
                    'amount_untaxed': amount_untaxed,
                    'amount_tax': amount_tax,
                    'amount_total': amount_untaxed + amount_tax, 
                    'tax_client': amount_tax,
                    'amount_total_client': amount_untaxed + amount_tax,
                    'code': 0,                    
                })
    
    total_tax_discount = fields.Integer(string="Descuento IVA (%)",default=0)
    total_tax_amount_discount = fields.Integer(string="Descuento IVA ($)",default=0)
    untaxed_percentage_discount = fields.Integer(string="Descuento neto (%).",default=0)
    untaxed_amount_discount = fields.Integer(string="Descuento neto ($).",default=0)
    tax_client = fields.Float(string="Impuestos")
    amount_total_client = fields.Float(string="Total.")
    code = fields.Float(string="Código")
    """
    
    