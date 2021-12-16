# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProducTemplate(models.Model):
    _inherit='product.template'
    
    @api.depends('last_update_pricelist_date')
    def compute_difference(self):
        for date in self:
            if date.last_update_pricelist_date != False:
                date.last_update_number_days = (fields.Date.context_today(self) - date.last_update_pricelist_date).days
            else:
                date.last_update_number_days = 46
            
    
    last_update_pricelist_date = fields.Date(string='Ultima actualizacion de precio')
    last_update_pricelist_partner = fields.Many2one('res.partner',string='Proveedor',readonly=True)
    last_update_type = fields.Boolean(string="Tipo de ultima actualización")
    last_update_type_selector = fields.Selection([('indefinido', 'Indefinido'),('cotizacion','Cotización'),('compra','Compra')],string="Tipo de actualización", default='indefinido')
    last_update_number_days = fields.Integer(string="Dias transcurridos", compute=compute_difference)

