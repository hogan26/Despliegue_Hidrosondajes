# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class Lead(models.Model):
    _inherit = "crm.lead"
    
    payment_agreed_matriz_ids = fields.One2many(
        comodel_name="payment.agreed",
        inverse_name="payment_agreed_id", string=' ')
    
class PaymentAgreed(models.Model):
    _name = "payment.agreed" 
    _description = "registro de acuerdos de pago"
    
    @api.model
    def default_get(self,fields_list):
        res = super(PaymentAgreed,self).default_get(fields_list)
        _logger.info('payment_agreed_matriz_ids= {}'.format(self.payment_agreed_id.payment_agreed_matriz_ids))
        '''
        if self.partner_id.vat:
            self.update({'rut_facturacion':self.partner_id.vat})
        '''            
        return res
    
    payment_agreed_id = fields.Many2one(comodel_name="crm.lead")
    Abono_monto = fields.Integer(string="Abono ($)")
    Abono_porcentaje = fields.Integer(string="Abono (%)")
    descuento_neto_porcentaje = fields.Integer(string="Descuento neto (%)")
    descuento_neto_monto = fields.Integer(string="Descuento neto ($)")
    descuento_iva = fields.Integer("Descuento IVA (%)") 
    num_cuotas = fields.Integer(string="Num. Cuotas")
    fijar_ac = fields.Boolean(string="Fijar a.c",default=True)
    comentarios = fields.Char(string="Comentarios")
    rut_facturacion = fields.Char(string="Rut Facturación")
    