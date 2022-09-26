# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from itertools import groupby
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    
    settlement_code = fields.Char(string="Código liquidación")
    
    
    def button_validate(self):
        res = super(StockPicking,self).button_validate()
        self.verification_service_closures()
        return res
    
    
    def verification_service_closures(self):
        if self.origin:
            _logger.info('origin validado = {}'.format(self.origin))
            cierre = False
            origin_sale_order = self.env['sale.order'].search([('name','=',self.origin)])
            for picking_ids in origin_sale_order.picking_ids:
                _logger.info('revisando picking = {}'.format(picking_ids.servicio_reservado))
                closure_picking = self.env['stock.picking'].search([('id','!=',picking_ids.id),('servicio_reservado','=',picking_ids.servicio_reservado),('origin','=',self.origin),('state','=','done')])
                if closure_picking:
                    _logger.info('existe cierre aprobado para = {}'.format(picking_ids.servicio_reservado))
                    if closure_picking.settlement_code:                        
                        _logger.info('existe liquidacion para = {}'.format(picking_ids.servicio_reservado))
                        continue
                    else:                        
                        _logger.info('liquidacion pendiente para = {}'.format(picking_ids.servicio_reservado))
                        cierre = True
                else:
                    #significa que se esta validando una transferencia a bodega satelite, no un cierre.
                    _logger.info('no existe cierre aprobado para = {}'.format(picking_ids.servicio_reservado))
                    continue
            if cierre:
                opportunity_id = self.env['crm.lead'].search([('id','=',origin_sale_order.opportunity_id.id)])
                siguiente_etapa = self.env['crm.stage'].search([('name','=','CERRADO')])
                opportunity_id.write({
                     'pending_settlements':True,
                     'color_settlement':1,
                     'stage_id':siguiente_etapa.id
                    })
                
                
                