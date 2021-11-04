# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProducTemplate(models.Model):
    _inherit='product.template'
    
    last_update_pricelist_date = fields.Date(string='Ultima actulizacion de precio')
    last_update_pricelist_partner = fields.Many2one('res.partner',string='Proveedor',readonly=True)

