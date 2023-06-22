# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
import logging
_logger = logging.getLogger(__name__)

class MargenTotal(models.Model):
    _inherit='sale.order'
    
    @api.depends('order_line.margen_total')
    def suma_margen(self):
        for order in self:
            suma_margen=0
            for line in order.order_line:
                suma_margen += line.margen_total
            order.update({'suma_margen':suma_margen})
            
    suma_margen = fields.Monetary(string='Margen Utilidad',readonly=True,compute=suma_margen)

    @api.depends('order_line.tax_id', 'order_line.price_unit','order_line.precio_venta','order_line.utilidad_porcentaje', 'amount_total', 'amount_untaxed')
    def _compute_tax_totals_json(self):
        # _logger.info('dentro de _compute_tax_totals_json')
        def compute_taxes(order_line):
            price = order_line.precio_venta * (1 - (order_line.discount or 0.0) / 100.0)
            order = order_line.order_id
            return order_line.tax_id._origin.compute_all(price, order.currency_id, order_line.product_uom_qty, product=order_line.product_id, partner=order.partner_shipping_id)

        account_move = self.env['account.move']
        for order in self:
            tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line, compute_taxes)
            tax_totals = account_move._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total, order.amount_untaxed, order.currency_id)
            order.tax_totals_json = json.dumps(tax_totals)

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
            price = (line.price_unit + line.utilidad_unitaria) * (1- (line.discount or 0.0)/100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])                   
    
                
    utilidad_porcentaje = fields.Float(string="Utilidad (%)",default=45)
    utilidad_unitaria = fields.Monetary(string="U. unitaria ($)",
                                       compute=utilidad_unitaria)
    precio_venta = fields.Monetary(string="Precio de venta",
                                  compute=precio_venta)
    monto_final = fields.Monetary(string="Monto final", compute=monto_final)
    margen_total = fields.Monetary(string="Margen", compute=margen_total)
    
class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    service = fields.Selection([('s1','S1'),('s2','S2'),('s3','S3'),('s4','S4')],string='Servicio que aplica')        

