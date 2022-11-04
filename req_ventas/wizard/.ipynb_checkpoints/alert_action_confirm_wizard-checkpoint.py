# -*- coding: utf-8 -*-

from odoo import models, fields, api , tools, _
from odoo.exceptions import AccessError, UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)

class ConfirmWizard(models.TransientModel):
    _name = 'wizard.confirm'
    
    abono_porcentaje = fields.Integer(string='Abono inicial (%)')
    abono_monto = fields.Integer(string='Abono ($)')
    descuento_iva = fields.Integer(string='Descuento IVA')
    descuento_neto_porcentaje = fields.Integer(string='Descuento neto (%)')
    descuento_neto_monto = fields.Integer(string='Descuento neto ($)')
    num_cuotas = fields.Integer(string='Num. cuotas')
    payment_method = fields.Selection([('efectivo','Efectivo'),('tarjeta_credito','Tarjeta de crédito'),('cheque','Cheque'),('transferencia','Transferencia')],string="Forma de pago")
    observaciones = fields.Char(string='Observaciones')
    set_new_payment_agreed = fields.Boolean(string="Fijar nuevo acuerdo comercial")
    
    
    def sale_confirm_wizard(self):
        sale_order = self.env['sale.order'].search([('name','=',self._context['parent_obj'])])
        if self.set_new_payment_agreed:
            crm_lead = self.env['crm.lead'].search([('id','=',sale_order.opportunity_id.id)])
            
            for payment_agreed_lines in crm_lead.payment_agreed_matriz_ids:
                payment_agreed_lines.write({'fijar_ac':False})
            
            crm_lead.write({
                'payment_agreed_matriz_ids': [(0, 0, {
                    'Abono_monto': self.abono_monto,
                    'Abono_porcentaje': self.abono_porcentaje,
                    'descuento_neto_porcentaje': self.descuento_neto_porcentaje,
                    'descuento_neto_monto': self.descuento_neto_monto,
                    'descuento_iva': self.descuento_iva,
                    'num_cuotas': self.num_cuotas,
                    'fijar_ac': True,
                    'comentarios': self.observaciones,
                    'rut_facturacion': sale_order.partner_id.vat,
                    'payment_method': self.payment_method
                })]
            })

            sale_order.write({
                'abono_porcentaje':self.abono_porcentaje,
                'abono_monto':self.abono_monto,
                'descuento_iva':self.descuento_iva,
                'descuento_neto_porcentaje':self.descuento_neto_porcentaje,
                'descuento_neto_monto':self.descuento_neto_monto,
                'num_cuotas':self.num_cuotas,
                'payment_method':self.payment_method,
                'observaciones':self.observaciones                
            })
            
            sale_order.action_confirm()
        else:
            sale_order.action_confirm()
        
#         raise ValidationError(_("name de la cotizacion pasada por contexto: %s ") % (self._context['parent_obj']))
