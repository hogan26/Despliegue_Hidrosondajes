# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LastUpdatePriceLine(models.Model):
    _inherit='sale.order.line'
    
    last_update_price_date = fields.Date(related='product_template_id.last_update_pricelist_date',readonly=True)
    last_update_price_partner = fields.Many2one('res.partner',related='product_template_id.last_update_pricelist_partner',readonly=True)