# -*- coding: utf-8 -*-

from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit='purchase.order'
    
    def button_confirm(self):
        res = super(PurchaseOrder,self).button_confirm()
        if self.requisition_id:            
            requisition_pos = self.env['purchase.requisition'].search([('id','=',self.requisition_id.id)])
            if requisition_pos:
                for requisition in requisition_pos.purchase_ids:                    
                    if requisition.name != self.name:
                        requisition.button_cancel()
                requisition_pos.action_done()
        
        return res