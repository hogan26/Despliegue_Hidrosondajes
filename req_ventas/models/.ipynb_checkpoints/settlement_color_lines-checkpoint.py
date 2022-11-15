# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit='sale.order.line'
    
    
    sale_qty = fields.Integer(string="Cotizado")
    settlement_added_product = fields.Boolean(string="Adicional",default=False)
    settlement_line = fields.Boolean(string="Linea de liquidación",default=False)
    