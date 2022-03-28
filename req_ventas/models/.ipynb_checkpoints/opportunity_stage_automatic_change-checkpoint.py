# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    
    @api.model_create_multi
    def create(self,vals_list):
        res = super(SaleOrder,self).create(vals_list)        
        if res.opportunity_id:
            id_requerimiento = res.opportunity_id.id
            etapa = res.opportunity_id.stage_id.name
            #_logger.info('id_requerimiento = {}'.format(id_requerimiento))
            #_logger.info('etapa = {}'.format(etapa))
            
            if etapa == 'INICIO':
                siguiente_etapa = self.env['crm.stage'].search([('name','=','ELABORADO')])
                res.opportunity_id.update({'stage_id':siguiente_etapa.id})
                
        return res
    
    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm()        
        if self.opportunity_id:
            current_stage = self.opportunity_id.stage_id.name
            if current_stage == 'INICIO' or current_stage == 'Elaborado' or current_stage == 'ENVIADO':
                siguiente_etapa = self.env['crm.stage'].search([('name','=','CONFIRMADO')])
                self.opportunity_id.update({'stage_id':siguiente_etapa.id})
                
        return res
    
    
class MailComposer(models.TransientModel):
    _inherit='mail.compose.message'    
    
    def action_send_mail(self):        
        res = super(MailComposer,self).action_send_mail()
        quotation_name = self.attachment_ids.res_name
        current_quotation_object = self.env['sale.order'].search([('name','=',quotation_name)])
        if current_quotation_object.opportunity_id:
            current_lead = current_quotation_object.opportunity_id
            if current_lead.stage_id.name == 'INICIO' or current_lead.stage_id.name == 'ELABORADO':
                siguiente_etapa = self.env['crm.stage'].search([('name','=','ENVIADO')])
                current_lead.update({'stage_id':siguiente_etapa.id})
                
        return res