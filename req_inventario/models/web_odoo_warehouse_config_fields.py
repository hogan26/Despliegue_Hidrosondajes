# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockWarehouse(models.Model):
    _inherit='stock.warehouse'
    
    show_in_web_system = fields.Boolean(string="Mostrar en sistema web")
    servicio_perforacion = fields.Boolean(string="Servicio 1")
    servicio_bombeo = fields.Boolean(string="Servicio 2")
    servicio_almacenamiento = fields.Boolean(string="Servicio 3")
    servicio_prueba_bombeo = fields.Boolean(string="Prueba de bombeo")
    servicio_limpieza = fields.Boolean(string="Limpieza")
    servicio_diagnostico = fields.Boolean(string="Diagnostico")