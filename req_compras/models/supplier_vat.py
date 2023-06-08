# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit='purchase.order'
    
    vat = fields.Char(related="partner_id.vat",string="Rut proveedor",store=True,readonly=False)
    
    def button_confirm(self):
        res = super(PurchaseOrder,self).button_confirm()
        
        if not(self.vat):
            raise ValidationError('El campo "Rut proveedor" está vacío, por favor complete este campo e intente confirmar el pedido nuevamente')
        if not(self.partner_ref):
            raise ValidationError('El campo "Referencia de proveedor" está vacío, el cual es el equivalente al campo "Folio" de la factura, por favor complete este campo e intente confirmar el pedido nuevamente')
        
        return res