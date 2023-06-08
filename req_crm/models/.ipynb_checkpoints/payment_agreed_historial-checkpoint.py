# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class Lead(models.Model):
    _inherit = "crm.lead"
    
    payment_agreed_matriz_ids = fields.One2many(
        comodel_name="payment.agreed",
        inverse_name="payment_agreed_id", string=' ')
    
    @api.onchange('payment_agreed_matriz_ids')
    def onchange_matriz_s4(self):
        #_logger.info('cambio en matriz de servicio 4= {}'.format(True))        
        for line_s4 in self.lead_matriz_s4_lines_ids:
            if 'PRUEBA DE BOMBEO' in line_s4.listado_servicios.name:
                self.update({'caudal_esperado_check':True})
            """    
            else:
                self.update({'caudal_esperado_check':False})
            """
    
class PaymentAgreed(models.Model):
    _name = "payment.agreed" 
    _description = "registro de acuerdos de pago"
    
    
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
    payment_method = fields.Selection([('efectivo','Efectivo'),('tarjeta_credito','Tarjeta de crédito'),('cheque','Cheque'),('transferencia','Transferencia')],string="Forma de pago",default="transferencia",required=True)
    