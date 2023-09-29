# -*- coding: utf-8 -*-

from odoo import api, models, fields
import logging
_logger = logging.getLogger(__name__)


class ActualizarPrecio(models.Model):
    _inherit='purchase.order'

    @api.model
    def create(self, vals):
        company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
        self_comp = self.with_company(company_id)
        if vals.get('name', 'New') == 'New':
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            vals['name'] = self_comp.env['ir.sequence'].next_by_code('purchase.order', sequence_date=seq_date) or '/'
        vals, partner_vals = self._write_partner_values(vals)
        res = super(ActualizarPrecio, self_comp).create(vals)        
        if partner_vals:
            res.sudo().write(partner_vals)  # Because the purchase user doesn't have write on `res.partner`    
    
        for line in res.order_line:
            for proveedor in line.product_id.seller_ids:
                if proveedor.display_name in res.partner_id.display_name:
                    if proveedor.fijar_proveedor:
                        _logger.info('line.product_uom.display_name = {}, line.display_name = {}, line.descuento_porcentaje'.format(line.product_uom.display_name,line.display_name,line.descuento_porcentaje))
                        if line.product_uom.display_name == 'Tira 3mt' and line.display_name.find('V-WELL') == -1:
                            if line.descuento_porcentaje:
                                nuevo_precio = (line.price_unit - ((line.price_unit*line.descuento_porcentaje)/100))/3
                                _logger.info('descuento_porcentaje = {}'.format(line.descuento_porcentaje))
                            elif line.descuento_monto: 
                                nuevo_precio = (line.price_unit - line.descuento_monto)/3
                                _logger.info('descuento_monto = {}'.format(line.descuento_monto))
                            else:
                                nuevo_precio = line.price_unit/3
                                _logger.info('no se detecto descuento')
                        elif line.product_uom.display_name == 'Tira 6mt':
                            if line.descuento_porcentaje: 
                                nuevo_precio = (line.price_unit - ((line.price_unit*line.descuento_porcentaje)/100))/6
                                _logger.info('descuento_porcentaje = {}'.format(line.descuento_porcentaje))
                            elif line.descuento_monto: 
                                nuevo_precio = (line.price_unit - line.descuento_monto)/6
                                _logger.info('descuento_monto = {}'.format(line.descuento_monto))
                            else:
                                nuevo_precio = line.price_unit/6
                                _logger.info('no se detecto descuento')
                        elif line.product_uom.display_name == 'Balde 20' or line.product_uom.display_name == 'Bidón 20':
                            if line.descuento_porcentaje: 
                                nuevo_precio = (line.price_unit - ((line.price_unit*line.descuento_porcentaje)/100))/20
                                _logger.info('descuento_porcentaje = {}'.format(line.descuento_porcentaje))
                            elif line.descuento_monto: 
                                nuevo_precio = (line.price_unit - line.descuento_monto)/20
                                _logger.info('descuento_monto = {}'.format(line.descuento_monto))
                            else:
                                nuevo_precio = line.price_unit/20
                                _logger.info('no se detecto descuento')
                        else:
                            if line.descuento_porcentaje:
                                nuevo_precio = (line.price_unit - ((line.price_unit*line.descuento_porcentaje)/100))
                                _logger.info('descuento_porcentaje = {}'.format(line.descuento_porcentaje))
                            elif line.descuento_monto: 
                                nuevo_precio = (line.price_unit - line.descuento_monto)
                                _logger.info('descuento_monto = {}'.format(line.descuento_monto))
                            else:
                                nuevo_precio = line.price_unit
                                _logger.info('no se detecto descuento')
                            
                        line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                        line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                        line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': self.partner_id})
                        line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})
                        if self.state == 'sale':
                            line.product_id.product_tmpl_id.write({'last_update_type_selector':'compra'})
                        if self.state == 'draft':
                            line.product_id.product_tmpl_id.write({'last_update_type_selector':'cotizacion'})
                        proveedor.write({'price':nuevo_precio})
                    else: continue
                else: continue
        return res
    
    def write(self, vals):
        vals, partner_vals = self._write_partner_values(vals)
        res = super().write(vals)
        if partner_vals:
            self.partner_id.sudo().write(partner_vals)  # Because the purchase user doesn't have write on `res.partner`            
                   
        for line in self.order_line:
            for proveedor in line.product_id.seller_ids:
                if proveedor.display_name in self.partner_id.display_name:
                    if proveedor.fijar_proveedor:    
                        _logger.info('line.product_uom.display_name = {}, line.display_name = {}, line.descuento_porcentaje = {}'.format(line.product_uom.display_name,line.display_name,line.descuento_porcentaje))
                        if line.product_uom.display_name == 'Tira 3mt' and line.display_name.find('V-WELL') == -1:
                            if line.descuento_porcentaje:
                                nuevo_precio = (line.price_unit - ((line.price_unit*line.descuento_porcentaje)/100))/3
                                _logger.info('descuento_porcentaje = {}'.format(line.descuento_porcentaje))
                            elif line.descuento_monto: 
                                nuevo_precio = (line.price_unit - line.descuento_monto)/3
                                _logger.info('descuento_monto = {}'.format(line.descuento_monto))
                            else:
                                nuevo_precio = line.price_unit/3
                                _logger.info('no se detecto descuento')
                        elif line.product_uom.display_name == 'Tira 6mt':
                            if line.descuento_porcentaje: 
                                nuevo_precio = (line.price_unit - ((line.price_unit*line.descuento_porcentaje)/100))/6
                                _logger.info('descuento_porcentaje = {}'.format(line.descuento_porcentaje))
                            elif line.descuento_monto: 
                                nuevo_precio = (line.price_unit - line.descuento_monto)/6
                                _logger.info('descuento_monto = {}'.format(line.descuento_monto))
                            else:
                                nuevo_precio = line.price_unit/6
                                _logger.info('no se detecto descuento')
                        elif line.product_uom.display_name == 'Balde 20' or line.product_uom.display_name == 'Bidón 20':
                            if line.descuento_porcentaje: 
                                nuevo_precio = (line.price_unit - ((line.price_unit*line.descuento_porcentaje)/100))/20
                                _logger.info('descuento_porcentaje = {}'.format(line.descuento_porcentaje))
                            elif line.descuento_monto: 
                                nuevo_precio = (line.price_unit - line.descuento_monto)/20
                                _logger.info('descuento_monto = {}'.format(line.descuento_monto))
                            else:
                                nuevo_precio = line.price_unit/20
                                _logger.info('no se detecto descuento')
                        else: 
                            if line.descuento_porcentaje:
                                nuevo_precio = (line.price_unit - ((line.price_unit*line.descuento_porcentaje)/100))
                                _logger.info('descuento_porcentaje = {}'.format(line.descuento_porcentaje))
                            elif line.descuento_monto: 
                                nuevo_precio = (line.price_unit - line.descuento_monto)
                                _logger.info('descuento_monto = {}'.format(line.descuento_monto))
                            else:
                                nuevo_precio = line.price_unit
                                _logger.info('no se detecto descuento')
                            
                        line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                        line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                        line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': self.partner_id})
                        line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})
                        if self.state == 'sale':
                            line.product_id.product_tmpl_id.write({'last_update_type_selector':'compra'})
                        if self.state == 'draft':
                            line.product_id.product_tmpl_id.write({'last_update_type_selector':'cotizacion'})
                        proveedor.write({'price':nuevo_precio})
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
                                if line.descuento_porcentaje:
                                    nuevo_precio = (line.price_unit - ((line.price_unit*descuento_porcentaje)/100))/3
                                    _logger.info('descuento_porcentaje = {}'.format(line.descuento_porcentaje))
                                elif line.descuento_monto: 
                                    nuevo_precio = (line.price_unit - line.descuento_monto)/3
                                    _logger.info('descuento_monto = {}'.format(line.descuento_monto))
                                else:
                                    nuevo_precio = line.price_unit/3
                                    _logger.info('no se detecto descuento')
                            elif line.product_uom.display_name == 'Tira 6mt':
                                if line.descuento_porcentaje: 
                                    nuevo_precio = (line.price_unit - ((line.price_unit*descuento_porcentaje)/100))/6
                                    _logger.info('descuento_porcentaje = {}'.format(line.descuento_porcentaje))
                                elif line.descuento_monto: 
                                    nuevo_precio = (line.price_unit - line.descuento_monto)/6
                                    _logger.info('descuento_monto = {}'.format(line.descuento_monto))
                                else:
                                    nuevo_precio = line.price_unit/6
                                    _logger.info('no se detecto descuento')
                            elif line.product_uom.display_name == 'Balde 20' or line.product_uom.display_name == 'Bidón 20':
                                if line.descuento_porcentaje: 
                                    nuevo_precio = (line.price_unit - ((line.price_unit*descuento_porcentaje)/100))/20
                                    _logger.info('descuento_porcentaje = {}'.format(line.descuento_porcentaje))
                                elif line.descuento_monto: 
                                    nuevo_precio = (line.price_unit - line.descuento_monto)/20
                                    _logger.info('descuento_monto = {}'.format(line.descuento_monto))
                                else:
                                    nuevo_precio = line.price_unit/20
                                    _logger.info('no se detecto descuento')
                            else: 
                                if line.descuento_porcentaje:
                                    nuevo_precio = (line.price_unit - ((line.price_unit*descuento_porcentaje)/100))
                                    _logger.info('descuento_porcentaje = {}'.format(line.descuento_porcentaje))
                                elif line.descuento_monto: 
                                    nuevo_precio = (line.price_unit - line.descuento_monto)
                                    _logger.info('descuento_monto = {}'.format(line.descuento_monto))
                                else:
                                    nuevo_precio = line.price_unit
                                    _logger.info('no se detecto descuento')
                                
                            line.product_id.product_tmpl_id.write({'list_price': nuevo_precio})                        
                            line.product_id.product_tmpl_id.write({'standard_price': nuevo_precio})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_partner': self.partner_id})
                            line.product_id.product_tmpl_id.write({'last_update_pricelist_date': fields.Date.context_today(self)})     
                        else:
                            continue
                    else:
                        continue
            
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True
    
class DescuentoLineaCompra(models.Model):
    _inherit = 'purchase.order.line'

    
    def _prepare_compute_all_values(self):        
        # _logger.info('dentro de prepare_compute_all_values')
        self.ensure_one()
        if self.descuento_porcentaje:
            return {
                'price_unit': self.price_unit - (self.price_unit*(self.descuento_porcentaje/100)),
                'currency': self.order_id.currency_id,
                'quantity': self.product_qty,
                'product': self.product_id,
                'partner': self.order_id.partner_id,
            }
        elif self.descuento_monto:
            return {
                'price_unit': self.price_unit - self.descuento_monto,
                'currency': self.order_id.currency_id,
                'quantity': self.product_qty,
                'product': self.product_id,
                'partner': self.order_id.partner_id,
            }
        else:
            return {
                'price_unit': self.price_unit,
                'currency': self.order_id.currency_id,
                'quantity': self.product_qty,
                'product': self.product_id,
                'partner': self.order_id.partner_id,
            }                

    descuento_porcentaje = fields.Float(string="Descuento(%)", default=0.0)
    descuento_monto = fields.Float(string="Descuento($)", default=0.0)
    