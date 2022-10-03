# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class Lead(models.Model):
    _inherit = "crm.lead"
    
    
    pending_settlements = fields.Boolean(string="liquidaciones pendientes",default=False)
    color_settlement = fields.Integer(string="Color liquidación")
    
    def new_settlement_form(self):
        settlements = []
        for sale_order in self.order_ids:
            if sale_order.state == "sale":
                partner_invoice_id = sale_order.partner_invoice_id.id
                partner_shipping_id = sale_order.partner_shipping_id.id
                _logger.info('partner_invoice_id = {},partner_shipping_id = {}'.format(partner_invoice_id,partner_shipping_id))
                for picking_ids in sale_order.picking_ids:                    
                    closure_pickings = self.env['stock.picking'].search([('id','!=',picking_ids.id),('servicio_reservado','=',picking_ids.servicio_reservado),('origin','=',sale_order.name),('state','=','done')])
                    if closure_pickings:                        
                        for closure_picking in closure_pickings:
                            if closure_picking.settlement_code:                            
                                continue
                            else:                            
                                settlements.append(closure_picking.servicio_reservado)
                    else:                        
                        continue
                        
        
        if len(settlements)>0:
            if 's1' in settlements and 's2' in settlements and 's3' in settlements:
                return {
                    'type':'ir.actions.act_window',
                    'res_model':'sale.order',
                    'res_id':False,
                    'view_mode':'form',
                    'context': {
                        'default_state':'cerrar',
                        'default_state_settlement':'cerrar',
                        'default_opportunity_id':self.id,
                        'default_partner_id':self.partner_id.id,
                        'default_partner_invoice_id':partner_invoice_id,
                        'default_partner_shipping_id':partner_shipping_id,
                        'default_num_telefono':self.partner_id.mobile,
                        'default_direccion':self.partner_id.city,
                        'default_calle':self.partner_id.street2,
                        'default_pending_settlements_select':'s1s2s3'
                    }                
                }
            elif 's1' in settlements and 's2' in settlements and 's3' not in settlements:                
                return {
                    'type':'ir.actions.act_window',
                    'res_model':'sale.order',
                    'res_id':False,
                    'view_mode':'form',
                    'context': {
                        'default_state':'cerrar',
                        'default_state_settlement':'cerrar',
                        'default_opportunity_id':self.id,
                        'default_partner_id':self.partner_id.id,
                        'default_partner_invoice_id':partner_invoice_id,
                        'default_partner_shipping_id':partner_shipping_id,
                        'default_num_telefono':self.partner_id.mobile,
                        'default_direccion':self.partner_id.city,
                        'default_calle':self.partner_id.street2,
                        'default_pending_settlements_select':'s1s2'
                    }                
                }
            elif 's1' in settlements and 's2' not in settlements and 's3' not in settlements:                
                return {
                    'type':'ir.actions.act_window',
                    'res_model':'sale.order',
                    'res_id':False,
                    'view_mode':'form',
                    'context': {
                        'default_state':'cerrar',
                        'default_state_settlement':'cerrar',
                        'default_opportunity_id':self.id,
                        'default_partner_id':self.partner_id.id,
                        'default_partner_invoice_id':self.partner_id.id,
                        'default_partner_shipping_id':self.partner_id.id,
                        'default_num_telefono':self.partner_id.mobile,
                        'default_direccion':self.partner_id.city,
                        'default_calle':self.partner_id.street2,
                        'default_pending_settlements_select':'s1'
                    }                
                }
            elif 's1' not in settlements and 's2' in settlements and 's3' not in settlements:                
                return {
                    'type':'ir.actions.act_window',
                    'res_model':'sale.order',
                    'res_id':False,
                    'view_mode':'form',
                    'context': {
                        'default_state':'cerrar',
                        'default_state_settlement':'cerrar',
                        'default_opportunity_id':self.id,
                        'default_partner_id':self.partner_id.id,
                        'default_partner_invoice_id':partner_invoice_id,
                        'default_partner_shipping_id':partner_shipping_id,
                        'default_num_telefono':self.partner_id.mobile,
                        'default_direccion':self.partner_id.city,
                        'default_calle':self.partner_id.street2,
                        'default_pending_settlements_select':'s2'
                    }                
                }
            elif 's1' not in settlements and 's2' not in settlements and 's3' in settlements:
                return {
                    'type':'ir.actions.act_window',
                    'res_model':'sale.order',
                    'res_id':False,
                    'view_mode':'form',
                    'context': {
                        'default_state':'cerrar',
                        'default_state_settlement':'cerrar',
                        'default_opportunity_id':self.id,
                        'default_partner_id':self.partner_id.id,
                        'default_partner_invoice_id':partner_invoice_id,
                        'default_partner_shipping_id':partner_shipping_id,
                        'default_num_telefono':self.partner_id.mobile,
                        'default_direccion':self.partner_id.city,
                        'default_calle':self.partner_id.street2,
                        'default_pending_settlements_select':'s3'
                    }                
                }               
            elif 's1' not in settlements and 's2' in settlements and 's3' in settlements:                
                return {
                    'type':'ir.actions.act_window',
                    'res_model':'sale.order',
                    'res_id':False,
                    'view_mode':'form',
                    'context': {
                        'default_state':'cerrar',
                        'default_state_settlement':'cerrar',
                        'default_opportunity_id':self.id,
                        'default_partner_id':self.partner_id.id,
                        'default_partner_invoice_id':partner_invoice_id,
                        'default_partner_shipping_id':partner_shipping_id,
                        'default_num_telefono':self.partner_id.mobile,
                        'default_direccion':self.partner_id.city,
                        'default_calle':self.partner_id.street2,
                        'default_pending_settlements_select':'s2s3'
                    }                
                }
            elif 's4' in settlements:                
                return {
                    'type':'ir.actions.act_window',
                    'res_model':'sale.order',
                    'res_id':False,
                    'view_mode':'form',
                    'context': {
                        'default_state':'cerrar',
                        'default_state_settlement':'cerrar',
                        'default_opportunity_id':self.id,
                        'default_partner_id':self.partner_id.id,
                        'default_partner_invoice_id':partner_invoice_id,
                        'default_partner_shipping_id':partner_shipping_id,
                        'default_num_telefono':self.partner_id.mobile,
                        'default_direccion':self.partner_id.city,
                        'default_calle':self.partner_id.street2,
                        'default_pending_settlements_select':'s4'
                    }                
                }
        else:
            return {
                'type':'ir.actions.act_window',
                'res_model':'sale.order',
                'res_id':False,
                'view_mode':'form',
                'context': {
                    'default_state':'cerrar',
                    'default_state_settlement':'cerrar',
                    'default_opportunity_id':self.id,
                    'default_partner_id':self.partner_id.id,
                    'default_partner_invoice_id':partner_invoice_id,
                    'default_partner_shipping_id':partner_shipping_id,
                    'default_num_telefono':self.partner_id.mobile,
                    'default_direccion':self.partner_id.city,
                    'default_calle':self.partner_id.street2,
                    'default_pending_settlements_select':'no'
                }                
            }
        
    
    def verification_service_closures(self):
        cierre = False
        for sale_order in self.order_ids:
            if sale_order.state == "sale":
                for picking_ids in sale_order.picking_ids:
                    _logger.info('revisando picking = {}'.format(picking_ids.servicio_reservado))
                    closure_pickings = self.env['stock.picking'].search([('id','!=',picking_ids.id),('servicio_reservado','=',picking_ids.servicio_reservado),('origin','=',sale_order.name),('state','=','done')])
                    if closure_pickings:
                        for closure_picking in closure_pickings:
                            _logger.info('existe cierre aprobado para = {}'.format(picking_ids.servicio_reservado))
                            if closure_picking.settlement_code:
                                _logger.info('existe liquidacion para = {}'.format(picking_ids.servicio_reservado))
                                continue
                            else:                        
                                _logger.info('liquidacion pendiente para = {}'.format(picking_ids.servicio_reservado))
                                cierre = True
                    else:                        
                        _logger.info('no existe cierre aprobado para = {}'.format(picking_ids.servicio_reservado))
                        continue
                if cierre:                    
                    self.write({'pending_settlements':True})
                    self.write({'color_settlement':1})
                