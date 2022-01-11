# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Lead(models.Model):
    _inherit = "crm.lead"
    
    lead_matriz_s4_lines_ids = fields.One2many(
        comodel_name="matriz.servicio4",
        inverse_name="matriz_s4_line_id", string="lineas de matriz para servicio 4")
    
class MatrizServicio4(models.Model):
    _name = "matriz.servicio4"
    _description = 'matriz de servicios especiales'
    
    matriz_s4_line_id = fields.Many2one(comodel_name="crm.lead")
    listado_servicios = fields.Many2one('product.template',string='Servicio',domain=[('categ_id','in',[('SERVICIOS'),('SERVICIOS / PRUEBAS')])])
    valor_servicio = fields.Integer(string="Valor")
    
    
    
