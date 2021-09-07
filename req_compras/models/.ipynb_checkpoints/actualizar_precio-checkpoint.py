# -*- coding: utf-8 -*-

from odoo import models, fields


class ActualizarPrecio(models.Model):
    _inherit='purchase.order'
    
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            for line in order.order_line:
                for proveedor in line.product_id.seller_ids:
                    if proveedor.display_name in order.partner_id.display_name:
                        if proveedor.fijar_proveedor:
                            nuevo_precio = line.price_unit
                            line.product_id.product_tmpl_id.write({'list_price':nuevo_precio})
                            continue
                        else:
                            continue
                    else:
                        continue            

            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                or (order.company_id.po_double_validation == 'two_step'\
                and order.amount_total < self.env.company.currency_id._convert(
                order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
        return True
    