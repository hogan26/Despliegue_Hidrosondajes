# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def action_warehouse_picking_stock(self):
        # _logger.info('location_id = {}'.format(self.location_id.name))
        warehouse_stock_location = self.env['stock.location'].search([('id','=',self.location_id.id)])
        
        for detailed_operations_lines in self.move_line_ids_without_package:
            encontrado = False
            for cantidades in warehouse_stock_location.quant_ids:
                if detailed_operations_lines.product_id.id == cantidades.product_id.id:                    
                    encontrado = True
                    detailed_operations_lines.write({'warehouse_picking_stock':cantidades.quantity})                    
            
            if encontrado == False:
                detailed_operations_lines.write({'warehouse_picking_stock':0})

class StockMoveLine(models.Model):
    _inherit='stock.move.line'
    
    warehouse_picking_stock = fields.Float(string="Stock B.S.")