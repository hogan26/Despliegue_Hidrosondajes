# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LastUpdatePriceLine(models.Model):
    _inherit='sale.order.line'
    
    def compute_validation(self):
        for number in self:
            if number.last_update_number_days >= 45:
                number.number_days_context = True
            else:
                number.number_days_context = False
    
    last_update_price_date = fields.Date(related='product_template_id.last_update_pricelist_date',readonly=True)
    last_update_price_partner = fields.Many2one('res.partner',related='product_template_id.last_update_pricelist_partner',readonly=True)
    last_update_type_selector = fields.Selection(related='product_template_id.last_update_type_selector',readonly=False)
    last_update_number_days = fields.Integer(related='product_template_id.last_update_number_days',readonly=True)
    number_days_context = fields.Boolean(string="validacion de dias",compute=compute_validation)