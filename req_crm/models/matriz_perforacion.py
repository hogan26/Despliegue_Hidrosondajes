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
    tipo_servicio_perforacion = fields.Many2one('product.template',string='Tipo servicio',domain=[('categ_id','in',[('SERVICIOS / PERFORACION'),('SERVICIOS / ENTUBACION')])])
    cantidad_metros = fields.Integer(string="Metros")
    valor_metro = fields.Integer(string="Valor mt")   
    
    
class CoronasPerforacion(models.Model):
    _name = "coronas.perforacion"
    _description = 'coronas para matriz de servicio de perforacion'    
    
    
    @api.onchange('corona')
    def onchange_corona(self):
        data = self.env['product.template'].search([('id','=',self.corona.id)])
        self.update({'precio':data.list_price})
        self.update({'proveedor':data.last_update_pricelist_partner.name})
        self.update({'tipo_ult_com':data.last_update_type_selector})
        self.update({'fecha_ult_com':data.last_update_pricelist_date})
    
    corona_line_id = fields.Many2one(comodel_name="crm.lead")
    corona = fields.Many2one('product.template',string='Corona',domain=[('categ_id','=','OPERACIÓN PERFORACIÓN / HERRAMIENTAS PERFORACIÓN / CORONAS')])
    precio = fields.Integer(string="Precio u.a",store=True)
    proveedor = fields.Char(string="Proveedor u.a",readonly=True,store=True)
    tipo_ult_com = fields.Char(string="Tipo u.a",readonly=True,store=True)
    fecha_ult_com = fields.Date(string="fecha u.a",readonly=True,store=True)