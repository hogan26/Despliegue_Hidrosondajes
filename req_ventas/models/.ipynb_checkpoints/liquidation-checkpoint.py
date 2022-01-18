# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    def action_liquidation(self):
        self.write({'state':'liquidar'})
    
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('liquidar', 'Liquidado'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    encabezado_liquidacion = fields.Html(string='Titulo principal')
    detalle_abonos_liquidacion = fields.Html(string='Detalle abonos')