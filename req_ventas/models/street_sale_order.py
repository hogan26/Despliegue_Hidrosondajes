# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    @api.model
    def default_get(self,fields_list):
        res = super(SaleOrder,self).default_get(fields_list)
        # si genera problemas de visualizacion en las ordenes de trabajo o cotizaciones, darle un valor por defecto si no se ingresaron los datos de street
        # y ciudad, por ejemplo '-', al hacer esto hay que modificar las condicionales de las vistas y los informes qweb
        self.update({
            'city_sale_order':self.partner_id.city,
            'street_sale_order':self.partner_id.street,                
        })
            
        return res
    
    city_sale_order = fields.Char(string="Ciudad Cotización")
    street_sale_order = fields.Char(string="Dirección Cotización")
    
    
    