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
                elif self.picking_type_id.code == 'outgoing' and ot_document.x_equipo_asignado:                    
                    warehouse = self.env['stock.warehouse'].search([('lot_stock_id','=',ot_document.x_equipo_asignado+'/Stock')])
                    picking_type_id = self.env['stock.picking.type'].search([('warehouse_id','=',warehouse.id),('sequence_code','=','OUT')])
                    location_id = self.env['stock.location'].search([('complete_name','=',ot_document.x_equipo_asignado+'/Stock')])
                    self.update({
                    'location_id':location_id.id,
                    'picking_type_id':picking_type_id.id    
                            })
            else:            
                raise ValidationError("No se ha encontrado el documento de orden de trabajo, ingrese un valor válido")
        else:
            raise ValidationError("Ingrese un Codigo de orden de trabajo")

        if self.location_dest_id:
            warehouse_stock_location = self.env['stock.location'].search([('id','=',self.location_dest_id.id)])
            
            for detailed_operations_lines in self.move_line_ids_without_package:                                                
                detailed_operations_lines.write({'location_dest_id':warehouse_stock_location.id}) 