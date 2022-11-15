# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from itertools import groupby
from odoo.exceptions import UserError,ValidationError
from datetime import datetime , time


_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking' 
    
    
    def autocomplete_from_ot_code(self):
        if self.ot_origen:
            ot_document = self.env['sale.order'].search([('name','=',self.ot_origen),('opportunity_id','=',False)])
            if ot_document:
                self.update({
                    'origin':ot_document.origin_sale_order,
                    'partner_id':ot_document.partner_id,
                    'servicio_reservado':ot_document.service
                            })
                if self.picking_type_id.code == 'internal' and ot_document.x_equipo_asignado:
                    location_dest_id = self.env['stock.location'].search([('complete_name','=',ot_document.x_equipo_asignado+'/Stock')])
                    self.update({
                    'location_dest_id':location_dest_id.id                   
                            })
            else:            
                raise ValidationError("No se ha encontrado el documento de orden de trabajo, ingrese un valor válido")
        else:
            raise ValidationError("Ingrese un Codigo de orden de trabajo")