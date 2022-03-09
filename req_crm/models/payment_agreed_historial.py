# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Lead(models.Model):
    _inherit = "crm.lead"
    
    payment_agreed_matriz_ids = fields.One2many(
        comodel_name="payment.agreed",
        inverse_name="payment_agreed_id", string=' ')
    
class PaymentAgreed(models.Model):
    _name = "payment.agreed"   
    
    payment_agreed_id = fields.Many2one(comodel_name="crm.lead")
    Abono_monto = fields.Integer(string="Abono ($)")
    Abono_porcentaje = fields.Integer(string="Abono (%)")
    descuento_iva = fields.Integer("Descuento IVA (%)") 
    num_cuotas = fields.Integer(string="Num. Cuotas")
    fijar_ac = fields.Boolean(string="Fijar a.c",default=True)
    comentarios = fields.Char(string="Comentarios")
    