# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    origin_sale_order = fields.Char(string='Presupuesto origen')
    #este campo tambien esta en el modelo sale.order.template, cuando se ejecute el evento onchage del field sale_order_template_id
    #este campo se debera setear en el valor que tiene esa plantilla, si se hace una ot sin usar un plantilla entonces el campo debe ser
    #requerido
    service = fields.Selection([('s1', 'S1'), ('s2', 'S2'), ('s3', 'S3'), ('s4', 'S4')], string='Servicio que aplica')

    def action_new_ot(self):
        if self.opportunity_id:
            return {
                'type':'ir.actions.act_window',
                'res_model':'sale.order',
                'res_id':False,
                'view_mode':'form',
                'context': {
                    'default_partner_id': self.partner_id.id,
                    'default_origin_sale_order': self.name
                }
            }
        
    def action_load_sale_order_items(self):
        origin_sale_order = self.env['sale.order'].search([('name','=',self.origin_sale_order)]) 
        # _logger.info('state = {}'.format(origin_sale_order.state))

        if origin_sale_order.state in ['sale']:
            product_ids_array = []
            for picking in origin_sale_order.picking_ids:
                if picking.servicio_reservado == self.service:                
                    for order_line in origin_sale_order.order_line:
                        if order_line.product_id.id and not (order_line.display_type):
                            for move_line in picking.move_ids_without_package:                        
                                if order_line.product_id.id == move_line.product_id.id:
                                    if order_line.product_id.id not in product_ids_array:
                                        self.write({
                                            'order_line': [(0, 0, {
                                                'product_id': order_line.product_id.id,
                                                'name': order_line.name,
                                                'product_uom_qty': order_line.product_uom_qty,
                                                'product_uom': order_line.product_uom.id,
                                                'price_unit': order_line.price_unit,
                                                'utilidad_porcentaje': order_line.utilidad_porcentaje,
                                                'precio_venta': order_line.precio_venta,
                                                'tax_id': order_line.tax_id,
                                                'last_update_price_date': order_line.last_update_price_date,
                                                'last_update_price_partner': order_line.last_update_price_partner,
                                                'last_update_type_selector': order_line.last_update_type_selector,
                                                'number_days_context': order_line.number_days_context,
                                                'discount': order_line.discount,
                                                'price_subtotal': order_line.price_subtotal,
                                                'margen_total': order_line.margen_total,
                                                'customer_lead': order_line.customer_lead,
                                            })]
                                        })
                                        product_ids_array.append(order_line.product_id.id)
                                    else:
                                        continue
        else: raise ValidationError("Debe confirmar la cotización antes de cargar los items a la OT")
            