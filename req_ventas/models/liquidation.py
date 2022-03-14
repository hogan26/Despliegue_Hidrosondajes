# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    def action_liquidation(self):
        self.write({'state':'liquidar'})
    
    state = fields.Selection(selection_add=[('liquidar', 'Liquidado')])
    encabezado_liquidacion = fields.Html(string='Titulo principal')
    detalle_abonos_liquidacion = fields.Html(string='Detalle abonos')