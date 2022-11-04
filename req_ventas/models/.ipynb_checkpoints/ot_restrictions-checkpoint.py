# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    
    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm()        
        if not(self.opportunity_id):
            if self.origin_sale_order:
                sale_order = self.env['sale.order'].search([('name','=',self.origin_sale_order)])
                if sale_order.opportunity_id:
                    if sale_order.state != 'sale':
                        raise ValidationError("la cotización vinculada a esta orden de trabajo no está confirmada por el área de ventas o está deshabilitada, favor dar aviso y vuelva a intentar una vez resuelto este problema")
                else:
                    raise ValidationError("la cotización vinculada a esta orden de trabajo no existe o no corresponde a un documento de cotización")
            else:
                raise ValidationError("Esta orden de trabajo no esta vinculada a ninguna cotización, favor completar el campo 'Presupuesto origen' y vuelva a confirmar esta orden de trabajo")
                
        return res