# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def action_warehouse_picking_stock(self):
        warehouse_stock_dest_location = self.env['stock.location'].search([('id','=',self.location_dest_id.id)])
        
        for detailed_operations_lines in self.move_line_ids_without_package:
            encontrado = False
            for cantidades in warehouse_stock_dest_location.quant_ids:
                if detailed_operations_lines.product_id.id == cantidades.product_id.id:                    
                    encontrado = True
                    detailed_operations_lines.write({'warehouse_picking_stock':cantidades.quantity})                    
            
            if encontrado == False:
                detailed_operations_lines.write({'warehouse_picking_stock':0})

class StockMoveLine(models.Model):
    _inherit='stock.move.line'
    
    warehouse_picking_stock = fields.Float(string="Stock B.S.")