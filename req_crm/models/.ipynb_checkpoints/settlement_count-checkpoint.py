# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.sale_crm.models.crm_lead import CrmLead as OriginalCrmLead

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = "crm.lead"
    
    
    def action_view_sale_order(self):        
        action = self.env.ref('sale.action_orders').read()[0]
        action['context'] = {
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_opportunity_id': self.id,
        }
        action['domain'] = [('opportunity_id', '=', self.id), ('state', 'not in', ('draft', 'sent', 'cancel','cerrar','liquidar'))]
        orders = self.mapped('order_ids').filtered(lambda l: l.state not in ('draft', 'sent', 'cancel','cerrar','liquidar'))
        if len(orders) == 1:
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = orders.id
        
        OriginalCrmLead.action_view_sale_order = self.action_view_sale_order
        
        return action
    
    
    def action_view_settlement(self):        
        action = self.env.ref('sale.action_orders').read()[0]
        action['context'] = {
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_opportunity_id': self.id,
        }
        action['domain'] = [('opportunity_id', '=', self.id), ('state_settlement', 'in', ('cerrar','liquidar'))]
        orders = self.mapped('order_ids').filtered(lambda l: l.state_settlement in ('cerrar','liquidar'))
        if len(orders) == 1:
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = orders.id        
        
        return action
    
    
    @api.depends('order_ids.state', 'order_ids.currency_id', 'order_ids.amount_untaxed', 'order_ids.date_order', 'order_ids.company_id', 'order_ids.amount_total')
    def _compute_sale_data(self):
        for lead in self:
            total = 0.0
            quotation_cnt = 0
            sale_order_cnt = 0
            settlement_count = 0
            settlement_amount_total = 0.0
            company_currency = lead.company_currency or self.env.company.currency_id
            for order in lead.order_ids:
                if order.state in ('draft', 'sent'):
                    quotation_cnt += 1
                if order.state not in ('draft', 'sent', 'cancel','cerrar','liquidar'):
                    sale_order_cnt += 1
                    total += order.currency_id._convert(
                        order.amount_total, company_currency, order.company_id, order.date_order or fields.Date.today())
                if order.state not in ('draft', 'sent', 'cancel','sale','done'):
                    settlement_count += 1
                    settlement_amount_total += order.currency_id._convert(
                        order.amount_total, company_currency, order.company_id, order.date_order or fields.Date.today())
            lead.sale_amount_total = total
            lead.quotation_count = quotation_cnt
            lead.sale_order_count = sale_order_cnt
            lead.settlement_count = settlement_count
            lead.settlement_amount_total = settlement_amount_total
            
        OriginalCrmLead._compute_sale_data = self._compute_sale_data
        
        
        
    settlement_count = fields.Integer(compute='_compute_sale_data',string="Número de liquidaciones")
    settlement_amount_total = fields.Monetary(compute='_compute_sale_data',string="Suma montos liquidaciones",currency_field='company_currency')