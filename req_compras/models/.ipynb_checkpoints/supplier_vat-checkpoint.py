# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit='purchase.order'
    
    vat = fields.Char(related="partner_id.vat",string="Rut proveedor",store=True,readonly=False)
    
    # revisar el flujo del codigo, al ejecutar esta funcion, si se cumple la condicion se muestra el wizard, pero aun asi se confirma 
    # la orden de compra independiente del boton que se presione en el wizard
    
#     def button_confirm(self):
#         res = super(PurchaseOrder,self).button_confirm()
        
#         if not(self.vat):
#             raise ValidationError('El campo "Rut proveedor" está vacío, por favor complete este campo e intente confirmar el pedido nuevamente')
#         if not(self.partner_ref):
#             raise ValidationError('El campo "Referencia de proveedor" está vacío, el cual es el equivalente al campo "Folio" de la factura, por favor complete este campo e intente confirmar el pedido nuevamente')
            
#         datetime_order = fields.Datetime.to_string(self.date_order)
#         date_order_datetime = fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(datetime_order)))[:10]
#         date_order = fields.Date.from_string(date_order_datetime)
#         if date_order == fields.Date.context_today(self): 
#             return {
#                 'type': 'ir.actions.act_window',
#                 'name': 'purchase_date_order_verification_confirm_button',
#                 'view_mode': 'form',
#                 'target': 'new',
#                 'res_model': 'wizard.date.purchase',
#                 'context': {'parent_obj': self.name,
#                             'default_date_order':self.date_order,
#                            } 
#             }
#         else:        
#             return res