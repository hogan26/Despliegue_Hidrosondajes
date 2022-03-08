# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProducTemplate(models.Model):
    _inherit='product.template'
    
    
    @api.onchange('composite_products_lines_ids')
    def onchange_composite_products_lines_ids(self):
        amount_total = 0
        total_margen = 0
        for lines in self.composite_products_lines_ids:
            amount_total = amount_total + lines.amount_total_line
            total_margen = total_margen + lines.margen
            
        self.update({'amount_total':amount_total})        
        self.update({'total_margen':total_margen})
        #finalmente se actualiza el precio del producto que sera mostrado al integrarlo en una cotizacion
        self.update({'list_price':amount_total})
        self.update({'standard_price':amount_total})
            
    
    composite_product_check = fields.Boolean(string="Producto compuesto")
    composite_products_lines_ids = fields.One2many(
        comodel_name="composite.product",
        inverse_name="composite_product_id", string="Composición")
    amount_total = fields.Integer(string="Total = ",readonly=True)
    total_margen = fields.Integer(string="Margen total = ",readonly=True)
    
    
class MatrizProductoCompuesto(models.Model):    
    _name = "composite.product"
    _description = 'coronas para matriz de servicio de perforacion'    
    
    @api.onchange('product','cost_price','quantity','utility')
    def onchange_product(self):
        data = self.env['product.template'].search([('id','=',self.product.id)])
        
        sale_price = self.cost_price + (data.list_price*(self.utility/100))
        margen = (sale_price - self.cost_price)*self.quantity
        amount_total_line = (self.cost_price + (data.list_price*(self.utility/100))) * self.quantity
        
        self.update({'cost_price':data.list_price})        
        self.update({'utility':self.utility})
        self.update({'uom':data.uom_id.id})
        self.update({'sale_price':sale_price})
        self.update({'amount_total_line':amount_total_line})
        self.update({'margen':margen})
    
    composite_product_id = fields.Many2one(comodel_name="product.template")
    product = fields.Many2one('product.template',string='Producto',store=True)
    cost_price = fields.Integer(string="Precio Costo")
    quantity = fields.Integer(string="Cantidad")
    utility = fields.Integer(string="Utilidad (%)",default=45)
    uom = fields.Many2one('uom.uom',string="Un",readonly=True)
    sale_price = fields.Integer(string="Precio Venta",readonly=True)
    amount_total_line = fields.Integer(string="Total",readonly=True)
    margen = fields.Integer(string="margen",readonly=True)
    
    
    