# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Lead(models.Model):
    _inherit = "crm.lead"
    
    lead_matriz_lines_ids = fields.One2many(
        comodel_name="matriz.perforacion",
        inverse_name="matriz_line_id", string="lineas de matriz de perforacion")
    corona_matriz_lines_ids = fields.One2many(
        comodel_name="coronas.perforacion",
        inverse_name="corona_line_id", string="lineas de coronas para matriz de perforacion")
    matriz_activada = fields.Boolean(string="Usar matriz")
    retiro_material = fields.Integer(string="Retiro de material")
    
    
    @api.model
    def default_get(self,field_list):
        res=super(Lead,self).default_get(field_list)
        res.update({'matriz_activada':True})
        return res       
    
    
class MatrizPerforacion(models.Model):
    _name = "matriz.perforacion"
    _description = 'matriz de servicio de perforacion'
    
    matriz_line_id = fields.Many2one(comodel_name="crm.lead")
    tipo_servicio_perforacion = fields.Many2one('product.template',string='Tipo servicio',domain=[('categ_id','=','SERVICIOS / PERFORACION')])
    cantidad_metros = fields.Integer(string="Metros")
    valor_metro = fields.Integer(string="Valor mt")   
    
    
class CoronasPerforacion(models.Model):
    _name = "coronas.perforacion"
    _description = 'coronas para matriz de servicio de perforacion'
    
    corona_line_id = fields.Many2one(comodel_name="crm.lead")
    corona = fields.Many2one('product.template',string='Corona',domain=[('categ_id','=','OPERACIÓN PERFORACIÓN / HERRAMIENTAS PERFORACIÓN / CORONAS')])