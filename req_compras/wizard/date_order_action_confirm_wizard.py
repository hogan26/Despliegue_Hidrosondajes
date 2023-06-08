# -*- coding: utf-8 -*-

from odoo import models, fields, api , tools, _
from odoo.exceptions import AccessError, UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)

class DateOrderWizard(models.TransientModel):
    _name = 'wizard.date.purchase'
    _description = 'ventana de alerta para confirmar la fecha del pedido de una order de compra'
    
    date_order = fields.Datetime(string='Fecha de pedido')    
    
    def purchase_order_confirm_wizard(self):
        purchase_order = self.env['purchase.order'].search([('name','=',self._context['parent_obj'])])
        if self.date_order:            
            purchase_order.write({'date_order':self.date_order})            
            purchase_order.button_confirm()
        else:
            raise ValidationError('Debe ingresar una fecha')
