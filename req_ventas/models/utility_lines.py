# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MargenTotal(models.Model):
    _inherit='sale.order'
    
    @api.depends('order_line.margen_total')
    def suma_margen(self):
        for order in self:
            suma_margen=0
            for line in order.order_line:
                suma_margen += line.margen_total
            order.update({'suma_margen':suma_margen})
            
    suma_margen = fields.Monetary(
        string='Margen total', 
        readonly=True, 
        compute=suma_margen)

class SaleOrderLine(models.Model):
    _inherit='sale.order.line'
    
    def utilidad_unitaria(self):
        for line in self:
            line.utilidad_unitaria = line.price_unit * (line.utilidad_porcentaje/100.0)
    
    def precio_venta(self):
        for line in self:
            line.precio_venta = line.price_unit + line.utilidad_unitaria
            
    def monto_final(self):
        for line in self:
            line.monto_final = line.precio_venta * line.product_uom_qty
            
    def margen_total(self):
        for line in self:
            line.margen_total = line.utilidad_unitaria * line.product_uom_qty
            
    @api.depends('product_uom_qty','discount','price_unit','tax_id',
                'utilidad_unitaria','precio_venta','monto_final',
                'utilidad_porcentaje')
    def _compute_amount(self):
        for line in self:
            price = (line.price_unit + line.utilidad_unitaria) * (
            1- (line.discount or 0.0)/100.0)
            taxes = line.tax_id.compute_all(price,line.order_id.currency_id,
                                   line.product_uom_qty,
                                   product=line.product_id,
                                   partner=line.order_id.partner_shipping_id)
            line.update({
                'price.tax':sum(
                t.get('amount',0.0) for t in taxes.get('taxes',[])),
                'price_total':taxes['total_included'],
                'price_subtotal':taxes['total_excluded'],
            })
            if self.env.context.get('import_file',False) and not 
            self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'],
                                            [line.tax_id.id])
    
    utilidad_porcentaje = fields.Float(string="Utilidad (%)", default=45)
    utilidad_unitaria = fields.Monetary(string="U. unitaria ($)",
                                       compute=utilidad_unitaria)
    precio_venta = fields.Monetary(string="Precio de venta",
                                  compute=precio_venta)
    monto_final = fields.Monetary(string="Monto final", compute=monto_final)
    margen_total = fields.Montery(string="Margen", compute=margen_total)
            
        

