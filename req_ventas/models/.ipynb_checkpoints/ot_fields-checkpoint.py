# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    #para ordenes de trabajo
    x_equipo_asignado = fields.Selection([('eqp21','Equipo 21'),('eqp22','Equipo 22'),('eqp23','Equipo 23'),('eqp24','Equipo 24'),('eqb1','Equipo Bombas 1'),('eqb2','Equipo Bombas 2'),('eqb3','Equipo Bombas 3')],string='Equipo asignado')
    x_fecha_retiro = fields.Date(string='Fecha de retiro de materiales')
    ot_tipo_servicio = fields.Selection([('perforacion','Perforación'),('bombas','Bombas')],string='Tipo de servicio')
    configuracion_perforacion = fields.Html(string='Configuracion perforación')
    detalle_stock_seguridad = fields.Html(string='Detalle stock de seguridad')
    observaciones = fields.Char(string='Observaciones')
    num_telefono = fields.Char(related='partner_id.mobile',string='Mobil',readonly=False)
    calle = fields.Char(related='partner_id.street',string='Calle',readonly=False)
    direccion = fields.Char(related='partner_id.street2',string='Direccion',readonly=False)
    
    
    