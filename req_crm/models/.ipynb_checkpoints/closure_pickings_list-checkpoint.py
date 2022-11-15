# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from itertools import groupby
from odoo.exceptions import UserError,ValidationError
from datetime import datetime , time


_logger = logging.getLogger(__name__)

class Lead(models.Model):
    _inherit = "crm.lead"    
    
    
    def action_view_closure_pickings(self):
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        closure_ids = []
        if self.order_ids:
            for sale_order in self.order_ids:
                if sale_order.state == "sale":
                    for picking_ids in sale_order.picking_ids:                    
                        closure_pickings = self.env['stock.picking'].search([('id','!=',picking_ids.id),('servicio_reservado','=',picking_ids.servicio_reservado),('origin','=',sale_order.name),('service_shutdown_creator','!=',False),('state','=','done')])
                        if closure_pickings:
                            for closure_picking in closure_pickings:
                                closure_ids.append(closure_picking.id)
                                _logger.info('closure_ids.name = {}'.format(closure_picking.name))
                        else:
                            continue
                            
                            
                    if len(closure_ids)>0:
                        pickings = closure_ids
                        _logger.info('pickings = {}'.format(pickings))
                        if len(pickings) > 1:
                            action['domain'] = [('id', 'in', pickings)]
                        elif pickings:
                            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
                            if 'views' in action:
                                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
                            else:
                                action['views'] = form_view
                            action['res_id'] = pickings[0]

                        return action
                    else:
                        raise ValidationError("No se han encontrado cierres validados")                        
        else:
            raise ValidationError("No existen documentos de ventas vinculados a este requerimiento")
        
        

#         pickings = self.mapped('order_ids.picking_ids')
        
#         if len(pickings) > 1:
#             action['domain'] = [('id', 'in', pickings.ids)]
#         elif pickings:
#             form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
#             if 'views' in action:
#                 action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
#             else:
#                 action['views'] = form_view
#             action['res_id'] = pickings.id
            
        # Prepare the context.
#         picking_id = pickings.filtered(lambda l: l.picking_type_id.code == 'outgoing')
#         if picking_id:
#             picking_id = picking_id[0]
#         else:
#             picking_id = pickings[0]
#         action['context'] = dict(self._context, default_partner_id=self.partner_id.id, default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name, default_group_id=picking_id.group_id.id)
#         return action
        
        
        
        
        
#         raise ValidationError("dentro de la funcion")