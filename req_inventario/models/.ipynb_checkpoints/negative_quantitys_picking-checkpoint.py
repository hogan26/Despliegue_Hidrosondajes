# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    
    @api.constrains('qty_done')
    def _check_positive_qty_done(self):
        negative_quantity = False
        negative_quantity_names = []
        for ml in self:
            if ml.qty_done < 0:
                negative_quantity_names.append(ml.product_id.name)
                negative_quantity = True
        
        if negative_quantity:
            product_names = '- '
            for product_name in negative_quantity_names:
                product_names = product_names + product_name + ' - '
            
            raise ValidationError(_('No se pueden cargar cantidades negativas, los siguientes productos presentan cantidades negativas en la ubicación de origen : %s ') % (product_names))