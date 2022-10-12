# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from itertools import groupby
from odoo.exceptions import UserError
from datetime import datetime , time


_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'    
    
    
    @api.depends('fecha_ing','fecha_ter')
    def _calculo_dias_trabajados(self):
        for res in self:
            if res.fecha_ing and res.fecha_ter:
                res.dias_trabajados = (res.fecha_ter - res.fecha_ing).days
            else:
                res.dias_trabajados = 0
    
    #CAMPOS EN COMUN PARA TODOS LOS FORMULARIOS DE CIERRE
    
    #el campo service_shutdown_creator (quien_ingresa el cierre) esta definido en el archivo assign_picking_updated
    settlement_code = fields.Char(string="Código liquidación")    
    fecha_ing = fields.Date(string="Fecha de Inicio")
    fecha_ter = fields.Date(string="Fecha de Término")
    dias_trabajados = fields.Integer(string="Días trabajados",compute="_calculo_dias_trabajados")
    employee_closure_line_ids = fields.One2many(comodel_name="employee.closure",inverse_name="employee_closure_id", string="Trabajadores Involucrados")
    bonos_pagados = fields.Boolean(string="Bonos pagados")
    revision_supervisor = fields.Boolean(string="Revisión supervisor de operaciones")
    informe = fields.Boolean(string="Informe ok")
    revision_gerente_continuidad = fields.Boolean(string="Revision Gerente Continuidad")
    
    #CAMPOS EXCLUSIVOS PARA CIERRE DE SERVICIO 1
    
    agua = fields.Boolean(string="Se encontró agua?")
    prof_tot = fields.Integer(string="Profundidad Total")
    m_pincha = fields.Integer(string="Mts. pincha agua")
    vol_req = fields.Float(string="Vol. Estimado")
    tapa_pozo = fields.Binary(string="Foto de tapa del pozo")
    foto_entorno = fields.Binary(string="Foto orden y aseo del entorno")
    foto_rotura = fields.Binary(string="Foto rotura infraestructura del cliente")    
    foto_coordenadas = fields.Binary(string="Foto coordenadas")
    maquina = fields.Selection([('21','Maq21'),('22','Maq22'),('23','Maq23'),('24','Maq24')],string="Máquina")
    stratigraphy_line_ids = fields.One2many(comodel_name="perforation.stratigraphy",inverse_name="stratigraphy_id", string="Estratigrafía")
    detail_grooves_line_ids = fields.One2many(comodel_name="perforation.grooves",inverse_name="grooves_id", string="Ubicación Ranuraciones")
    comentarios_s1 = fields.Char(string="Comentarios s1")
    coordenadas_este = fields.Char(string="Este")
    coordenadas_oeste = fields.Char(string="Oeste")
    
    #CAMPOS PARA ENCUESTA AL SUPERVISOR SERVICIO 1
    
    participa = fields.Boolean(string="Participa en instalación")
    problemas_hm = fields.Text(string="Problemas mecánico/hidráulicos")
    cambio_punto_perforacion = fields.Text(string="Cambio punto de perforación")
    detalle_materiales_defectuosos = fields.Text(string="Detalle materiales defectuosos")
    herramientas_mal_estado = fields.Text(string="Herramientas en mal estado")
    corte_caneria = fields.Text(string="Corte cañerías")
    amonestacion_verbal = fields.Text(string="Amonestación verbal trabajadores")
    mejora_condiciones_seguridad = fields.Text(string="Condiciones de seguridad a mejorar")
    oportunidad_mejora = fields.Text(string="Oportunidad de mejora")
    comentarios_cliente = fields.Text(string="Comentarios comerciales del cliente")
    
    #CAMPOS EXCLUSIVOS PARA CIERRE DE SERVICIO 2
    
    pumping_capacity_line_ids = fields.One2many(comodel_name="pumping.capacity",inverse_name="pumping_capacity_id", string="Aforo")
    salida_pozo = fields.Binary(string="Salida pozo")
    panoramico = fields.Binary(string="Panorámico (pozo y tablero)")
    tramo_conexion_zanja = fields.Binary(string="Tramo conexión zanja")
    tablero_panoramico = fields.Binary(string="Tablero panoramico")
    interior_tablero = fields.Binary(string="Interior tablero")
    coordenadas_gps = fields.Binary(string="Coordenadas gps")
    comentarios_s2 = fields.Text("Comentarios s2")
    
    #CAMPOS EXCLUSIVOS PARA CIERRE DE SERVICIO 3
    
    comentarios_s3 = fields.Text("Comentarios s3")    
    
    #CAMPOS EXCLUSIVOS PARA CIERRE DE SERVICIO PRUEBA DE BOMBEO
    
    tipo_pb = fields.Selection([('2','2 Hrs'),('4','4 Hrs'),('8','8 Hrs'),('24','24 Hrs (DGA)')],string="Tipo de prueba de bombeo")
    diametro_pb = fields.Integer(string="Diametro")
    profundidad_pb = fields.Integer(string="Profundidad pozo")
    nivel_estatico = fields.Char(string="Nivel estático")
    mas_caudal = fields.Boolean(string="Puede dar mas caudal?")
    registro_fotografico = fields.Binary(string="Registro fotografico")
    dinamic_level_line_ids = fields.One2many(comodel_name="dinamic.level",inverse_name="dinamic_level_id", string="Caudales y niveles")
    comentarios_pb = fields.Text("Comentarios pb")
    
    #CAMPOS EXCLUSIVOS PARA CIERRE DE SERVICIO LIMPIEZA
    
    agua_limpieza = fields.Boolean(string="Se encontró agua? lim.")
    diametro_limpieza = fields.Integer(string="Diametro lim.")
    espesor_limpieza = fields.Char(string="Espesor lim.")
    profundidad_limpieza = fields.Integer(string="Profundidad total lim.")
    vol_estimado_limpieza = fields.Float(string="Volumen estimado lim.")
    maquina_limpieza = fields.Selection([('maq21','Maq21'),('maq22','Maq22'),('maq23','Maq23'),('maq24','Maq24')],string="Máquina lim.")
    comentarios_limpieza = fields.Text(string="Comentarios ser. lim.")
    foto_coordenadas_limpieza = fields.Binary(string="Foto coordenadas lim.")
    coordenada_este_limpieza = fields.Char(string="Coordenada este lim.")
    coordenada_oeste_limpieza = fields.Char(string="Coordenada oeste lim.")
    
    #CAMPOS EXCLUSIVOS PARA CIERRE DE SERVICIO DIAGNOSTICO
    
    descripcion_diagnostico = fields.Text(string="Descripción trabajo realizado")
    diagnostico = fields.Text(string="Diagnostico")
    comentarios_diag = fields.Text(string="Comentarios diag.")
    
    
    def button_validate(self):
        res = super(StockPicking,self).button_validate()
        self.verification_service_closures()
        return res
    
    
    def verification_service_closures(self):
        if self.origin:
            _logger.info('origin validado = {}'.format(self.origin))
            cierre = False
            origin_sale_order = self.env['sale.order'].search([('name','=',self.origin)])
            for picking_ids in origin_sale_order.picking_ids:
                _logger.info('revisando picking = {}'.format(picking_ids.servicio_reservado))
                closure_picking = self.env['stock.picking'].search([('id','!=',picking_ids.id),('servicio_reservado','=',picking_ids.servicio_reservado),('origin','=',self.origin),('state','=','done')])
                if closure_picking:
                    _logger.info('existe cierre aprobado para = {}'.format(picking_ids.servicio_reservado))
                    if closure_picking.settlement_code:                        
                        _logger.info('existe liquidacion para = {}'.format(picking_ids.servicio_reservado))
                        continue
                    else:                        
                        _logger.info('liquidacion pendiente para = {}'.format(picking_ids.servicio_reservado))
                        cierre = True
                else:
                    #significa que se esta validando una transferencia a bodega satelite, no un cierre.
                    _logger.info('no existe cierre aprobado para = {}'.format(picking_ids.servicio_reservado))
                    continue
            if cierre:
                opportunity_id = self.env['crm.lead'].search([('id','=',origin_sale_order.opportunity_id.id)])
                siguiente_etapa = self.env['crm.stage'].search([('name','=','CERRADO')])
                opportunity_id.write({
                     'pending_settlements':True,
                     'color_settlement':1,
                     'stage_id':siguiente_etapa.id
                    })
                
                
class EmployeeClosure(models.Model):    
    _name = "employee.closure"
    _description = "hace referencia a los trabajadores involucrados en el cierre de servicio"
    
    employee_closure_id = fields.Many2one(comodel_name="stock.picking")    
    employee_id = fields.Many2one("hr.employee",string="Nombre")
    employee_job = fields.Many2one("hr.job",string="Cargo")
    
    
class Stratigraphy(models.Model):    
    _name = "perforation.stratigraphy"
    _description = "detalla la estratigrafia del servicio de perforacion cerrado"
    
    stratigraphy_id = fields.Many2one(comodel_name="stock.picking")
    floor = fields.Char(string="Suelo")
    
    
class DetailGrooves(models.Model):    
    _name = "perforation.grooves"
    _description = "detalla la ubicacion de ranuraciones del servicio de perforacion cerrado"
    
    grooves_id = fields.Many2one(comodel_name="stock.picking")
    detail_grooves = fields.Char(string="Ranuras")
    

class Capacity(models.Model):
    _name = "pumping.capacity"
    _description = "aforo del sistema de bombeo detallado por nivel y caudal"
    
    pumping_capacity_id = fields.Many2one(comodel_name="stock.picking")
    level = fields.Char(string="Nivel")
    flow = fields.Char(string="Caudal")
    

class Dinamic_levels(models.Model):
    _name = "dinamic.level"
    _description = "niveles dinamicos de prueba de bombeo detallado por nivel y caudal"
    
    dinamic_level_id = fields.Many2one(comodel_name="stock.picking")
    flow_pb = fields.Char(string="Caudal pb")
    dinamic_level = fields.Char(string="Nivel dinámico")
                