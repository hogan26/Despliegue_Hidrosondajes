# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProducTemplate(models.Model):
    _inherit='product.template'
    
    
    inches = fields.Integer(string="Pulgadas")