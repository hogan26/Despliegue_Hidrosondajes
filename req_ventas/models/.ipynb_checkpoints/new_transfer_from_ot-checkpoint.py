# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from itertools import groupby
from odoo.exceptions import UserError,ValidationError
from datetime import datetime , time


_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    ot_origen = fields.Char(string="O.T. origen")
    
    
    def new_transfer_from_ot(self):
        return {
                'type':'ir.actions.act_window',
                'res_model':'sale.order',
                'res_id':False,
                'view_mode':'form',
                'context': {
                    'default_partner_id': self.partner_id.id,
                    'default_num_telefono': self.num_telefono,
                    'default_direccion': self.direccion,                    
                    'default_calle': self.calle,
                    'default_x_equipo_asignado': self.x_equipo_asignado,
                    'default_origin_sale_order': self.origin_sale_order,
                    'default_service': self.service,
                    'default_ot_origen': self.name
                }
            }
#         raise ValidationError("dentro de la funcion")