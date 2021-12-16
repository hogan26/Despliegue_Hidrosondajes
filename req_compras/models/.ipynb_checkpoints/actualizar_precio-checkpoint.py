# -*- coding: utf-8 -*-

from odoo import api, models, fields


class ActualizarPrecio(models.Model):
    _inherit='purchase.order'
    
    @api.model
    def create(self, vals):
        company_id = vals.get('company_id',self.default_get(['company_id'])['company_id'])
        if vals.get('name', 'New') == 'New':
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self,fields.Datetime.to_datetime(vals['date_order']))
            vals['name'] = self.env['ir.sequence'].with_context(force_company=company_id).next_by_code('purchase.order',sequence_date=seq_date) or '/'

        res = super(ActualizarPrecio,self.with_context(company_id=company_id)).create(vals)

        for line in res.order_line:
            for proveedor in line.product_id.seller_ids:
                if proveedor.display_name in res.partner_id.display_name:
                    if proveedor.fijar_proveedor:
                        if line.product_uom.display_name == 'Tira 3mt' and line.display_name.find('V-WELL') == -1:
                            nuevo_precio = line.price_unit/3
                            line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                            line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': res.partner_id})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})
                            if res.state == 'sale':
                                line.product_id.product_tmpl_id.write({'last_update_type_selector':'compra'})
                            if res.state == 'draft':
                                line.product_id.product_tmpl_id.write({'last_update_type_selector':'cotizacion'})
                            proveedor.write({'price':line.price_unit})
                            continue
                        elif line.product_uom.display_name == 'Tira 6mt':
                            nuevo_precio = line.price_unit/6
                            line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                            line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': res.partner_id})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})
                            if res.state == 'sale':
                                line.product_id.product_tmpl_id.write({'last_update_type_selector':'compra'})
                            if res.state == 'draft':
                                line.product_id.product_tmpl_id.write({'last_update_type_selector':'cotizacion'})
                            proveedor.write({'price':line.price_unit})
                            continue
                        else:
                            nuevo_precio = line.price_unit
                            line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                            line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': res.partner_id})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})
                            if res.state == 'sale':
                                line.product_id.product_tmpl_id.write({'last_update_type_selector':'compra'})
                            if res.state == 'draft':
                                line.product_id.product_tmpl_id.write({'last_update_type_selector':'cotizacion'})
                            proveedor.write({'price':nuevo_precio})
                            continue
                    else:                        
                        continue
                else:                    
                    continue
        return res
    
    def write(self, vals):
        res = super(ActualizarPrecio, self).write(vals)
        if vals.get('date_planned'):
            self.order_line.filtered(lambda line: not line.display_type).date_planned = vals['date_planned']
            
        for line in self.order_line:
            for proveedor in line.product_id.seller_ids:
                if proveedor.display_name in self.partner_id.display_name:
                    if proveedor.fijar_proveedor:                        
                        if line.product_uom.display_name == 'Tira 3mt' and line.display_name.find('V-WELL') == -1:
                            nuevo_precio = line.price_unit/3
                            line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                            line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': self.partner_id})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})
                            if self.state == 'sale':
                                line.product_id.product_tmpl_id.write({'last_update_type_selector':'compra'})
                            if self.state == 'draft':
                                line.product_id.product_tmpl_id.write({'last_update_type_selector':'cotizacion'})
                            proveedor.write({'price':line.price_unit})
                            continue
                        elif line.product_uom.display_name == 'Tira 6mt':
                            nuevo_precio = line.price_unit/6
                            line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                            line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': self.partner_id})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})
                            if self.state == 'sale':
                                line.product_id.product_tmpl_id.write({'last_update_type_selector':'compra'})
                            if self.state == 'draft':
                                line.product_id.product_tmpl_id.write({'last_update_type_selector':'cotizacion'})
                            proveedor.write({'price':line.price_unit})
                            continue
                        else:
                            nuevo_precio = line.price_unit
                            line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                            line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': self.partner_id})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})
                            if self.state == 'sale':
                                line.product_id.product_tmpl_id.write({'last_update_type_selector':'compra'})
                            if self.state == 'draft':
                                line.product_id.product_tmpl_id.write({'last_update_type_selector':'cotizacion'})
                            proveedor.write({'price':nuevo_precio})
                            continue
                    else:                        
                        continue
                else:                    
                    continue
        return res
    
    def write(self, vals):
        res = super(ActualizarPrecio, self).write(vals)
        if vals.get('date_planned'):
            self.order_line.filtered(lambda line: not line.display_type).date_planned = vals['date_planned']
            
        for line in self.order_line:
            for proveedor in line.product_id.seller_ids:
                if proveedor.display_name in self.partner_id.display_name:
                    if proveedor.fijar_proveedor:                        
                        if line.product_uom.display_name == 'Tira 3mt' and line.display_name.find('V-WELL') == -1:
                            nuevo_precio = line.price_unit/3
                            line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                            line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': self.partner_id})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})
                            proveedor.write({'price':nuevo_precio})
                            continue
                        elif line.product_uom.display_name == 'Tira 6mt':
                            nuevo_precio = line.price_unit/6
                            line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                            line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': self.partner_id})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})
                            proveedor.write({'price':nuevo_precio})
                            continue
                        else:
                            nuevo_precio = line.price_unit
                            line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                            line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': self.partner_id})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})
                            proveedor.write({'price':nuevo_precio})
                            continue
                    else:                        
                        continue
                else:                    
                    continue
        return res
    
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            for line in order.order_line:
                for proveedor in line.product_id.seller_ids:
                    if proveedor.display_name in order.partner_id.display_name:
                        if proveedor.fijar_proveedor:
                           if line.product_uom.display_name == 'Tira 3mt' and line.display_name.find('V-WELL') == -1:
                            nuevo_precio = line.price_unit/3
                            line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                            line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': self.partner_id})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})
                            line.product_id.product_tmpl_id.write({'last_update_type_selector':'compra'})                            
                            proveedor.write({'price':line.price_unit})
                            continue
                        elif line.product_uom.display_name == 'Tira 6mt':
                            nuevo_precio = line.price_unit/6
                            line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                            line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': self.partner_id})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})
                            line.product_id.product_tmpl_id.write({'last_update_type_selector':'compra'})                            
                            proveedor.write({'price':line.price_unit})
                            continue
                        else:
                            nuevo_precio = line.price_unit
                            line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                            line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': self.partner_id})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})
                            line.product_id.product_tmpl_id.write({'last_update_type_selector':'compra'})                            
                            proveedor.write({'price':nuevo_precio})
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
    
class DescuentoLineaCompra(models.Model):
    _inherit = 'purchase.order.line'

    @api.depends('product_qty', 'price_unit', 'taxes_id','descuento_porcentaje', 'descuento_monto')
    def _compute_amount(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_id.compute_all(
                vals['price_unit'],
                vals['currency_id'],
                vals['product_qty'],
                vals['product'],
                vals['partner'])

            if line.descuento_porcentaje:
                line.update({
                    'price_tax': sum(
                        t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded']-(taxes['total_excluded']*(line.descuento_porcentaje/100)),
                })
            elif line.descuento_monto:
                line.update({
                    'price_tax': sum(
                        t.get('amount', 0.0) for t in
                        taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'] - line.descuento_monto,
                })
            else:
                line.update({
                    'price_tax': sum(t.get('amount', 0.0) for t in
                                     taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                })

    descuento_porcentaje = fields.Float(string="Descuento(%)", default=0.0)
    descuento_monto = fields.Float(string="Descuento($)", default=0.0)
    