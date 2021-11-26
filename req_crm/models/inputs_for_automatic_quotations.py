# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Lead(models.Model):
    _inherit = "crm.lead"
    
    #formulario principal
    x_servicios_requeridos = fields.Selection([('s1', 'S1'),('s2','S2'),('s1s2','S1 + S2'),('s1s2s3','S1 + S2 + S3')],string='Servicios requeridos', required=True)
    x_enviar_wsp = fields.Boolean(string='Enviar por WhatsApp')
    x_tipo_instalacion = fields.Selection([('domiciliario','Domiciliario'),('otro','Otro')],string='Tipo de instalacion')
    x_otro = fields.Char(string='otro')
    #servicio 1
    x_tipo_servicio = fields.Selection([('construccion','Construccion'),('profundizar','Profundizar')],string='Tipo de servicio')
    x_diametro = fields.Integer(string='Diametro')
    x_profundidad = fields.Integer(string='Profundidad')
    x_faena = fields.Integer(string='Instalacion de faena')
    x_valorxmt = fields.Integer(string='Valor por metro')
    x_prueba_bombeo = fields.Selection([('sinprueba','Sin Prueba de Bombeo'),('pb2hrs','Prueba de bombeo 2hrs'),('pb4hrs','Prueba de bombeo 4hrs'),('pb24hrs','Prueba de bombeo DGA 24hrs')],string='Prueba de bombeo')
    prueba_bombeo = fields.Many2one('product.template',string='Prueba de bombeo',domain=[('categ_id','=','SERVICIOS / PRUEBAS')])
    x_valorpb = fields.Integer(string='Valor prueba de bombeo')
    x_insc_dga = fields.Integer(string='Inscripcion pozo DGA')
    corona = fields.Many2one('product.template',string='Corona',domain=[('categ_id','=','OPERACIÓN PERFORACIÓN / HERRAMIENTAS PERFORACIÓN / CORONAS')])
    x_valor_corona = fields.Integer(string='Valor corona')
    x_duracion = fields.Integer(string='Duracion')
    #servicio 2
    x_caudal_fl = fields.Integer('Caudal')
    x_hp_fl = fields.Float(string='HP')
    x_bomba_crm = fields.Many2one('product.template',string='Bomba',domain=[('categ_id','in',[('OPERACIÓN BOMBEO / BOMBAS'),('OPERACIÓN BOMBEO / KITS')])])
    x_motor_crm = fields.Many2one('product.template',string='Motor',domain=[('categ_id','=','OPERACIÓN BOMBEO / MOTORES')])
    tablero = fields.Many2one('product.template',string='Tablero',domain=[('categ_id','in',[('OPERACIÓN BOMBEO / TABLEROS ELECTRICOS'),('OPERACIÓN BOMBEO / TABLEROS ELECTRICOS / MONOFASICO'),('OPERACIÓN BOMBEO / TABLEROS ELECTRICOS / TRIFASICO')])])
    x_tipo_caneria = fields.Selection([('pvc','PVC C10'),('vwell','V-WELL'),('galvanizada','Galvanizada')],string='Tipo de caneria')
    x_pul_canerias_s2 = fields.Selection([('1','1"'),('1,25','1 1/4"'),('1,5','1 1/2"'),('2','2"'),('3','3"'),('4','4"'),('5','5"'),('6','6"')],string='Pulgadas')
    x_impulsion = fields.Integer(string='Total impulsion')
    x_altura = fields.Integer(string='Altura total')
    x_voltaje = fields.Integer(string='Voltaje')
    x_valor_instalacion = fields.Integer(string='Valor Instalacion')
    x_duracion_s2 = fields.Integer(string='Duracion')
    x_valor_referencia = fields.Integer(string='Valor total referencia')
    #servicio 3
    x_estanque = fields.Selection([('1000','1000 lts'),('2000','2000 lts'),('3000','3000 lts'),('5000','5000 lts'),('10000','10000 lts'),('20000','20000 lts')],string='Capacidad estanque')
    x_superficie = fields.Boolean(string='Superficie')
    x_enterrado_s3 = fields.Boolean(string='Enterrado')
    x_bombacen_hp_fl = fields.Float(string='Bomba centrifuga HP')
    x_hidropack = fields.Boolean(string='Hidropack')
    x_controlpress = fields.Boolean(string='ControlPress')
    x_cloracion = fields.Boolean(string='Cloracion')
    x_valor_instalacion_s3 = fields.Integer(string='Valor instalacion')
    x_duracion_s3 = fields.Integer(string='Duracion')
    x_valor_referencia_s3 = fields.Integer(string='valor referencial')
    #servicio 4
    x_servicio4 = fields.Selection([('bombeoestandar','Prueba de bombeo estándar'),('bombeodga','Prueba de bombeo DGA 24hrs'),('bombeo2hrs','Prueba de bombeo 2hrs'),('bombeo4hrs','Prueba de bombeo 4hrs'),('bombeo8hrs','Prueba de bombeo 8hrs'),('analisisagua','Análisis agua'),('recargoagua','Recargo análisis agua'),('visita','	Visita técnica'),('camaravideo','Cámara video'),('limpiezamecanica','Limpieza mecánica'),('inscripciondga','Inscripción pozo DGA'),('retiroequipo','Retiro equipo existente'),('montajeequipo','Montaje equipo existente'),('instalacionfaena','Instalación de faena')],string='Servicio')
    x_precios4 = fields.Integer(string='Precio servicio')
    #servicio 5
    x_idakm = fields.Integer(string='Ida (km)')
    x_duracionhrs = fields.Integer(string='Duracion hrs trabajo')
    x_num_personas = fields.Integer(string='Num. Personas Totales')
    x_sin_camion = fields.Boolean(string='Sin camion Pluma')
    x_con_camion = fields.Boolean(string='Con camion Pluma')
    x_num_vehiculos = fields.Integer(string='Num. Vehiculo camion')
    #servicio 6
    x_mt_estimado = fields.Integer(string='Metros estimados')
    x_idakms6 = fields.Integer(string='Ida (km)')
    x_dias_s6 = fields.Integer(string='Num. dias')
    x_personas_s6 = fields.Integer(string='Num. personas')
    x_dias_s6_lim = fields.Integer(string='Num. dias')
    x_num_perforadores = fields.Integer(string='Num. Pers. perforador')
    x_num_soldadores = fields.Integer(string='Num. Pers. soldador')
    x_num_ayudantes = fields.Integer(string='Num. Pers. ayudante')
    x_dias_s6_ib = fields.Integer(string='Num. dias')
    x_num_personas_ib = fields.Integer(string='Num. personas')
    #formato de pagos
    x_abono = fields.Integer('Abono inicial (%)')
    x_abono_monto = fields.Integer(string='Abono ($)')
    x_cuotas = fields.Integer(string='Num. cuotas')
    x_comentarios = fields.Char(string='comentarios')
    
    
    
    
    
    
    