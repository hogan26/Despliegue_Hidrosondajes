# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Lead(models.Model):
    _inherit = "crm.lead"
    
    corona = fields.Many2one('product.template',string='Corona',domain=[('categ_id','=','OPERACIÓN PERFORACIÓN / HERRAMIENTAS PERFORACIÓN / CORONAS')])
    