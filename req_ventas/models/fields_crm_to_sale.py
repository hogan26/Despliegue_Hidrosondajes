# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    def _get_default_enc1(self):
        result1 = """
            <div><span>- Revestimiento con cañería de acero al carbono ASTM A-53 Sch 40 negra.</span></div>\n<div><span>- La tubería estará ranurada y distribuida de acuerdo a la ubicación de las zonas aportantes.</span></div>"""
        return result1
    
    def _get_default_enc2(self):
        result2 = """
            <div><span>- Tablero de control y comando, cables y sondas.</span></div>\n<div><span>- Cañería para la instalación de la bomba y piezas especiales.</span></div>"""
        return result2
    
    def _get_default_enc3(self):
        result3 = """
            <div><span>- Transporte de equipos de perforación y apoyo logístico.</span></div>\n<div><span>- Perforación con sistema DTH de entubación simultanea.</span></div>\n<div><span>- Limpieza de pozo a través de inyección de aire comprimido.</span></div>\n<div><span>- Sello de hormigón de 50x50x30 cm.</span></div><div><span>- Pintura y tapa de pozo.</span></div>"""
        return result3
    
    def _get_default_enc4(self):
        result4 = """
            <div><span>- Instalación y levante de faenas.</span></div>\n<div><span>- Suministro e instalación de sistema de bombeo completo.</span></div>\n<div><span>- Puesta en marcha.</span></div>\n<div><span>- Informe de construcción del pozo y de la prueba de bombeo.</span></div>"""
        return result4
    
    def _get_default_enc5(self):
        result5 = """
            <div><span>- Transporte de equipos de apoyo logístico.</span></div>\n<div><span>- Instalación y levante de faenas.</span></div>\n<div><span>- Suministro e instalación de sistema de bombeo completo.</span></div>\n<div><span>- Puesta en marcha.</span></div>"""
        return result5
    
    def get_default_profundidad_calculada(self):
        if self.opportunity_id.x_profundidad:
            return self.opportunity_id.x_profundidad
        else:
            return 0
            
    #onchange de plantillas de presupuesto
    sale_order_template_id_prueba = fields.Many2one(comodel_name='sale.order.template',string='Plantilla de presupuesto',readonly=True,states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    sale_order_template_id = fields.Many2one(
        'sale.order.template', 'Quotation Template',
        readonly=True, check_company=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",invisible=True) 
    #formulario principal
    opportunity_id = fields.Many2one('crm.lead', string='Opportunity', check_company=True,domain="[('type', '=', 'opportunity'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    x_servicios_requeridos = fields.Selection(related='opportunity_id.x_servicios_requeridos', string='Servicios requeridos')
    x_enviar_wsp = fields.Boolean(related='opportunity_id.x_enviar_wsp',string='Enviar por WhatsApp')
    x_tipo_instalacion = fields.Selection(related='opportunity_id.x_tipo_instalacion',string='Tipo de instalacion')
    x_otro = fields.Char(related='opportunity_id.x_otro',string='otro')
    #servicio 1
    x_tipo_servicio = fields.Selection(related='opportunity_id.x_tipo_servicio',string='Tipo de servicio..')
    tipo_servicio = fields.Char(string='Tipo de servicio')    
    profundidad_profundizar = fields.Integer(string='Metros a profundizar: ',readonly=True)
    diametro_profundizar = fields.Integer(string='Diametro de profundización: ',readonly=True)
    caudal_estimado_profundizar = fields.Char(string='Caudal estimado: ',readonly=True)
    x_diametro_pozo = fields.Integer(related='opportunity_id.x_diametro',string='Diametro:.. ')
    diametro_pozo = fields.Char(string='Diametro: ',readonly=True,store=True)
    x_profundidad_pozo = fields.Integer(related='opportunity_id.x_profundidad',string='Profundidad.: ')
    profundidad_calculada = fields.Integer(string="Profundidad: ",default=get_default_profundidad_calculada,readonly=True,store=True)
    x_faena = fields.Integer(related='opportunity_id.x_faena',string='Instalacion de faena')
    x_valorxmt = fields.Integer(related='opportunity_id.x_valorxmt',string='Valor por metro')
    x_prueba_bombeo = fields.Selection(related='opportunity_id.x_prueba_bombeo',string='Prueba de bombeo..')
    x_valorpb = fields.Integer(related='opportunity_id.x_valorpb',string='Valor prueba de bombeo')
    x_insc_dga = fields.Integer(related='opportunity_id.x_insc_dga',string='Inscripcion pozo DGA')
    corona = fields.Many2one('product.template',related='opportunity_id.corona',string='Corona')
    x_valor_corona = fields.Integer(related='opportunity_id.x_valor_corona',string='Valor corona')
    x_duracion_s1 = fields.Integer(related='opportunity_id.x_duracion',string='Duración servicio de perforación')
    duracion_servicio1 = fields.Integer(string='Duración',store=True,readonly=True)
    prueba_bombeo = fields.Many2one('product.template',related='opportunity_id.prueba_bombeo',string='Prueba de bombeo.')
    prueba_bombeo_crm = fields.Char(string='Prueba de bombeo: ',store=True,readonly=True)
    generador = fields.Boolean(string='Req. Generador')
    #servicio 2
    x_caudal_crm = fields.Float(related='opportunity_id.x_caudal_fl',string='Caudal..: ')
    caudal_crm = fields.Float(string='Caudal.: ',store=True,readonly=True)
    caudal_text = fields.Char(string='Caudal: ',store=True,readonly=True)
    x_hp_fl = fields.Float(related='opportunity_id.x_hp_fl',string='HP')
    #hp_text = fields.Char(string='HP')
    kit_check = fields.Boolean(string='kit_check')
    kit_store = fields.Char(string='Conjunto Bomba/Motor: ',store=True,readonly=True)
    bombas_store = fields.Char(string='Bomba: ',store=True,readonly=True)
    motor_store = fields.Char(string='Motor: ',store=True,readonly=True)
    x_bomba_crm = fields.Many2one('product.template',related='opportunity_id.x_bomba_crm',string='Bomba.: ')
    x_motor_crm = fields.Many2one('product.template',related='opportunity_id.x_motor_crm',string='Motor.: ')
    tablero = fields.Many2one('product.template',related='opportunity_id.tablero',string='Tablero')
    x_tipo_caneria = fields.Selection(related='opportunity_id.x_tipo_caneria',string='Tipo de caneria')
    x_pul_canerias_s2 = fields.Selection(related='opportunity_id.x_pul_canerias_s2',string='Pulgadas')
    x_impulsion = fields.Integer(related='opportunity_id.x_impulsion',string='Total impulsion')
    x_altura = fields.Integer(related='opportunity_id.x_altura',string='Altura total')
    x_voltaje = fields.Integer(related='opportunity_id.x_voltaje',string='Voltaje')
    x_valor_instalacion = fields.Integer(related='opportunity_id.x_valor_instalacion',string='Valor Instalacion')
    x_duracion_total = fields.Integer(related='opportunity_id.x_duracion_s2',string='Duracion.')
    duracion_s2 = fields.Integer(string='Duración sistema de bombeo',readonly=True,store=True)
    x_valor_referencia = fields.Integer(related='opportunity_id.x_valor_referencia',string='Valor total referencia')
    #servicio 3
    x_estanque = fields.Selection(related='opportunity_id.x_estanque',string='Capacidad estanque')
    x_superficie = fields.Boolean(related='opportunity_id.x_superficie',string='Superficie')
    x_enterrado_s3 = fields.Boolean(related='opportunity_id.x_enterrado_s3',string='Enterrado')
    x_bombacen_hp_fl = fields.Float(related='opportunity_id.x_bombacen_hp_fl',string='Bomba centrifuga HP')
    x_hidropack = fields.Boolean(related='opportunity_id.x_hidropack',string='Hidropack')
    x_controlpress = fields.Boolean(related='opportunity_id.x_controlpress',string='Presscontrol')
    x_cloracion = fields.Boolean(related='opportunity_id.x_cloracion',string='Cloracion')
    x_valor_instalacion_s3 = fields.Integer(related='opportunity_id.x_valor_instalacion_s3',string='Valor instalacion')
    x_duracion_s3 = fields.Integer(related='opportunity_id.x_duracion_s3',string='Duracion')
    x_valor_referencia_s3 = fields.Integer(related='opportunity_id.x_valor_referencia_s3',string='valor referencial')
    #servicio 4
    x_servicio4 = fields.Selection(related='opportunity_id.x_servicio4',string='Servicio')
    x_precios4 = fields.Integer(related='opportunity_id.x_precios4',string='Precio servicio')
    caudal_esperado = fields.Float(string='Caudal esperado por el cliente')    
    #servicio 5
    x_idakm = fields.Integer(related='opportunity_id.x_idakm',string='Ida (km).')
    x_duracionhrs = fields.Integer(related='opportunity_id.x_duracionhrs',string='Duracion hrs trabajo')
    x_num_personas = fields.Integer(related='opportunity_id.x_num_personas',string='Num. Personas Totales')
    x_sin_camion = fields.Boolean(related='opportunity_id.x_sin_camion',string='Sin camion Pluma')
    x_con_camion = fields.Boolean(related='opportunity_id.x_con_camion',string='Con camion Pluma')
    x_num_vehiculos = fields.Integer(related='opportunity_id.x_num_vehiculos',string='Num. Vehiculo camion')
    #servicio 6
    x_mt_estimado = fields.Integer(related='opportunity_id.x_mt_estimado',string='Metros estimados')
    x_idakms6 = fields.Integer(related='opportunity_id.x_idakms6',string='Ida (km)')
    x_dias_s6 = fields.Integer(related='opportunity_id.x_dias_s6',string='Num. dias..')
    x_personas_s6 = fields.Integer(related='opportunity_id.x_personas_s6',string='Num. personas.')
    x_dias_s6_lim = fields.Integer(related='opportunity_id.x_dias_s6_lim',string='Num. dias.')
    x_num_perforadores = fields.Integer(related='opportunity_id.x_num_perforadores',string='Num. Pers. perforador')
    x_num_soldadores = fields.Integer(related='opportunity_id.x_num_soldadores',string='Num. Pers. soldador')
    x_num_ayudantes = fields.Integer(related='opportunity_id.x_num_ayudantes',string='Num. Pers. ayudante')
    x_dias_s6_ib = fields.Integer(related='opportunity_id.x_dias_s6_ib',string='Num. dias')
    x_num_personas_ib = fields.Integer(related='opportunity_id.x_num_personas_ib',string='Num. personas')
    # campos de acuerdos de pago antiguos
    x_abono_crm = fields.Integer(related='opportunity_id.x_abono',string='Abono (%)')
    x_abono_m_crm = fields.Integer(related='opportunity_id.x_abono_monto',string='Abono ($).')
    x_cuotas_crm = fields.Integer(related='opportunity_id.x_cuotas',string='Num. cuotas.')
    x_comentarios = fields.Char(string='Comentarios',related='opportunity_id.x_comentarios')    
    # campos de acuerdos de pago nuevos
    abono_porcentaje = fields.Integer(string='Abono inicial (%)',readonly=True)
    abono_monto = fields.Integer(string='Abono ($)',readonly=True)
    descuento_iva = fields.Integer(string='Descuento IVA',readonly=True)
    descuento_neto_porcentaje = fields.Integer(string='Descuento neto (%)',readonly=True)
    descuento_neto_monto = fields.Integer(string='Descuento neto ($)',readonly=True)
    num_cuotas = fields.Integer(string='Num. cuotas',readonly=True)
    observaciones = fields.Char(string='Observaciones',readonly=False)  
    observacion_s1 = fields.Char(string='observacion_s1_bomba',default='- Este servicio no incluye bomba de pozo.')
    observacion_s2 = fields.Char(string='observacion_s1_tablero',default='- Este servicio considera la instalación del tablero de control a 1 metro de distancia del pozo.')
    
    x_encabezado_coti1 = fields.Html(string='encabezado coti 1',default = _get_default_enc1)
    x_encabezado_coti2 = fields.Html(string='encabezado coti 2',default = _get_default_enc2)
    x_encabezado_coti3 = fields.Html(string='encabezado coti 3',default = _get_default_enc3)
    x_encabezado_coti4 = fields.Html(string='encabezado coti 4',default = _get_default_enc4)
    x_encabezado_coti5 = fields.Html(string='encabezado coti 5',default = _get_default_enc5)
    x_encabezado_coti_s4 = fields.Html(string='encabezado coti s4')
    encabezado_s3_descripcion = fields.Html(string='encabezado coti s3 descripcion')
    encabezado_s3_obra = fields.Html(string='encabezado coti s3 obra')
    
    @api.onchange('sale_order_template_id_prueba')
    def onchange_sale_order_template_id_prueba(self):
        #_logger.info('entra exitosamente - metodo en req_ventas')
        if not self.sale_order_template_id_prueba:
            self.require_signature = self._get_default_require_signature()
            self.require_payment = self._get_default_require_payment()
            return
        template = self.sale_order_template_id_prueba.with_context(lang=self.partner_id.lang)
        
        #ACUERDOS DE PAGO
        
        for acuerdo in self.opportunity_id.payment_agreed_matriz_ids:
            if acuerdo.fijar_ac:
                self.update({'abono_porcentaje':acuerdo.Abono_porcentaje})
                self.update({'abono_monto':acuerdo.Abono_monto})
                self.update({'descuento_iva':acuerdo.descuento_iva})
                self.update({'descuento_neto_porcentaje':acuerdo.descuento_neto_porcentaje})
                self.update({'descuento_neto_monto':acuerdo.descuento_neto_monto})
                self.update({'num_cuotas':acuerdo.num_cuotas})
                self.update({'observaciones':acuerdo.comentarios})
        
        # CARGA DE INFORMACION PARA COTIZACIONES        
        diametros = []
        if not(self.opportunity_id.x_profundidad):
            calculo_profundidad = self.opportunity_id        
            profundidad = self.profundidad_calculada
            for suma in calculo_profundidad.lead_matriz_lines_ids:
                if suma.tipo_servicio_perforacion.categ_id.display_name == 'SERVICIOS / PERFORACION':
                    profundidad = profundidad + suma.cantidad_metros
                    if not(self.opportunity_id.x_diametro):
                        if suma.tipo_servicio_perforacion.display_name.rfind('5') != -1:
                            diametros.append(5)
                        if suma.tipo_servicio_perforacion.display_name.rfind('6') != -1:
                            diametros.append(6)
                        if suma.tipo_servicio_perforacion.display_name.rfind('8') != -1:
                            diametros.append(8)
                        if suma.tipo_servicio_perforacion.display_name.rfind('10') != -1:
                            diametros.append(10)
                        if suma.tipo_servicio_perforacion.display_name.rfind('12') != -1:
                            diametros.append(12)
            
            diametro_tapa = ''
            if len(diametros)>1:                
                encabezado_diametro = ''
                aux = 0
                for calculo_diametro in diametros:  
                    _logger.info('tipo de dato: {}'.format(type(calculo_diametro)))                    
                    if aux == 0:
                        encabezado_diametro = str(calculo_diametro)                        
                        aux = aux + 1
                    else:
                        encabezado_diametro = encabezado_diametro + ' y ' + str(calculo_diametro) + ' Pulgadas'
            else:
                encabezado_diametro = ''                
                for calculo_diametro in diametros:                
                    diametro_tapa = str(calculo_diametro)
                    encabezado_diametro = str(calculo_diametro) + ' Pulgadas'                       
            
            if self.opportunity_id.kits:                
                search_kit = self.env['product.product'].search([('name','=',self.opportunity_id.kits.name)])
                search_kit = search_kit.name.lower()
            else:
                search_kit = ''
                
            if self.opportunity_id.bomba_crm:                
                search_bomba = self.env['product.product'].search([('name','=',self.opportunity_id.bomba_crm.name)])
                search_bomba = search_bomba.name.lower()
            else:
                search_bomba = ''
                
            if self.opportunity_id.motor_crm:                
                search_motor = self.env['product.product'].search([('name','=',self.opportunity_id.motor_crm.name)])
                search_motor = search_motor.name.lower()
            else:
                search_motor = ''            
                
            if self.opportunity_id.kit_check:
                self.update({'kit_check':True})
            else:
                self.update({'kit_check':False})
                
            if self.opportunity_id.prueba_bombeo_crm:                
                search_pbb = self.env['product.product'].search([('name','=',self.opportunity_id.prueba_bombeo_crm.name)])
                search_pbb = search_pbb.name.lower()
            else:
                search_pbb = ''            
            
            self.update({'profundidad_calculada':profundidad})
            self.update({'diametro_pozo':encabezado_diametro})
            self.update({'duracion_servicio1':self.opportunity_id.duracion_s1})
            self.update({'caudal_crm':self.opportunity_id.caudal_crm})                        
            self.update({'caudal_text':self.opportunity_id.caudal_text})
            self.update({'kit_store':search_kit})
            self.update({'bombas_store':search_bomba})
            self.update({'motor_store':search_motor})
            self.update({'duracion_s2':self.opportunity_id.duracion_s2})
            self.update({'prueba_bombeo_crm':search_pbb})
            self.update({'tipo_servicio':self.opportunity_id.x_tipo_servicio})
            
            if self.opportunity_id.generador:
                self.update({'generador':True})
            else:
                self.update({'generador':False})
            
            if self.opportunity_id.x_tipo_servicio in ['profundizar']:
                self.update({'profundidad_profundizar':self.opportunity_id.profundidad_profundizar})
                self.update({'diametro_profundizar':self.opportunity_id.diametro_profundizar})
                self.update({'caudal_estimado_profundizar':self.opportunity_id.caudal_estimado_profundizar})
                
            if self.opportunity_id.caudal_esperado_check:
                self.update({'caudal_esperado':self.opportunity_id.caudal_esperado})
                
        
        tuberia_medida = self.opportunity_id.x_pul_canerias_s2
        if tuberia_medida == '1':
            tuberia_medida_mm = '32'
            tuberia_medida_vwell = '25'
            terminal_medida_pvc = '32 x 1" CEMENTAR'
            adaptador_medida = '25MM (1")'
            llave_bola = 'LLAVE DE BOLA PASO CONTINUO 1"'
            union_americana = 'UNION AMERICANA PVC 32MM CEMENTAR'
            codo_hi_galva = 'CODO HI GALVA. 1"'
            tuberia_pvc_vwell = 'TUBERIA PVC 32X6000MM PN10'
            terminal_he_pvc_vwell = 'TERMINAL HE PVC 32 x 1" CEMENTAR'            
        
        if tuberia_medida == '1,25':
            tuberia_medida_mm = '40'
            tuberia_medida_vwell = '32MM (1 1/4")'
            terminal_medida_pvc = '40 x 1 1/4" CEMENTAR'
            adaptador_medida = '32MM (1 1/4")'
            llave_bola = 'LLAVE DE BOLA PASO CONTINUO 1 1/4"'
            union_americana = 'UNION AMERICANA PVC 40MM CEMENTAR'
            codo_hi_galva = 'CODO HI GALVA. 1 1/4"'
            tuberia_pvc_vwell = 'TUBERIA PVC 40X6000MM PN10'
            terminal_he_pvc_vwell = 'TERMINAL HE PVC 40 x 1 1/4" CEMENTAR'
            
        if tuberia_medida == '1,5':
            tuberia_medida_mm = '50'
            tuberia_medida_vwell = '40MM (1 1/2")'
            terminal_medida_pvc = '50 x 1 1/2" CEMENTAR'
            adaptador_medida = '40MM (1 1/2")'
            llave_bola = 'LLAVE DE BOLA PASO CONTINUO 1 1/2"'
            union_americana = 'UNION AMERICANA PVC 50MM CEMENTAR'
            codo_hi_galva = 'CODO HI GALVA. 1 1/2"'
            tuberia_pvc_vwell = 'TUBERIA PVC 50X6000MM PN10'
            terminal_he_pvc_vwell = 'TERMINAL HE PVC 50 x 1 1/2" CEMENTAR'
            
        if tuberia_medida == '2':
            tuberia_medida_mm = '63'
            tuberia_medida_vwell = '50MM (2")'
            terminal_medida_pvc = '63 x 2" CEMENTAR'
            adaptador_medida = '50MM (2")'
            llave_bola = 'LLAVE DE BOLA PASO CONTINUO 2"'
            union_americana = 'UNION AMERICANA PVC 63MM CEMENTAR'
            codo_hi_galva = 'CODO HI GALVA. 2"'
            tuberia_pvc_vwell = 'TUBERIA PVC 63X6000MM PN10'
            terminal_he_pvc_vwell = 'TERMINAL HE PVC 63 x 2" CEMENTAR'
            
        if tuberia_medida == '3':
            tuberia_medida_mm = '90'
            tuberia_medida_vwell = '75MM (3")'
            terminal_medida_pvc = '90 x 3" CEMENTAR'
            adaptador_medida = '75MM (3")'
            llave_bola = 'LLAVE DE BOLA PASO CONTINUO 3"'
            union_americana = 'UNION AMERICANA PVC 90MM CEMENTAR'
            codo_hi_galva = 'CODO HI GALVA. 3"'
            flange_hi_acero = 'FLANGE HI ACERO 3" BSP DIN'
            curva_brida_brida_acero = 'CURVA BRIDA BRIDA ACERO 3"'
            valvula_elastoamerica = 'VALVULA ELASTOAMERICA 3"'
            goma_brida = 'GOMA BRIDA 3"'
            copla_hi_galva = 'COPLA HI GALVA. 3" BSP'
            
        if tuberia_medida == '4':
            tuberia_medida_mm = '110'
            tuberia_medida_vwell = '100MM (4")'
            terminal_medida_pvc = '110 x 4" CEMENTAR'
            adaptador_medida = '100MM (4")'
            llave_bola = 'LLAVE DE BOLA PASO CONTINUO 4"'
            union_americana = 'UNION AMERICANA PVC 110MM CEMENTAR'
            codo_hi_galva = 'CODO HI GALVA. 4"'
            flange_hi_acero = 'FLANGE HI ACERO 4" BSP DIN'
            curva_brida_brida_acero = 'CURVA BRIDA BRIDA ACERO 4"'
            valvula_elastoamerica = 'VALVULA ELASTOAMERICA 4"'
            goma_brida = 'GOMA BRIDA 4"'
            copla_hi_galva = 'COPLA HI GALVA. 4" BSP'
            
        if tuberia_medida == '5':
            tuberia_medida_mm = '140'
            tuberia_medida_vwell = '125MM (5")'
            terminal_medida_pvc = '140 x 5" CEMENTAR'
            adaptador_medida = '125MM (5")'
            llave_bola = 'LLAVE DE BOLA PASO CONTINUO 5"'
            union_americana = 'UNION AMERICANA PVC 140MM CEMENTAR'
            codo_hi_galva = 'CODO HI GALVA. 5"'
            flange_hi_acero = 'FLANGE HI ACERO 5" BSP DIN'
            curva_brida_brida_acero = 'CURVA BRIDA BRIDA ACERO 5"'
            valvula_elastoamerica = 'VALVULA ELASTOAMERICA 5"'
            goma_brida = 'GOMA BRIDA 5"'
            copla_hi_galva = 'COPLA HI GALVA. 5" BSP'
            
        if tuberia_medida == '6':
            tuberia_medida_mm = '160'
            tuberia_medida_vwell = '150MM (6")'
            terminal_medida_pvc = '160 x 6" CEMENTAR'
            adaptador_medida = '150MM (6")'
            llave_bola = 'LLAVE DE BOLA PASO CONTINUO 6"'
            union_americana = 'UNION AMERICANA PVC 160MM CEMENTAR'
            codo_hi_galva = 'CODO HI GALVA. 6"'
            flange_hi_acero = 'FLANGE HI ACERO 6" BSP DIN'
            curva_brida_brida_acero = 'CURVA BRIDA BRIDA ACERO 6"'
            valvula_elastoamerica = 'VALVULA ELASTOAMERICA 6"'
            goma_brida = 'GOMA BRIDA 6"'
            copla_hi_galva = 'COPLA HI GALVA. 6" BSP'
            
            
        order_lines = [(5, 0, 0)]
        for line in template.sale_order_template_line_ids:
            #_logger.info('line_id= {}'.format(line.id))
            data = self._compute_line_data_for_template_change(line)
            if line.product_id:
                discount = 0
                """
                if self.pricelist_id:
                    price = self.pricelist_id.with_context(uom=line.product_uom_id.id).get_product_price(line.product_id, 1, False)
                    if self.pricelist_id.discount_policy == 'without_discount' and line.price_unit:
                        discount = (line.price_unit - price) / line.price_unit * 100
                        # negative discounts (= surcharge) are included in the display price
                        if discount < 0:
                            discount = 0
                        else:
                            price = line.price_unit
                    elif line.price_unit:
                        price = line.price_unit

                else:
                    price = line.price_unit
                """    
                price = line.product_id.product_tmpl_id.list_price        
                #validacion si la plantilla que se esta cargando corresponde a un presupuesto o una orden de trabajo
                if self.opportunity_id:                    
                    entra_categoria=0
                    seleccionado=0
                    #_logger.info('diametro= {}'.format(diametro))
                    #_logger.info('categoria= {}'.format(line.product_id.product_tmpl_id.categ_id.display_name))
                    _logger.info('product_id= {}'.format(line.product_id.product_tmpl_id.id))
                    matriz = self.opportunity_id
                    if line.product_id.product_tmpl_id.categ_id.display_name in [('SERVICIOS / PERFORACION'),('SERVICIOS / ENTUBACION')]:
                        entra_categoria=1
                        for matriz_perforacion in matriz.lead_matriz_lines_ids:
                            #_logger.info('matriz_perforacion= {}'.format(matriz_perforacion))
                                
                            if matriz_perforacion.tipo_servicio_perforacion.id == line.product_id.product_tmpl_id.id:
                                data.update({
                                    'name': matriz_perforacion.tipo_servicio_perforacion.name,
                                    'price_unit': matriz_perforacion.valor_metro,
                                    'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                    'product_uom_qty': matriz_perforacion.cantidad_metros,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                    'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                    'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,
                                    'utilidad_porcentaje': 0,                            
                                })                        
                                if self.pricelist_id:
                                    data.update(self.env['sale.order.line']._get_purchase_price(
                                        self.pricelist_id, 
                                        line.product_id, 
                                        line.product_uom_id, 
                                        fields.Date.context_today(self)))

                                    order_lines.append((0, 0, data))                    
                                    seleccionado=1                        

                    if line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN PERFORACIÓN / HERRAMIENTAS PERFORACIÓN / CORONAS':
                        entra_categoria=1
                        for matriz_corona in matriz.corona_matriz_lines_ids:
                            #_logger.info('matriz_corona= {}'.format(matriz_corona))
                            if matriz_corona.corona.id == line.product_id.product_tmpl_id.id:
                                #_logger.info('corona crm= {}'.format(self.opportunity_id.corona.id))
                                #_logger.info('corona plantilla= {}'.format(line.product_id.product_tmpl_id.id))
                                data.update({
                                    'price_unit': matriz_corona.precio,
                                    'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                    'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                    'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,
                                    'utilidad_porcentaje': 0,
                                })                        
                                if self.pricelist_id:
                                    data.update(self.env['sale.order.line']._get_purchase_price(
                                        self.pricelist_id, 
                                        line.product_id, 
                                        line.product_uom_id, 
                                        fields.Date.context_today(self)))

                                order_lines.append((0, 0, data))  
                                seleccionado=1

                    if line.product_id.product_tmpl_id.categ_id.display_name == 'SERVICIOS / PRUEBAS' and self.opportunity_id.x_servicios_requeridos != 's4':
                        entra_categoria=1
                        if self.opportunity_id.prueba_bombeo_crm.id == line.product_id.product_tmpl_id.id:
                            #comprueba si es una prueba de combeo DGA
                            if line.product_id.product_tmpl_id.id == 551:
                                data.update({
                                    'price_unit': self.opportunity_id.x_insc_dga,
                                    'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                    'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                    'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,
                                    'utilidad_porcentaje': 0,
                                })
                            else:
                                data.update({
                                    'price_unit': self.opportunity_id.x_valorpb,
                                    'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                    'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                    'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,
                                    'utilidad_porcentaje': 0,
                                })

                            if line.product_id.product_tmpl_id.id != 2211:    
                                if self.pricelist_id:
                                    data.update(self.env['sale.order.line']._get_purchase_price(
                                        self.pricelist_id, 
                                        line.product_id, 
                                        line.product_uom_id, 
                                        fields.Date.context_today(self)))

                                order_lines.append((0, 0, data)) 
                                seleccionado=1

                    if line.product_id.product_tmpl_id.categ_id.display_name == 'SERVICIOS' and self.opportunity_id.x_servicios_requeridos != 's4':
                        entra_categoria=1
                        if line.product_id.product_tmpl_id.id == 546:                        
                            data.update({
                                'price_unit': self.opportunity_id.x_faena + self.opportunity_id.retiro_material,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,
                                'utilidad_porcentaje': 0,
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id, 
                                    line.product_id, 
                                    line.product_uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1

                        if line.product_id.product_tmpl_id.id == 1521:                        
                            data.update({
                                'price_unit': self.opportunity_id.x_valor_instalacion,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,
                                'utilidad_porcentaje': 0,
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id, 
                                    line.product_id, 
                                    line.product_uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1

                    if line.name == 'REFERENCIA POSICIONAL KIT':
                        entra_categoria=1
                        if self.opportunity_id.kit_check:
                            if self.opportunity_id.kits:
                                data.update({
                                    'name':self.opportunity_id.kits.name,
                                    'price_unit': self.opportunity_id.kits.list_price,
                                    'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': self.opportunity_id.kits.id,
                                    'product_uom': self.opportunity_id.kits.uom_id.id,
                                    'customer_lead': self._get_customer_lead(self.opportunity_id.kits),
                                    'last_update_price_date': self.opportunity_id.kits.last_update_pricelist_date,
                                    'last_update_price_partner': self.opportunity_id.kits.last_update_pricelist_partner,
                                })                        
                                if self.pricelist_id:
                                    data.update(self.env['sale.order.line']._get_purchase_price(
                                        self.opportunity_id.kits.list_price, 
                                        self.opportunity_id.kits.id, 
                                        self.opportunity_id.kits.uom_id.id, 
                                        fields.Date.context_today(self)))

                                order_lines.append((0, 0, data))
                                seleccionado=1  
                            
                         
                    if line.name == 'REFERENCIA POSICIONAL BOMBA POZO':
                        entra_categoria=1
                        bomba_pozo = self.env['product.product'].search([('name','=',self.opportunity_id.bomba_crm.name)])
                        if not(self.opportunity_id.kit_check):
                            if self.opportunity_id.bomba_crm:
                                data.update({
                                    'name': bomba_pozo.name,
                                    'price_unit': bomba_pozo.list_price,
                                    'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': bomba_pozo.id,
                                    'product_uom': bomba_pozo.uom_id.id,
                                    'customer_lead': self._get_customer_lead(bomba_pozo),
                                    'last_update_price_date': bomba_pozo.last_update_pricelist_date,
                                    'last_update_price_partner': bomba_pozo.last_update_pricelist_partner,
                                })                        
                                if self.pricelist_id:
                                    data.update(self.env['sale.order.line']._get_purchase_price(
                                        bomba_pozo.list_price, 
                                        bomba_pozo.id, 
                                        bomba_pozo.uom_id.id, 
                                        fields.Date.context_today(self)))

                                order_lines.append((0, 0, data))
                                seleccionado=1
                            
                    if line.name == 'REFERENCIA POSICIONAL MOTOR':
                        entra_categoria=1
                        motor = self.env['product.product'].search([('name','=',self.opportunity_id.motor_crm.name)])                        
                        if not(self.opportunity_id.kit_check):
                            if self.opportunity_id.motor_crm:
                                data.update({
                                    'name': motor.name,
                                    'price_unit': motor.list_price,
                                    'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': motor.id,
                                    'product_uom': motor.uom_id.id,
                                    'customer_lead': self._get_customer_lead(motor),
                                    'last_update_price_date': motor.last_update_pricelist_date,
                                    'last_update_price_partner': motor.last_update_pricelist_partner,
                                })                        
                                if self.pricelist_id:
                                    data.update(self.env['sale.order.line']._get_purchase_price(
                                        motor.list_price, 
                                        motor.id, 
                                        motor.uom_id.id, 
                                        fields.Date.context_today(self)))

                                order_lines.append((0, 0, data))
                                seleccionado=1 
                            
                    if line.name == 'REFERENCIA POSICIONAL TUBERIA PVC': 
                        entra_categoria=1                        
                        if self.opportunity_id.x_tipo_caneria in ['pvc']:                        
                            tuberia_name = 'TUBERIA PVC '+tuberia_medida_mm+'X6000MM PN10'                        
                            tuberia_pvc = self.env['product.product'].search([('name','=',tuberia_name)])                       

                            data.update({
                                'name': tuberia_pvc.name,
                                'price_unit': tuberia_pvc.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': self.opportunity_id.x_impulsion,
                                'product_id': tuberia_pvc.id,
                                'product_uom': tuberia_pvc.uom_id.id,
                                'customer_lead': self._get_customer_lead(tuberia_pvc),
                                'last_update_price_date': tuberia_pvc.last_update_pricelist_date,
                                'last_update_price_partner': tuberia_pvc.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    tuberia_pvc.pricelist_id, 
                                    tuberia_pvc.id, 
                                    tuberia_pvc.uom_id.id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                    
                    if line.name == 'REFERENCIA POSICIONAL TUBERIA V-WELL': 
                        entra_categoria=1                        
                        if self.opportunity_id.x_tipo_caneria in ['vwell']:                        
                            tuberia_name = 'TUBERIA V-WELL '+tuberia_medida_vwell
                            tuberia_vwell = self.env['product.product'].search([('name','=',tuberia_name)])

                            if self.opportunity_id.x_impulsion%3>0:
                                calc_impulsion = round((self.opportunity_id.x_impulsion/3)+0.5)
                            else:
                                calc_impulsion = round(self.opportunity_id.x_impulsion/3)

                            data.update({
                                'name': tuberia_vwell.name,
                                'price_unit': tuberia_vwell.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': calc_impulsion,
                                'product_id': tuberia_vwell.id,
                                'product_uom': tuberia_vwell.uom_id.id,
                                'customer_lead': self._get_customer_lead(tuberia_vwell),
                                'last_update_price_date': tuberia_vwell.last_update_pricelist_date,
                                'last_update_price_partner': tuberia_vwell.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    tuberia_vwell.pricelist_id, 
                                    tuberia_vwell.id, 
                                    tuberia_vwell.uom_id.id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                    
                    if line.name == 'REFERENCIA POSICIONAL TERMINAL HI PVC':
                        entra_categoria=1
                        if self.opportunity_id.x_tipo_caneria in ['pvc']:                            
                    
                            terminal_hi_name = 'TERMINAL HI PVC '+terminal_medida_pvc
                            _logger.info('terminal_hi_name= {}'.format(terminal_hi_name))
                            terminal_hi_pvc = self.env['product.product'].search([('name','=',terminal_hi_name)])
                            
                            if self.opportunity_id.x_impulsion%6>0:
                                cant_terminales = round((self.opportunity_id.x_impulsion/6)+0.5)
                            else:
                                cant_terminales = round(self.opportunity_id.x_impulsion/6)

                            data.update({
                                'name': terminal_hi_pvc.name,
                                'price_unit': terminal_hi_pvc.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': cant_terminales,
                                'product_id': terminal_hi_pvc.id,
                                'product_uom': terminal_hi_pvc.uom_id.id,
                                'customer_lead': self._get_customer_lead(terminal_hi_pvc),
                                'last_update_price_date': terminal_hi_pvc.last_update_pricelist_date,
                                'last_update_price_partner': terminal_hi_pvc.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    terminal_hi_pvc.pricelist_id, 
                                    terminal_hi_pvc.id, 
                                    terminal_hi_pvc.uom_id.id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                    
                    
                    if line.name == 'REFERENCIA POSICIONAL TERMINAL HE PVC':
                        entra_categoria=1
                        if self.opportunity_id.x_tipo_caneria in ['pvc']:                            
                    
                            terminal_he_name = 'TERMINAL HE PVC '+terminal_medida_pvc
                            terminal_he_pvc = self.env['product.product'].search([('name','=',terminal_he_name)])
                            
                            if self.opportunity_id.x_impulsion%6>0:
                                cant_terminales = round((self.opportunity_id.x_impulsion/6)+0.5)
                            else:
                                cant_terminales = round(self.opportunity_id.x_impulsion/6)

                            data.update({
                                'name': terminal_he_pvc.name, 
                                'price_unit': terminal_he_pvc.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': cant_terminales,
                                'product_id': terminal_he_pvc.id,
                                'product_uom': terminal_he_pvc.uom_id.id,
                                'customer_lead': self._get_customer_lead(terminal_he_pvc),
                                'last_update_price_date': terminal_he_pvc.last_update_pricelist_date,
                                'last_update_price_partner': terminal_he_pvc.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    terminal_he_pvc.pricelist_id, 
                                    terminal_he_pvc.id, 
                                    terminal_he_pvc.uom_id.id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                            
                    if line.name == 'REFERENCIA POSICIONAL ADAPTADOR SUP':
                        entra_categoria=1
                        if self.opportunity_id.x_tipo_caneria in ['vwell']:                            
                    
                            adaptador_sup_name = 'ADAPTADOR SUP V-WELL '+adaptador_medida
                            adaptador_sup_vwell = self.env['product.product'].search([('name','=',adaptador_sup_name)])
                            
                            data.update({
                                'name': adaptador_sup_vwell.name,
                                'price_unit': adaptador_sup_vwell.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': 1,
                                'product_id': adaptador_sup_vwell.id,
                                'product_uom': adaptador_sup_vwell.uom_id.id,
                                'customer_lead': self._get_customer_lead(adaptador_sup_vwell),
                                'last_update_price_date': adaptador_sup_vwell.last_update_pricelist_date,
                                'last_update_price_partner': adaptador_sup_vwell.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    adaptador_sup_vwell.pricelist_id, 
                                    adaptador_sup_vwell.id, 
                                    adaptador_sup_vwell.uom_id.id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                            
                    if line.name == 'REFERENCIA POSICIONAL ADAPTADOR INF':
                        entra_categoria=1
                        if self.opportunity_id.x_tipo_caneria in ['vwell']:                            
                    
                            adaptador_inf_name = 'ADAPTADOR INF V-WELL '+adaptador_medida
                            adaptador_inf_vwell = self.env['product.product'].search([('name','=',adaptador_inf_name)])
                            
                            data.update({
                                'name': adaptador_inf_vwell.name,
                                'price_unit': adaptador_inf_vwell.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': 1,
                                'product_id': adaptador_inf_vwell.id,
                                'product_uom': adaptador_inf_vwell.uom_id.id,
                                'customer_lead': self._get_customer_lead(adaptador_inf_vwell),
                                'last_update_price_date': adaptador_inf_vwell.last_update_pricelist_date,
                                'last_update_price_partner': adaptador_inf_vwell.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    adaptador_inf_vwell.pricelist_id, 
                                    adaptador_inf_vwell.id, 
                                    adaptador_inf_vwell.uom_id.id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                            
                    if line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TUBOS Y CAÑERIAS / CONDUIT' and line.product_id.product_tmpl_id.id == 1573:                        
                        data.update({
                            'price_unit': price,
                            'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                            'product_uom_qty': self.opportunity_id.x_impulsion,
                            'product_id': line.product_id.id,
                            'product_uom': line.product_uom_id.id,
                            'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                            'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                            'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                            
                        })                        
                        if self.pricelist_id:
                            data.update(self.env['sale.order.line']._get_purchase_price(
                                self.pricelist_id, 
                                line.product_id, 
                                line.product_uom_id, 
                                fields.Date.context_today(self)))

                        order_lines.append((0, 0, data))
                        seleccionado=1
                            
                    if line.product_id.product_tmpl_id.id == 535:    #CUERDA DE POLIPROPILENO                     
                        data.update({
                            'price_unit': price,
                            'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                            'product_uom_qty': self.opportunity_id.x_impulsion,
                            'product_id': line.product_id.id,
                            'product_uom': line.product_uom_id.id,
                            'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                            'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                            'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                            
                        })                        
                        if self.pricelist_id:
                            data.update(self.env['sale.order.line']._get_purchase_price(
                                self.pricelist_id, 
                                line.product_id, 
                                line.product_uom_id, 
                                fields.Date.context_today(self)))

                        order_lines.append((0, 0, data))
                        seleccionado=1  
                        
                    if line.name == 'REFERENCIA POSICIONAL TABLERO ELECTRICO':
                        entra_categoria=1
                        
                        tablero_electrico = self.env['product.product'].search([('name','=',self.opportunity_id.tablero.name)])
                                                
                        data.update({
                            'name': tablero_electrico.name,
                            'price_unit': tablero_electrico.list_price,
                            'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                            'product_uom_qty': line.product_uom_qty,
                            'product_id': tablero_electrico.id,
                            'product_uom': tablero_electrico.uom_id.id,
                            'customer_lead': self._get_customer_lead(tablero_electrico),
                            'last_update_price_date': tablero_electrico.last_update_pricelist_date,
                            'last_update_price_partner': tablero_electrico.last_update_pricelist_partner,                            
                        })                        
                        if self.pricelist_id:
                            data.update(self.env['sale.order.line']._get_purchase_price(
                                tablero_electrico.pricelist_id, 
                                tablero_electrico.id, 
                                tablero_electrico.uom_id, 
                                fields.Date.context_today(self)))

                        order_lines.append((0, 0, data))                        
                        seleccionado=1


                    if line.product_id.product_tmpl_id.categ_id.display_name == 'HERRAMIENTAS Y EQUIPOS / INSUMOS ELECTRICOS / CORDONES Y CABLES' and (line.product_id.product_tmpl_id.id == 498 or line.product_id.product_tmpl_id.id == 56 or line.product_id.product_tmpl_id.id == 497 or line.product_id.product_tmpl_id.id == 495 or line.product_id.product_tmpl_id.id == 496 or line.product_id.product_tmpl_id.id == 2352 or line.product_id.product_tmpl_id.id == 2353):  #CABLES PLANOS SUMERGIBLES
                        entra_categoria=1                        
                            
                        if self.opportunity_id.hp_text:                            
                            if self.opportunity_id.hp_text.find(',')!=-1:                            
                                hp_motor = float(self.opportunity_id.hp_text.replace(',','.'))                                
                            else:
                                hp_motor = float(self.opportunity_id.hp_text)
                        else:
                            hp_motor = self.opportunity_id.x_hp_fl

                        if hp_motor <= 7.5 and line.product_id.product_tmpl_id.id == 495:                            
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': self.opportunity_id.x_impulsion+5,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                         
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id, 
                                    line.product_id, 
                                    line.product_uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1

                        if hp_motor > 7.5 and hp_motor < 30 and line.product_id.product_tmpl_id.id == 56:                            
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': (self.opportunity_id.x_altura*2)+5,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                         
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id, 
                                    line.product_id, 
                                    line.product_uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1

                        if hp_motor >= 30 and hp_motor < 50 and line.product_id.product_tmpl_id.id == 496:                            
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': (self.opportunity_id.x_altura*2)+5,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                         
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id, 
                                    line.product_id, 
                                    line.product_uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1

                        if hp_motor >= 50 and hp_motor < 75 and line.product_id.product_tmpl_id.id == 497:                            
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': (self.opportunity_id.x_altura*2)+5,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                         
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id, 
                                    line.product_id, 
                                    line.product_uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1

                        if hp_motor >= 75 and hp_motor < 100 and (line.product_id.product_tmpl_id.id == 498 or line.product_id.product_tmpl_id.id == 2352):                            
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': (self.opportunity_id.x_altura*2)+5,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                         
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id, 
                                    line.product_id, 
                                    line.product_uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1

                        if hp_motor >= 100 and line.product_id.product_tmpl_id.id == 2353:                            
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': (self.opportunity_id.x_altura*2)+5,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                         
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id, 
                                    line.product_id, 
                                    line.product_uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1

                    if line.product_id.product_tmpl_id.categ_id.display_name == 'HERRAMIENTAS Y EQUIPOS / INSUMOS ELECTRICOS / CORDONES Y CABLES' and line.product_id.product_tmpl_id.id == 55:    #CABLE SONDA                     
                        data.update({
                            'price_unit': price,
                            'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                            'product_uom_qty': (self.opportunity_id.x_impulsion+5)*2,
                            'product_id': line.product_id.id,
                            'product_uom': line.product_uom_id.id,
                            'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                            'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                            'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                            
                        })                        
                        if self.pricelist_id:
                            data.update(self.env['sale.order.line']._get_purchase_price(
                                self.pricelist_id, 
                                line.product_id, 
                                line.product_uom_id, 
                                fields.Date.context_today(self)))

                        order_lines.append((0, 0, data))
                        seleccionado=1
                        
                    if line.product_id.product_tmpl_id.id == 51:    #mufa resina m11
                        
                        if self.opportunity_id.hp_text:                            
                            if self.opportunity_id.hp_text.find(',')!=-1:                            
                                hp_motor = float(self.opportunity_id.hp_text.replace(',','.'))                                
                            else:
                                hp_motor = float(self.opportunity_id.hp_text)
                        else:
                            hp_motor = self.opportunity_id.x_hp_fl
                        
                        
                        if hp_motor > 7.5:
                            #_logger.info('entra al if------hp_motor = {}'.format(hp_motor))
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': 2,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id, 
                                    line.product_id, 
                                    line.product_uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                                                
                        
                    if line.name == 'REFERENCIA POSICIONAL LLAVE DE BOLA':
                        entra_categoria=1
                        if self.opportunity_id.x_tipo_caneria in ['pvc']:
                            
                            llave_bola_object = self.env['product.product'].search([('name','=',llave_bola)])

                            data.update({
                                'name': llave_bola_object.name,
                                'price_unit': llave_bola_object.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': llave_bola_object.id,
                                'product_uom': llave_bola_object.uom_id.id,
                                'customer_lead': self._get_customer_lead(llave_bola_object),
                                'last_update_price_date': llave_bola_object.last_update_pricelist_date,
                                'last_update_price_partner': llave_bola_object.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    llave_bola_object.pricelist_id, 
                                    llave_bola_object.id, 
                                    llave_bola_object.uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))                        
                            seleccionado=1
                        
                        if self.opportunity_id.x_tipo_caneria in ['vwell'] and self.opportunity_id.x_pul_canerias_s2 in ['1','1,25','1,5','2']:
                            
                            llave_bola_object = self.env['product.product'].search([('name','=',llave_bola)])

                            data.update({
                                'name': llave_bola_object.name,
                                'price_unit': llave_bola_object.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': llave_bola_object.id,
                                'product_uom': llave_bola_object.uom_id.id,
                                'customer_lead': self._get_customer_lead(llave_bola_object),
                                'last_update_price_date': llave_bola_object.last_update_pricelist_date,
                                'last_update_price_partner': llave_bola_object.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    llave_bola_object.pricelist_id, 
                                    llave_bola_object.id, 
                                    llave_bola_object.uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))                        
                            seleccionado=1
                            
                    if line.name == 'REFERENCIA POSICIONAL UNION AMERICANA':
                        entra_categoria=1
                        if self.opportunity_id.x_tipo_caneria in ['pvc']:
                            
                            union_americana_object = self.env['product.product'].search([('name','=',union_americana)])

                            data.update({
                                'name': union_americana_object.name,
                                'price_unit': union_americana_object.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': union_americana_object.id,
                                'product_uom': union_americana_object.uom_id.id,
                                'customer_lead': self._get_customer_lead(union_americana_object),
                                'last_update_price_date': union_americana_object.last_update_pricelist_date,
                                'last_update_price_partner': union_americana_object.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    union_americana_object.pricelist_id, 
                                    union_americana_object.id, 
                                    union_americana_object.uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))                        
                            seleccionado=1
                        
                        if self.opportunity_id.x_tipo_caneria in ['vwell'] and self.opportunity_id.x_pul_canerias_s2 in ['1','1,25','1,5','2']:
                            
                            union_americana_object = self.env['product.product'].search([('name','=',union_americana)])

                            data.update({
                                'name': union_americana_object.name,
                                'price_unit': union_americana_object.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': union_americana_object.id,
                                'product_uom': union_americana_object.uom_id.id,
                                'customer_lead': self._get_customer_lead(union_americana_object),
                                'last_update_price_date': union_americana_object.last_update_pricelist_date,
                                'last_update_price_partner': union_americana_object.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    union_americana_object.pricelist_id, 
                                    union_americana_object.id, 
                                    union_americana_object.uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))                        
                            seleccionado=1
                    
                    if line.name == 'REFERENCIA POSICIONAL CODO HI GALVA.':
                        entra_categoria=1
                        if self.opportunity_id.x_tipo_caneria in ['pvc']:
                            
                            codo_hi_galva_object = self.env['product.product'].search([('name','=',codo_hi_galva)])

                            data.update({
                                'name': codo_hi_galva_object.name,
                                'price_unit': codo_hi_galva_object.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': codo_hi_galva_object.id,
                                'product_uom': codo_hi_galva_object.uom_id.id,
                                'customer_lead': self._get_customer_lead(codo_hi_galva_object),
                                'last_update_price_date': codo_hi_galva_object.last_update_pricelist_date,
                                'last_update_price_partner': codo_hi_galva_object.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    codo_hi_galva_object.pricelist_id, 
                                    codo_hi_galva_object.id, 
                                    codo_hi_galva_object.uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))                        
                            seleccionado=1
                        
                        if self.opportunity_id.x_tipo_caneria in ['vwell'] and self.opportunity_id.x_pul_canerias_s2 in ['1','1,25','1,5','2']:
                            
                            codo_hi_galva_object = self.env['product.product'].search([('name','=',codo_hi_galva)])

                            data.update({
                                'name': codo_hi_galva_object.name,
                                'price_unit': codo_hi_galva_object.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': codo_hi_galva_object.id,
                                'product_uom': codo_hi_galva_object.uom_id.id,
                                'customer_lead': self._get_customer_lead(codo_hi_galva_object),
                                'last_update_price_date': codo_hi_galva_object.last_update_pricelist_date,
                                'last_update_price_partner': codo_hi_galva_object.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    codo_hi_galva_object.pricelist_id, 
                                    codo_hi_galva_object.id, 
                                    codo_hi_galva_object.uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))                        
                            seleccionado=1
                            
                    if line.name == 'REFERENCIA POSICIONAL TUBERIA PVC (V-WELL)':
                        entra_categoria=1
                        if self.opportunity_id.x_tipo_caneria in ['vwell'] and self.opportunity_id.x_pul_canerias_s2 in ['1','1,25','1,5','2']:
                            
                            tuberia_pvc_vwell_object = self.env['product.product'].search([('name','=',tuberia_pvc_vwell)])
                            if self.opportunity_id.x_servicios_requeridos in ['s2','s2s3']:                                
                                cantidad = self.opportunity_id.profundidad_s2 - 6
                            else:
                                cantidad = profundidad

                            data.update({
                                'name': tuberia_pvc_vwell_object.name,
                                'price_unit': tuberia_pvc_vwell_object.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': cantidad,
                                'product_id': tuberia_pvc_vwell_object.id,
                                'product_uom': tuberia_pvc_vwell_object.uom_id.id,
                                'customer_lead': self._get_customer_lead(tuberia_pvc_vwell_object),
                                'last_update_price_date': tuberia_pvc_vwell_object.last_update_pricelist_date,
                                'last_update_price_partner': tuberia_pvc_vwell_object.last_update_pricelist_partner,                       
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    tuberia_pvc_vwell_object.pricelist_id, 
                                    tuberia_pvc_vwell_object.id, 
                                    tuberia_pvc_vwell_object.uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))                        
                            seleccionado=1
                            
                    if line.name == 'REFERENCIA POSICIONAL TERMINAL HE PVC (V-WELL)':
                        entra_categoria=1
                        if self.opportunity_id.x_tipo_caneria in ['vwell'] and self.opportunity_id.x_pul_canerias_s2 in ['1','1,25','1,5','2']:
                            
                            terminal_he_pvc_vwell_object = self.env['product.product'].search([('name','=',terminal_he_pvc_vwell)])
                            
                            if self.opportunity_id.x_servicios_requeridos in ['s2','s2s3']:                                
                                if (self.opportunity_id.profundidad_s2 - 6)%6>0:
                                    cantidad = round(((self.opportunity_id.profundidad_s2 - 6)/6)+0.5)
                            else:
                                cantidad = (profundidad - 6)/6

                            data.update({
                                'name': terminal_he_pvc_vwell_object.name,
                                'price_unit': terminal_he_pvc_vwell_object.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': cantidad,
                                'product_id': terminal_he_pvc_vwell_object.id,
                                'product_uom': terminal_he_pvc_vwell_object.uom_id.id,
                                'customer_lead': self._get_customer_lead(terminal_he_pvc_vwell_object),
                                'last_update_price_date': terminal_he_pvc_vwell_object.last_update_pricelist_date,
                                'last_update_price_partner': terminal_he_pvc_vwell_object.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    terminal_he_pvc_vwell_object.pricelist_id, 
                                    terminal_he_pvc_vwell_object.id, 
                                    terminal_he_pvc_vwell_object.uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))                        
                            seleccionado=1
                            
                    if line.name == 'REFERENCIA POSICIONAL FLANGE HI ACERO':
                        entra_categoria=1    
                        
                        _logger.info('x_tipo_caneria= {}'.format(self.opportunity_id.x_tipo_caneria))
                        _logger.info('x_pul_canerias_s2= {}'.format(self.opportunity_id.x_pul_canerias_s2))
                        if self.opportunity_id.x_tipo_caneria in ['vwell'] and self.opportunity_id.x_pul_canerias_s2 in ['3','4','5','6']:
                            _logger.info('x_tipo_caneria= {}'.format(self.opportunity_id.x_tipo_caneria))
                            _logger.info('x_pul_canerias_s2= {}'.format(self.opportunity_id.x_pul_canerias_s2))
                            flange_hi_acero_object = self.env['product.product'].search([('name','=',flange_hi_acero)])

                            data.update({
                                'name': flange_hi_acero_object.name,
                                'price_unit': flange_hi_acero_object.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': flange_hi_acero_object.id,
                                'product_uom': flange_hi_acero_object.uom_id.id,
                                'customer_lead': self._get_customer_lead(flange_hi_acero_object),
                                'last_update_price_date': flange_hi_acero_object.last_update_pricelist_date,
                                'last_update_price_partner': flange_hi_acero_object.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    flange_hi_acero_object.pricelist_id, 
                                    flange_hi_acero_object.id, 
                                    flange_hi_acero_object.uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))                        
                            seleccionado=1 
                            
                    if line.name == 'REFERENCIA POSICIONAL CURVA BRIDA BRIDA ACERO':
                        entra_categoria=1                        
                        if self.opportunity_id.x_tipo_caneria in ['vwell'] and self.opportunity_id.x_pul_canerias_s2 in ['3','4','5','6']:
                            curva_brida_brida_acero_object = self.env['product.product'].search([('name','=',curva_brida_brida_acero)])

                            data.update({
                                'name': curva_brida_brida_acero_object.name,
                                'price_unit': curva_brida_brida_acero_object.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': curva_brida_brida_acero_object.id,
                                'product_uom': curva_brida_brida_acero_object.uom_id.id,
                                'customer_lead': self._get_customer_lead(curva_brida_brida_acero_object),
                                'last_update_price_date': curva_brida_brida_acero_object.last_update_pricelist_date,
                                'last_update_price_partner': curva_brida_brida_acero_object.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    curva_brida_brida_acero_object.pricelist_id, 
                                    curva_brida_brida_acero_object.id, 
                                    curva_brida_brida_acero_object.uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))                        
                            seleccionado=1
                    
                    if line.name == 'REFERENCIA POSICIONAL VALVULA ELASTOAMERICA':
                        entra_categoria=1                        
                        if self.opportunity_id.x_tipo_caneria in ['vwell'] and self.opportunity_id.x_pul_canerias_s2 in ['3','4','5','6']:
                            valvula_elastoamerica_object = self.env['product.product'].search([('name','=',valvula_elastoamerica)])

                            data.update({
                                'name': valvula_elastoamerica_object.name,
                                'price_unit': valvula_elastoamerica_object.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': valvula_elastoamerica_object.id,
                                'product_uom': valvula_elastoamerica_object.uom_id.id,
                                'customer_lead': self._get_customer_lead(valvula_elastoamerica_object),
                                'last_update_price_date': valvula_elastoamerica_object.last_update_pricelist_date,
                                'last_update_price_partner': valvula_elastoamerica_object.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    valvula_elastoamerica_object.pricelist_id, 
                                    valvula_elastoamerica_object.id, 
                                    valvula_elastoamerica_object.uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))                        
                            seleccionado=1 
                            
                    if line.name == 'REFERENCIA POSICIONAL GOMA BRIDA':
                        entra_categoria=1                        
                        if self.opportunity_id.x_tipo_caneria in ['vwell'] and self.opportunity_id.x_pul_canerias_s2 in ['3','4','5','6']:
                            goma_brida_object = self.env['product.product'].search([('name','=',goma_brida)])

                            data.update({
                                'name': goma_brida_object.name,
                                'price_unit': goma_brida_object.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': 2,
                                'product_id': goma_brida_object.id,
                                'product_uom': goma_brida_object.uom_id.id,
                                'customer_lead': self._get_customer_lead(goma_brida_object),
                                'last_update_price_date': goma_brida_object.last_update_pricelist_date,
                                'last_update_price_partner': goma_brida_object.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    goma_brida_object.pricelist_id, 
                                    goma_brida_object.id, 
                                    goma_brida_object.uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))                        
                            seleccionado=1
                            
                    if line.name == 'REFERENCIA POSICIONAL COPLA HI GALVA.':
                        entra_categoria=1                        
                        if self.opportunity_id.x_tipo_caneria in ['vwell'] and self.opportunity_id.x_pul_canerias_s2 in ['3','4','5','6']:
                            copla_hi_galva_object = self.env['product.product'].search([('name','=',copla_hi_galva)])

                            data.update({
                                'name': copla_hi_galva_object.name,
                                'price_unit': copla_hi_galva_object.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': copla_hi_galva_object.id,
                                'product_uom': copla_hi_galva_object.uom_id.id,
                                'customer_lead': self._get_customer_lead(copla_hi_galva_object),
                                'last_update_price_date': copla_hi_galva_object.last_update_pricelist_date,
                                'last_update_price_partner': copla_hi_galva_object.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    copla_hi_galva_object.pricelist_id, 
                                    copla_hi_galva_object.id, 
                                    copla_hi_galva_object.uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))                        
                            seleccionado=1
                            
                    if line.name == 'REFERENCIA POSICIONAL TAPA POZO':
                        entra_categoria=1                        
                        if self.opportunity_id.x_servicios_requeridos in ['s2','s2s3','s1s2','s1s2s3']:
                            if self.opportunity_id.x_servicios_requeridos in ['s2']:
                                tapa_pozo_name = 'TAPA POZO '+str(self.opportunity_id.diametro_s2)+'" CON INSTALACION'
                            else:
                                tapa_pozo_name = 'TAPA POZO '+diametro_tapa+'" CON INSTALACION'
                                
                            tapa_pozo_object = self.env['product.product'].search([('name','=',tapa_pozo_name)])

                            data.update({
                                'name': tapa_pozo_object.name,
                                'price_unit': tapa_pozo_object.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': 1,
                                'product_id': tapa_pozo_object.id,
                                'product_uom': tapa_pozo_object.uom_id.id,
                                'customer_lead': self._get_customer_lead(tapa_pozo_object),
                                'last_update_price_date': tapa_pozo_object.last_update_pricelist_date,
                                'last_update_price_partner': tapa_pozo_object.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    tapa_pozo_object.pricelist_id, 
                                    tapa_pozo_object.id, 
                                    tapa_pozo_object.uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))                        
                            seleccionado=1
                        
                    if line.product_id.product_tmpl_id.id == 516:    #perno hexagonal
                        entra_categoria = 1
                        if self.opportunity_id.x_tipo_caneria in ['vwell']:
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': 16,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id, 
                                    line.product_id, 
                                    line.product_uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                        
                    if line.product_id.product_tmpl_id.id == 517:    #golilla plana 5/8"
                        entra_categoria = 1
                        if self.opportunity_id.x_tipo_caneria in ['vwell']:
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': 32,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id, 
                                    line.product_id, 
                                    line.product_uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                        
                    if line.product_id.product_tmpl_id.id == 518:    #golilla presion 5/8"
                        entra_categoria = 1
                        if self.opportunity_id.x_tipo_caneria in ['vwell']:
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': 16,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id, 
                                    line.product_id, 
                                    line.product_uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                        
                    if line.product_id.product_tmpl_id.id == 519:    #tuerca 5/8"
                        entra_categoria = 1
                        if self.opportunity_id.x_tipo_caneria in ['vwell']:
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': 16,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                            
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id,
                                    line.product_id,
                                    line.product_uom_id,
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1                    
                        
                    if line.product_id.name == 'REFERENCIA POSICIONAL ESTANQUE':
                        #_logger.info('x_superficie= {}'.format(self.opportunity_id.x_superficie))
                        if self.opportunity_id.x_superficie:
                            #estanque = self.env['product.product'].search([('id','=',self.opportunity_id.estanque_acumulacion_sup.id)])
                            data.update({
                                'name': self.opportunity_id.estanque_acumulacion_sup.name,
                                'price_unit': self.opportunity_id.estanque_acumulacion_sup.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': 1,
                                'product_id': self.opportunity_id.estanque_acumulacion_sup.id,
                                'product_uom': self.opportunity_id.estanque_acumulacion_sup.uom_id.id,
                                'customer_lead': self._get_customer_lead(self.opportunity_id.estanque_acumulacion_sup),
                                'last_update_price_date': self.opportunity_id.estanque_acumulacion_sup.last_update_pricelist_date,
                                'last_update_price_partner': self.opportunity_id.estanque_acumulacion_sup.last_update_pricelist_partner,
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.opportunity_id.estanque_acumulacion_sup.list_price, 
                                    self.opportunity_id.estanque_acumulacion_sup, 
                                    self.opportunity_id.estanque_acumulacion_sup.uom_id.id, 
                                    fields.Date.context_today(self)))
                                
                        elif self.opportunity_id.x_enterrado_s3:                                
                            data.update({
                                'name': self.opportunity_id.estanque_acumulacion_ent.name,
                                'price_unit': self.opportunity_id.estanque_acumulacion_ent.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': self.opportunity_id.estanque_acumulacion_ent.id,
                                'product_uom': self.opportunity_id.estanque_acumulacion_ent.uom_id.id,
                                'customer_lead': self._get_customer_lead(self.opportunity_id.estanque_acumulacion_ent),
                                'last_update_price_date': self.opportunity_id.estanque_acumulacion_ent.last_update_pricelist_date,
                                'last_update_price_partner': self.opportunity_id.estanque_acumulacion_ent.last_update_pricelist_partner,
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.opportunity_id.estanque_acumulacion_ent.list_price, 
                                    self.opportunity_id.estanque_acumulacion_ent.id, 
                                    self.opportunity_id.estanque_acumulacion_ent.uom_id.id, 
                                    fields.Date.context_today(self)))

                        order_lines.append((0, 0, data))
                        seleccionado=1
                    
                    if line.product_id.name == 'REFERENCIA POSICIONAL BOMBA CENTRIFUGA':
                        data.update({
                            'name': self.opportunity_id.bomba_centrifuga.name,
                            'price_unit': self.opportunity_id.bomba_centrifuga.list_price,
                            'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                            'product_uom_qty': line.product_uom_qty,
                            'product_id': self.opportunity_id.bomba_centrifuga.id,
                            'product_uom': self.opportunity_id.bomba_centrifuga.uom_id.id,
                            'customer_lead': self._get_customer_lead(self.opportunity_id.bomba_centrifuga),
                            'last_update_price_date': self.opportunity_id.bomba_centrifuga.last_update_pricelist_date,
                            'last_update_price_partner': self.opportunity_id.bomba_centrifuga.last_update_pricelist_partner,
                        })                        
                        if self.pricelist_id:
                            data.update(self.env['sale.order.line']._get_purchase_price(
                                self.opportunity_id.bomba_centrifuga.list_price, 
                                self.opportunity_id.bomba_centrifuga.id, 
                                self.opportunity_id.bomba_centrifuga.uom_id.id, 
                                fields.Date.context_today(self)))

                        order_lines.append((0, 0, data))
                        seleccionado=1
                        
                    if line.product_id.name == 'REFERENCIA POSICIONAL LOSA HORMIGON':
                        entra_categoria=1
                        if self.opportunity_id.x_superficie:
                            data.update({
                                'name': self.opportunity_id.losa_hormigon.name,
                                'price_unit': self.opportunity_id.losa_hormigon.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': self.opportunity_id.losa_hormigon.id,
                                'product_uom': self.opportunity_id.losa_hormigon.uom_id.id,
                                'customer_lead': self._get_customer_lead(self.opportunity_id.losa_hormigon),
                                'last_update_price_date': self.opportunity_id.losa_hormigon.last_update_pricelist_date,
                                'last_update_price_partner': self.opportunity_id.losa_hormigon.last_update_pricelist_partner,
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.opportunity_id.losa_hormigon.list_price, 
                                    self.opportunity_id.losa_hormigon.id, 
                                    self.opportunity_id.losa_hormigon.uom_id.id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                        
                    if line.product_id.name == 'REFERENCIA POSICIONAL GUARDAMOTOR':
                        data.update({
                            'name': self.opportunity_id.guardamotor.name,
                            'price_unit': self.opportunity_id.guardamotor.list_price,
                            'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                            'product_uom_qty': line.product_uom_qty,
                            'product_id': self.opportunity_id.guardamotor.id,
                            'product_uom': self.opportunity_id.guardamotor.uom_id.id,
                            'customer_lead': self._get_customer_lead(self.opportunity_id.guardamotor),
                            'last_update_price_date': self.opportunity_id.guardamotor.last_update_pricelist_date,
                            'last_update_price_partner': self.opportunity_id.guardamotor.last_update_pricelist_partner,
                        })                        
                        if self.pricelist_id:
                            data.update(self.env['sale.order.line']._get_purchase_price(
                                self.opportunity_id.guardamotor.list_price, 
                                self.opportunity_id.guardamotor.id, 
                                self.opportunity_id.guardamotor.uom_id.id, 
                                fields.Date.context_today(self)))

                        order_lines.append((0, 0, data))
                        seleccionado=1
                        
                    if line.product_id.name == 'REFERENCIA POSICIONAL ESTANQUE HIDRONEUMATICO':
                        entra_categoria=1
                        if self.opportunity_id.x_hidropack:
                            data.update({
                                'name': self.opportunity_id.estanque_hidroneumatico.name,
                                'price_unit': self.opportunity_id.estanque_hidroneumatico.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': self.opportunity_id.estanque_hidroneumatico.id,
                                'product_uom': self.opportunity_id.estanque_hidroneumatico.uom_id.id,
                                'customer_lead': self._get_customer_lead(self.opportunity_id.estanque_hidroneumatico),
                                'last_update_price_date': self.opportunity_id.estanque_hidroneumatico.last_update_pricelist_date,
                                'last_update_price_partner': self.opportunity_id.estanque_hidroneumatico.last_update_pricelist_partner,
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.opportunity_id.estanque_hidroneumatico.list_price, 
                                    self.opportunity_id.estanque_hidroneumatico.id, 
                                    self.opportunity_id.estanque_hidroneumatico.uom_id.id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                        
                    if line.product_id.name == 'REFERENCIA POSICIONAL MANOMETRO':
                        entra_categoria=1
                        if self.opportunity_id.x_hidropack:
                            data.update({
                                'name': self.opportunity_id.manometro.name,
                                'price_unit': self.opportunity_id.manometro.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': self.opportunity_id.manometro.id,
                                'product_uom': self.opportunity_id.manometro.uom_id.id,
                                'customer_lead': self._get_customer_lead(self.opportunity_id.manometro),
                                'last_update_price_date': self.opportunity_id.manometro.last_update_pricelist_date,
                                'last_update_price_partner': self.opportunity_id.manometro.last_update_pricelist_partner,
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.opportunity_id.manometro.list_price, 
                                    self.opportunity_id.manometro.id, 
                                    self.opportunity_id.manometro.uom_id.id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                            
                    if line.product_id.name == 'REFERENCIA POSICIONAL PRESSCONTROL':
                        entra_categoria=1
                        if self.opportunity_id.x_controlpress:
                            data.update({
                                'name': self.opportunity_id.presscontrol.name,
                                'price_unit': self.opportunity_id.presscontrol.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': self.opportunity_id.presscontrol.id,
                                'product_uom': self.opportunity_id.presscontrol.uom_id.id,
                                'customer_lead': self._get_customer_lead(self.opportunity_id.presscontrol),
                                'last_update_price_date': self.opportunity_id.presscontrol.last_update_pricelist_date,
                                'last_update_price_partner': self.opportunity_id.presscontrol.last_update_pricelist_partner,
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.opportunity_id.presscontrol.list_price, 
                                    self.opportunity_id.presscontrol.id, 
                                    self.opportunity_id.presscontrol.uom_id.id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                        
                    if line.product_id.name == 'REFERENCIA POSICIONAL PRESOSTATO':
                        entra_categoria=1
                        if self.opportunity_id.x_hidropack:
                            data.update({
                                'name': self.opportunity_id.presostato.name,
                                'price_unit': self.opportunity_id.presostato.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': self.opportunity_id.presostato.id,
                                'product_uom': self.opportunity_id.presostato.uom_id.id,
                                'customer_lead': self._get_customer_lead(self.opportunity_id.presostato),
                                'last_update_price_date': self.opportunity_id.presostato.last_update_pricelist_date,
                                'last_update_price_partner': self.opportunity_id.presostato.last_update_pricelist_partner,
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.opportunity_id.presostato.list_price, 
                                    self.opportunity_id.presostato.id, 
                                    self.opportunity_id.presostato.uom_id.id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                        
                    if line.product_id.name == 'EXCAVACIÓN' and self.opportunity_id.x_enterrado_s3 == True:                            
                        data.update({
                            'price_unit': self.opportunity_id.excavacion,
                            'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                            'product_uom_qty': line.product_uom_qty,
                            'product_id': line.product_id.id,
                            'product_uom': line.product_uom_id.id,
                            'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                            'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                            'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,
                        })                        
                        if self.pricelist_id:
                            data.update(self.env['sale.order.line']._get_purchase_price(
                                self.pricelist_id, 
                                line.product_id, 
                                line.product_uom_id, 
                                fields.Date.context_today(self)))

                        order_lines.append((0, 0, data))
                        seleccionado=1
                        
                    if line.product_id.product_tmpl_id.id == 1180: 
                        entra_categoria=1
                        if self.opportunity_id.x_hidropack:                                
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id, 
                                    line.product_id, 
                                    line.product_uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                            
                    if line.product_id.product_tmpl_id.id == 1723: 
                        entra_categoria=1
                        if self.opportunity_id.x_hidropack:                                
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                                'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.pricelist_id, 
                                    line.product_id, 
                                    line.product_uom_id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                        
                    if line.product_id.product_tmpl_id.id == 1530 and self.opportunity_id.x_servicios_requeridos != 's4':
                        data.update({
                            'price_unit': self.opportunity_id.x_valor_instalacion_s3,
                            'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                            'product_uom_qty': line.product_uom_qty,
                            'product_id': line.product_id.id,
                            'product_uom': line.product_uom_id.id,
                            'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                            'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                            'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,
                        })                        
                        if self.pricelist_id:
                            data.update(self.env['sale.order.line']._get_purchase_price(
                                self.pricelist_id, 
                                line.product_id, 
                                line.product_uom_id, 
                                fields.Date.context_today(self)))

                        order_lines.append((0, 0, data))
                        seleccionado=1
                    
                    if line.product_id.name == 'REFERENCIA POSICIONAL BOMBA CLORACION': 
                        entra_categoria=1
                        if self.opportunity_id.x_cloracion:
                            data.update({
                                'name': self.opportunity_id.bomba_cloro.name,
                                'price_unit': self.opportunity_id.bomba_cloro.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': self.opportunity_id.bomba_cloro.id,
                                'product_uom': self.opportunity_id.bomba_cloro.uom_id.id,
                                'customer_lead': self._get_customer_lead(self.opportunity_id.bomba_cloro),
                                'last_update_price_date': self.opportunity_id.bomba_cloro.last_update_pricelist_date,
                                'last_update_price_partner': self.opportunity_id.bomba_cloro.last_update_pricelist_partner,
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.opportunity_id.bomba_cloro.list_price, 
                                    self.opportunity_id.bomba_cloro.id, 
                                    self.opportunity_id.bomba_cloro.uom_id.id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1
                    
                    if line.product_id.name == 'REFERENCIA POSICIONAL ESTANQUE CLORO': 
                        entra_categoria=1
                        if self.opportunity_id.x_cloracion:
                            data.update({
                                'name': self.opportunity_id.estanque_cloro.name,
                                'price_unit': self.opportunity_id.estanque_cloro.list_price,
                                'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': self.opportunity_id.estanque_cloro.id,
                                'product_uom': self.opportunity_id.estanque_cloro.uom_id.id,
                                'customer_lead': self._get_customer_lead(self.opportunity_id.estanque_cloro),
                                'last_update_price_date': self.opportunity_id.estanque_cloro.last_update_pricelist_date,
                                'last_update_price_partner': self.opportunity_id.estanque_cloro.last_update_pricelist_partner,
                            })                        
                            if self.pricelist_id:
                                data.update(self.env['sale.order.line']._get_purchase_price(
                                    self.opportunity_id.estanque_cloro.list_price, 
                                    self.opportunity_id.estanque_cloro.id, 
                                    self.opportunity_id.estanque_cloro.uom_id.id, 
                                    fields.Date.context_today(self)))

                            order_lines.append((0, 0, data))
                            seleccionado=1                        
                    
                    matriz_s4 = self.opportunity_id
                    if line.product_id.product_tmpl_id.categ_id.display_name == 'SERVICIOS / PRUEBAS' or 'SERVICIOS' and self.opportunity_id.x_servicios_requeridos == 's4':
                        entra_categoria=1
                        for matriz_servicio4 in matriz_s4.lead_matriz_s4_lines_ids:                                
                            if matriz_servicio4.listado_servicios.id == line.product_id.product_tmpl_id.id:
                                #_logger.info('matriz= {}'.format(matriz_servicio4.listado_servicios.id))
                                #_logger.info('plantilla= {}'.format(line.product_id.product_tmpl_id.id))
                                data.update({
                                    'price_unit': matriz_servicio4.valor_servicio,
                                    'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                                    'product_uom_qty': 1,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),                                        
                                    'utilidad_porcentaje': 0,                            
                                })                        
                                if self.pricelist_id:
                                    data.update(self.env['sale.order.line']._get_purchase_price(
                                        self.pricelist_id, 
                                        line.product_id, 
                                        line.product_uom_id, 
                                        fields.Date.context_today(self)))

                                    order_lines.append((0, 0, data))                    
                                    seleccionado=1 

                    if entra_categoria==0 and seleccionado == 0:                        
                        data.update({
                            'price_unit': price,
                            'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                            'product_uom_qty': line.product_uom_qty,
                            'product_id': line.product_id.id,
                            'product_uom': line.product_uom_id.id,
                            'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                            'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                            'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,                            
                        })                        
                        if self.pricelist_id:
                            data.update(self.env['sale.order.line']._get_purchase_price(
                                self.pricelist_id, 
                                line.product_id, 
                                line.product_uom_id, 
                                fields.Date.context_today(self)))

                        order_lines.append((0, 0, data))                    
                else:
                    _logger.info('es una orden de trabajo')
                    data.update({
                        'price_unit': price,
                        'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                        'product_uom_qty': line.product_uom_qty,
                        'product_id': line.product_id.id,
                        'product_uom': line.product_uom_id.id,
                        'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                        'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                        'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,
                    })
                    if self.pricelist_id:
                        data.update(self.env['sale.order.line']._get_purchase_price(
                            self.pricelist_id, 
                            line.product_id, 
                            line.product_uom_id, 
                            fields.Date.context_today(self)))
                        
                    order_lines.append((0, 0, data))
            else:
                order_lines.append((0, 0, data))
        self.order_line = order_lines
        self.order_line._compute_tax_id()

        option_lines = [(5, 0, 0)]
        for option in template.sale_order_template_option_ids:
            data = self._compute_option_data_for_template_change(option)
            option_lines.append((0, 0, data))
        self.sale_order_option_ids = option_lines

        if template.number_of_days > 0:
            self.validity_date = fields.Date.context_today(self) + timedelta(template.number_of_days)

        self.require_signature = template.require_signature
        self.require_payment = template.require_payment

        if template.note:
            self.note = template.note