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
    
            
    #onchange de plantillas de presupuesto
    sale_order_template_id_prueba = fields.Many2one(
        'sale.order.template', 'prueba de cotizaciones',
        readonly=True, check_company=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")  
    
    sale_order_template_id = fields.Many2one(
        'sale.order.template', 'Quotation Template',
        readonly=True, check_company=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    
    #para ordenes de trabajo
    x_equipo_asignado = fields.Selection([('eqp21','Equipo 21'),('eqp22','Equipo 22'),('eqp23','Equipo 23'),('eqp24','Equipo 24'),('eqb1','Equipo Bombas 1'),('eqb2','Equipo Bombas 2'),('eqb3','Equipo Bombas 3')],string='Equipo asignado')
    x_fecha_retiro = fields.Date(string='Fecha de retiro de materiales')    
    #formulario principal
    opportunity_id = fields.Many2one('crm.lead', string='Opportunity', check_company=True,domain="[('type', '=', 'opportunity'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    x_servicios_requeridos = fields.Selection(related='opportunity_id.x_servicios_requeridos', string='Servicios requeridos')
    x_enviar_wsp = fields.Boolean(related='opportunity_id.x_enviar_wsp',string='Enviar por WhatsApp')
    x_tipo_instalacion = fields.Selection(related='opportunity_id.x_tipo_instalacion',string='Tipo de instalacion')
    x_otro = fields.Char(related='opportunity_id.x_otro',string='otro')
    #servicio 1
    x_tipo_servicio = fields.Selection(related='opportunity_id.x_tipo_servicio',string='Tipo de servicio')
    x_diametro_pozo = fields.Integer(related='opportunity_id.x_diametro',string='Diametro')
    x_profundidad_pozo = fields.Integer(related='opportunity_id.x_profundidad',string='Profundidad')
    x_faena = fields.Integer(related='opportunity_id.x_faena',string='Instalacion de faena')
    x_valorxmt = fields.Integer(related='opportunity_id.x_valorxmt',string='Valor por metro')
    x_prueba_bombeo = fields.Selection(related='opportunity_id.x_prueba_bombeo',string='Prueba de bombeo')
    x_valorpb = fields.Integer(related='opportunity_id.x_valorpb',string='Valor prueba de bombeo')
    x_insc_dga = fields.Integer(related='opportunity_id.x_insc_dga',string='Inscripcion pozo DGA')
    corona = fields.Many2one('product.template',related='opportunity_id.corona',string='Corona')
    x_valor_corona = fields.Integer(related='opportunity_id.x_valor_corona',string='Valor corona')
    x_duracion_s1 = fields.Integer(related='opportunity_id.x_duracion',string='Duracion')
    prueba_bombeo = fields.Many2one('product.template',related='opportunity_id.prueba_bombeo',string='Prueba de bombeo')
    #servicio 2
    x_caudal_crm = fields.Integer(related='opportunity_id.x_caudal_fl',string='Caudal')
    x_hp_fl = fields.Float(related='opportunity_id.x_hp_fl',string='HP')
    x_bomba_crm = fields.Many2one('product.template',related='opportunity_id.x_bomba_crm',string='Bomba')
    x_motor_crm = fields.Many2one('product.template',related='opportunity_id.x_motor_crm',string='Motor')
    tablero = fields.Many2one('product.template',related='opportunity_id.tablero',string='Tablero')
    x_tipo_caneria = fields.Selection(related='opportunity_id.x_tipo_caneria',string='Tipo de caneria')
    x_pul_canerias_s2 = fields.Selection(related='opportunity_id.x_pul_canerias_s2',string='Pulgadas')
    x_impulsion = fields.Integer(related='opportunity_id.x_impulsion',string='Total impulsion')
    x_altura = fields.Integer(related='opportunity_id.x_altura',string='Altura total')
    x_voltaje = fields.Integer(related='opportunity_id.x_voltaje',string='Voltaje')
    x_valor_instalacion = fields.Integer(related='opportunity_id.x_valor_instalacion',string='Valor Instalacion')
    x_duracion_total = fields.Integer(related='opportunity_id.x_duracion_s2',string='Duracion')
    x_valor_referencia = fields.Integer(related='opportunity_id.x_valor_referencia',string='Valor total referencia')
    #servicio 3
    x_estanque = fields.Selection(related='opportunity_id.x_estanque',string='Capacidad estanque')
    x_superficie = fields.Boolean(related='opportunity_id.x_superficie',string='Superficie')
    x_enterrado_s3 = fields.Boolean(related='opportunity_id.x_enterrado_s3',string='Enterrado')
    x_bombacen_hp_fl = fields.Float(related='opportunity_id.x_bombacen_hp_fl',string='Bomba centrifuga HP')
    x_hidropack = fields.Boolean(related='opportunity_id.x_hidropack',string='Hidropack')
    x_controlpress = fields.Boolean(related='opportunity_id.x_controlpress',string='ControlPress')
    x_cloracion = fields.Boolean(related='opportunity_id.x_cloracion',string='Cloracion')
    x_valor_instalacion_s3 = fields.Integer(related='opportunity_id.x_valor_instalacion_s3',string='Valor instalacion')
    x_duracion_s3 = fields.Integer(related='opportunity_id.x_duracion_s3',string='Duracion')
    x_valor_referencia_s3 = fields.Integer(related='opportunity_id.x_valor_referencia_s3',string='valor referencial')
    #servicio 4
    x_servicio4 = fields.Selection(related='opportunity_id.x_servicio4',string='Servicio')
    x_precios4 = fields.Integer(related='opportunity_id.x_precios4',string='Precio servicio')
    #servicio 5
    x_idakm = fields.Integer(related='opportunity_id.x_idakm',string='Ida (km)')
    x_duracionhrs = fields.Integer(related='opportunity_id.x_duracionhrs',string='Duracion hrs trabajo')
    x_num_personas = fields.Integer(related='opportunity_id.x_num_personas',string='Num. Personas Totales')
    x_sin_camion = fields.Boolean(related='opportunity_id.x_sin_camion',string='Sin camion Pluma')
    x_con_camion = fields.Boolean(related='opportunity_id.x_con_camion',string='Con camion Pluma')
    x_num_vehiculos = fields.Integer(related='opportunity_id.x_num_vehiculos',string='Num. Vehiculo camion')
    #servicio 6
    x_mt_estimado = fields.Integer(related='opportunity_id.x_mt_estimado',string='Metros estimados')
    x_idakms6 = fields.Integer(related='opportunity_id.x_idakms6',string='Ida (km)')
    x_dias_s6 = fields.Integer(related='opportunity_id.x_dias_s6',string='Num. dias')
    x_personas_s6 = fields.Integer(related='opportunity_id.x_personas_s6',string='Num. personas')
    x_dias_s6_lim = fields.Integer(related='opportunity_id.x_dias_s6_lim',string='Num. dias')
    x_num_perforadores = fields.Integer(related='opportunity_id.x_num_perforadores',string='Num. Pers. perforador')
    x_num_soldadores = fields.Integer(related='opportunity_id.x_num_soldadores',string='Num. Pers. soldador')
    x_num_ayudantes = fields.Integer(related='opportunity_id.x_num_ayudantes',string='Num. Pers. ayudante')
    x_dias_s6_ib = fields.Integer(related='opportunity_id.x_dias_s6_ib',string='Num. dias')
    x_num_personas_ib = fields.Integer(related='opportunity_id.x_num_personas_ib',string='Num. personas')
    # campos de acuerdos de pago
    x_abono_crm = fields.Integer(related='opportunity_id.x_abono',string='Abono inicial (%)')
    x_abono_m_crm = fields.Integer(related='opportunity_id.x_abono_monto',string='Abono ($)')
    x_cuotas_crm = fields.Integer(related='opportunity_id.x_cuotas',string='Num. cuotas')
    x_comentarios = fields.Char(string='Comentarios',related='opportunity_id.x_comentarios')    
    x_encabezado_coti1 = fields.Html(string='encabezado coti 1',default = _get_default_enc1)
    x_encabezado_coti2 = fields.Html(string='encabezado coti 2',default = _get_default_enc2)
    x_encabezado_coti3 = fields.Html(string='encabezado coti 3',default = _get_default_enc3)
    x_encabezado_coti4 = fields.Html(string='encabezado coti 4',default = _get_default_enc4)
    x_encabezado_coti5 = fields.Html(string='encabezado coti 5',default = _get_default_enc5)
    
    @api.onchange('sale_order_template_id_prueba')
    def onchange_sale_order_template_id_prueba(self):
        _logger.info('entra exitosamente - metodo en req_ventas')
        if not self.sale_order_template_id_prueba:
            self.require_signature = self._get_default_require_signature()
            self.require_payment = self._get_default_require_payment()
            return
        template = self.sale_order_template_id_prueba.with_context(lang=self.partner_id.lang)

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
                    if self.opportunity_id.matriz_activada:                        
                        entra_categoria=0
                        seleccionado=0
                        #_logger.info('diametro= {}'.format(diametro))
                        #_logger.info('categoria= {}'.format(line.product_id.product_tmpl_id.categ_id.display_name))
                        _logger.info('product_id= {}'.format(line.product_id.product_tmpl_id.id))
                        matriz = self.opportunity_id
                        if line.product_id.product_tmpl_id.categ_id.display_name == 'SERVICIOS / PERFORACION':
                            entra_categoria=1
                            for matriz_perforacion in matriz.lead_matriz_lines_ids:
                                #_logger.info('matriz_perforacion= {}'.format(matriz_perforacion))
                                if matriz_perforacion.tipo_servicio_perforacion.id == line.product_id.product_tmpl_id.id:
                                    data.update({
                                        'price_unit': matriz_perforacion.valor_metro,
                                        'discount': 100 - ((100 - discount) * (
                                                100 - line.discount) / 100),
                                        'product_uom_qty': matriz_perforacion.cantidad_metros,
                                        'product_id': line.product_id.id,
                                        'product_uom': line.product_uom_id.id,
                                        'customer_lead': self._get_customer_lead(
                                            line.product_id.product_tmpl_id),
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
                                        'price_unit': price,
                                        'discount': 100 - ((100 - discount) * (
                                                100 - line.discount) / 100),
                                        'product_uom_qty': line.product_uom_qty,
                                        'product_id': line.product_id.id,
                                        'product_uom': line.product_uom_id.id,
                                        'customer_lead': self._get_customer_lead(
                                            line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'SERVICIOS / PRUEBAS':
                            entra_categoria=1
                            if self.opportunity_id.prueba_bombeo.id == line.product_id.product_tmpl_id.id:
                                #comprueba si es una prueba de combeo DGA
                                if line.product_id.product_tmpl_id.id == 551:
                                    data.update({
                                        'price_unit': self.opportunity_id.x_insc_dga,
                                        'discount': 100 - ((100 - discount) * (
                                                100 - line.discount) / 100),
                                        'product_uom_qty': line.product_uom_qty,
                                        'product_id': line.product_id.id,
                                        'product_uom': line.product_uom_id.id,
                                        'customer_lead': self._get_customer_lead(
                                            line.product_id.product_tmpl_id),
                                        'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                        'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,
                                        'utilidad_porcentaje': 0,
                                    })
                                else:
                                    data.update({
                                        'price_unit': self.opportunity_id.x_valorpb,
                                        'discount': 100 - ((100 - discount) * (
                                                100 - line.discount) / 100),
                                        'product_uom_qty': line.product_uom_qty,
                                        'product_id': line.product_id.id,
                                        'product_uom': line.product_uom_id.id,
                                        'customer_lead': self._get_customer_lead(
                                            line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'SERVICIOS':
                            entra_categoria=1
                            if line.product_id.product_tmpl_id.id == 546:                        
                                data.update({
                                    'price_unit': self.opportunity_id.x_faena + self.opportunity_id.retiro_material,
                                    'discount': 100 - ((100 - discount) * (
                                            100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(
                                        line.product_id.product_tmpl_id),
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
                                    'discount': 100 - ((100 - discount) * (
                                            100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(
                                        line.product_id.product_tmpl_id),
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

                        if (line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / BOMBAS' or line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / KITS'):
                            entra_categoria=1
                            if self.opportunity_id.x_bomba_crm.id == line.product_id.product_tmpl_id.id:                        
                                data.update({
                                    'price_unit': price,
                                    'discount': 100 - ((100 - discount) * (
                                            100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(
                                        line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / MOTORES':
                            entra_categoria=1
                            if self.opportunity_id.x_motor_crm.id == line.product_id.product_tmpl_id.id:                        
                                data.update({
                                    'price_unit': price,
                                    'discount': 100 - ((100 - discount) * (
                                            100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(
                                        line.product_id.product_tmpl_id),
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

                        if (line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TABLEROS ELECTRICOS' or line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TABLEROS ELECTRICOS / MONOFASICO' or line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TABLEROS ELECTRICOS / TRIFASICO'):
                            entra_categoria=1
                            if self.opportunity_id.tablero.id == line.product_id.product_tmpl_id.id:                        
                                data.update({
                                    'price_unit': price,
                                    'discount': 100 - ((100 - discount) * (
                                            100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(
                                        line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TUBOS Y CAÑERIAS / PVC':                        
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': self.opportunity_id.x_impulsion,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TUBOS Y CAÑERIAS / V-WELL':                        
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': Math.ceil(self.opportunity_id.x_impulsion/3),
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / FITTING / PVC / TERMINALES':
                            if self.opportunity_id.x_impulsion%6>0:
                                cant_terminales = round((self.opportunity_id.x_impulsion/6)+0.5)
                            else:
                                cant_terminales = round(self.opportunity_id.x_impulsion/6)

                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': cant_terminales,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TUBOS Y CAÑERIAS / CONDUIT' and line.product_id.product_tmpl_id.id == 1573:                        
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': self.opportunity_id.x_impulsion,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'HERRAMIENTAS Y EQUIPOS / INSUMOS ELECTRICOS / CORDONES Y CABLES' and (line.product_id.product_tmpl_id.id == 498 or line.product_id.product_tmpl_id.id == 56 or line.product_id.product_tmpl_id.id == 497 or line.product_id.product_tmpl_id.id == 495 or line.product_id.product_tmpl_id.id == 496):                        
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': self.opportunity_id.x_impulsion+10,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'HERRAMIENTAS Y EQUIPOS / INSUMOS ELECTRICOS / CORDONES Y CABLES' and line.product_id.product_tmpl_id.id == 55:                        
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': (self.opportunity_id.x_impulsion+10)*2,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.id == 535:                        
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': self.opportunity_id.x_impulsion,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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

                        if entra_categoria==0 and seleccionado == 0:                        
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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
                        diametro = line.display_name.count(str(self.opportunity_id.x_diametro))
                        entra_categoria=0
                        seleccionado=0
                        #_logger.info('diametro= {}'.format(diametro))
                        #_logger.info('categoria= {}'.format(line.product_id.product_tmpl_id.categ_id.display_name))
                        _logger.info('product_id= {}'.format(line.product_id.product_tmpl_id.id))
                        if line.product_id.product_tmpl_id.categ_id.display_name == 'SERVICIOS / PERFORACION':
                            entra_categoria=1
                            if diametro>0:                        
                                data.update({
                                    'price_unit': self.opportunity_id.x_valorxmt,
                                    'discount': 100 - ((100 - discount) * (
                                            100 - line.discount) / 100),
                                    'product_uom_qty': self.opportunity_id.x_profundidad,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(
                                        line.product_id.product_tmpl_id),
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
                            if self.opportunity_id.corona.id == line.product_id.product_tmpl_id.id:
                                #_logger.info('corona crm= {}'.format(self.opportunity_id.corona.id))
                                #_logger.info('corona plantilla= {}'.format(line.product_id.product_tmpl_id.id))
                                data.update({
                                    'price_unit': price,
                                    'discount': 100 - ((100 - discount) * (
                                            100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(
                                        line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'SERVICIOS / PRUEBAS':
                            entra_categoria=1
                            if self.opportunity_id.prueba_bombeo.id == line.product_id.product_tmpl_id.id:
                                #comprueba si es una prueba de combeo DGA
                                if line.product_id.product_tmpl_id.id == 551:
                                    data.update({
                                        'price_unit': self.opportunity_id.x_insc_dga,
                                        'discount': 100 - ((100 - discount) * (
                                                100 - line.discount) / 100),
                                        'product_uom_qty': line.product_uom_qty,
                                        'product_id': line.product_id.id,
                                        'product_uom': line.product_uom_id.id,
                                        'customer_lead': self._get_customer_lead(
                                            line.product_id.product_tmpl_id),
                                        'last_update_price_date': line.product_id.product_tmpl_id.last_update_pricelist_date,
                                        'last_update_price_partner': line.product_id.product_tmpl_id.last_update_pricelist_partner,
                                        'utilidad_porcentaje': 0,
                                    })
                                else:
                                    data.update({
                                        'price_unit': self.opportunity_id.x_valorpb,
                                        'discount': 100 - ((100 - discount) * (
                                                100 - line.discount) / 100),
                                        'product_uom_qty': line.product_uom_qty,
                                        'product_id': line.product_id.id,
                                        'product_uom': line.product_uom_id.id,
                                        'customer_lead': self._get_customer_lead(
                                            line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'SERVICIOS':
                            entra_categoria=1
                            if line.product_id.product_tmpl_id.id == 546:                        
                                data.update({
                                    'price_unit': self.opportunity_id.x_faena,
                                    'discount': 100 - ((100 - discount) * (
                                            100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(
                                        line.product_id.product_tmpl_id),
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
                                    'discount': 100 - ((100 - discount) * (
                                            100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(
                                        line.product_id.product_tmpl_id),
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

                        if (line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / BOMBAS' or line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / KITS'):
                            entra_categoria=1
                            if self.opportunity_id.x_bomba_crm.id == line.product_id.product_tmpl_id.id:                        
                                data.update({
                                    'price_unit': price,
                                    'discount': 100 - ((100 - discount) * (
                                            100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(
                                        line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / MOTORES':
                            entra_categoria=1
                            if self.opportunity_id.x_motor_crm.id == line.product_id.product_tmpl_id.id:                        
                                data.update({
                                    'price_unit': price,
                                    'discount': 100 - ((100 - discount) * (
                                            100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(
                                        line.product_id.product_tmpl_id),
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

                        if (line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TABLEROS ELECTRICOS' or line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TABLEROS ELECTRICOS / MONOFASICO' or line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TABLEROS ELECTRICOS / TRIFASICO'):
                            entra_categoria=1
                            if self.opportunity_id.tablero.id == line.product_id.product_tmpl_id.id:                        
                                data.update({
                                    'price_unit': price,
                                    'discount': 100 - ((100 - discount) * (
                                            100 - line.discount) / 100),
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_id': line.product_id.id,
                                    'product_uom': line.product_uom_id.id,
                                    'customer_lead': self._get_customer_lead(
                                        line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TUBOS Y CAÑERIAS / PVC':                        
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': self.opportunity_id.x_impulsion,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TUBOS Y CAÑERIAS / V-WELL':                        
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': Math.ceil(self.opportunity_id.x_impulsion/3),
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / FITTING / PVC / TERMINALES':
                            if self.opportunity_id.x_impulsion%6>0:
                                cant_terminales = round((self.opportunity_id.x_impulsion/6)+0.5)
                            else:
                                cant_terminales = round(self.opportunity_id.x_impulsion/6)

                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': cant_terminales,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TUBOS Y CAÑERIAS / CONDUIT' and line.product_id.product_tmpl_id.id == 1573:                        
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': self.opportunity_id.x_impulsion,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'HERRAMIENTAS Y EQUIPOS / INSUMOS ELECTRICOS / CORDONES Y CABLES' and (line.product_id.product_tmpl_id.id == 498 or line.product_id.product_tmpl_id.id == 56 or line.product_id.product_tmpl_id.id == 497 or line.product_id.product_tmpl_id.id == 495 or line.product_id.product_tmpl_id.id == 496):                        
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': self.opportunity_id.x_impulsion+10,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.categ_id.display_name == 'HERRAMIENTAS Y EQUIPOS / INSUMOS ELECTRICOS / CORDONES Y CABLES' and line.product_id.product_tmpl_id.id == 55:                        
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': (self.opportunity_id.x_impulsion+10)*2,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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

                        if line.product_id.product_tmpl_id.id == 535:                        
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': self.opportunity_id.x_impulsion,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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

                        if entra_categoria==0 and seleccionado == 0:                        
                            data.update({
                                'price_unit': price,
                                'discount': 100 - ((100 - discount) * (
                                        100 - line.discount) / 100),
                                'product_uom_qty': line.product_uom_qty,
                                'product_id': line.product_id.id,
                                'product_uom': line.product_uom_id.id,
                                'customer_lead': self._get_customer_lead(
                                    line.product_id.product_tmpl_id),
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
                        'discount': 100 - ((100 - discount) * (
                                100 - line.discount) / 100),
                        'product_uom_qty': line.product_uom_qty,
                        'product_id': line.product_id.id,
                        'product_uom': line.product_uom_id.id,
                        'customer_lead': self._get_customer_lead(
                            line.product_id.product_tmpl_id),
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