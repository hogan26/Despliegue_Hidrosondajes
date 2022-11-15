# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class StockQuant(models.Model):
    _inherit = 'stock.quant'
    
    
    product_name = fields.Char(related="product_id.name",string="Nombre",store=True)