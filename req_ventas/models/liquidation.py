# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    def action_liquidation(self):
        #ESTA FUNCION DEBE REALIZAR LAS SIGUIENTES OPERACIONES:
        #1 - CAMBIAR EL ESTADO DEL FORMULARIO DE CIERRE A 'LIQUIDADO'
        #2 - PASAR EL REQUERIMIENTO A LA SIGUIENTE ETAPA
        #3 - SETEAR EL CODIGO DE LA LIQUIDACION EN LOS PICKINGS UTILIZADOS PARA LIQUIDAR, DEJANDO ASI DE CONSIDERARLOS PENDIENTES
        #4 - VERIFICAR SI AUN QUEDAN LIQUIDACIONES PENDIENTES
        
        #PASO 1: CAMBIAR EL ESTADO DEL FORMULARIO DE CIERRE A 'LIQUIDADO'
        self.write({'state_settlement':'liquidar'})
        
        #PASO 2: PASAR EL REQUERIMIENTO A LA SIGUIENTE ETAPA
        siguiente_etapa = self.env['crm.stage'].search([('name','=','LIQUIDADO')])
        if self.opportunity_id:
            opportunity_id = self.env['crm.lead'].search([('id','=',self.opportunity_id.id)])
            opportunity_id.write({'stage_id':siguiente_etapa.id})
            
        #PASO 3: SETEAR EL CODIGO DE LA LIQUIDACION EN LOS PICKINGS UTILIZADOS PARA LIQUIDAR
            select_process = self.pending_settlements_select
            settlement_services = []
            if select_process == 's1s2':
                settlement_services = ['s1','s2']
            elif select_process == 's1s2s3':
                settlement_services = ['s1','s2','s3']
            elif select_process == 's2s3':
                settlement_services = ['s2','s3']
            else:
                settlement_services.append(self.pending_settlements_select)
                
            for sale_order in opportunity_id.order_ids:
                if sale_order.state=="sale":
                    for picking_id in sale_order.picking_ids:
                        if picking_id.state == 'done':
                            closure_pickings = self.env['stock.picking'].search([('id','!=',picking_id.id),('servicio_reservado','=',picking_id.servicio_reservado),('origin','=',sale_order.name),('state','=','done')])
                            if closure_pickings:
                                for closure_picking in closure_pickings:
                                    if closure_picking.servicio_reservado in settlement_services:
                                        closure_picking.write({'settlement_code':self.name})
                                    else:
                                        continue
            
        #PASO 4: VERIFICAR SI AUN QUEDAN LIQUIDACIONES PENDIENTES
            pending_settlement = False
            for sale_order in opportunity_id.order_ids:
                if sale_order.state=="sale":
                    for picking_id in sale_order.picking_ids:
                        if picking_id.state == 'done':
                            closure_pickings = self.env['stock.picking'].search([('id','!=',picking_id.id),('servicio_reservado','=',picking_id.servicio_reservado),('origin','=',sale_order.name),('service_shutdown_creator','!=',False),('state','=','done')])
                            if closure_pickings:
                                for closure_picking in closure_pickings:
                                    if not(closure_picking.settlement_code):
                                        pending_settlement = True
                                    else:
                                        continue
            if pending_settlement:
                opportunity_id.write({'pending_settlements':True,
                                      'color_settlement':1})
            else:
                opportunity_id.write({'pending_settlements':False,
                                      'color_settlement':0})
    
    def load_settlements_products(self):
        #PASO 1: TRATAMIENTO DE OPCIONES A LIQUIDAR, LA SELECCION POR DEFECTO VENDRÁ DADA POR UN CALCULO AL MOMENTO DE CREAR EL FORMULARIO
        if self.opportunity_id:
            select_process = self.pending_settlements_select
            settlement_services = []
            if select_process == 's1s2': settlement_services = ['s1','s2']
            elif select_process == 's1s2s3': settlement_services = ['s1','s2','s3']
            elif select_process == 's2s3': settlement_services = ['s2','s3']
            else: settlement_services.append(self.pending_settlements_select)

            #VALIDACION
            if settlement_services == 'no':
                raise ValidationError("Error al cargar productos, al parecer no hay servicios pendientes por liquidar")
            else:
                #PASO 2: PROCESAR LAS COTIZACIONES CONFIRMADAS DEL REQUERIMIENTO, EL FORMULARIO DE LIQUIDACION ESTA VINCULADO AL REQUERIMIENTO
                opportunity_id = self.env['crm.lead'].search([('id','=',self.opportunity_id.id)])
                if opportunity_id:
                    for sale_order in opportunity_id.order_ids:
                        if sale_order.state=="sale":
                            #PASO 3: TRASPADO DE CAMPOS REQUERIDOS
                            self.update({'partner_invoice_id':sale_order.partner_invoice_id,
                                         'partner_shipping_id':sale_order.partner_shipping_id,
                                        'pricelist_id':sale_order.pricelist_id})
                            #PASO 4: SEPARACION DE PRODUCTOS POR SECCION TAL COMO VIENE EN LA COTIZACION CONFIRMADA ORIGINAL, PARA ESTO HACEMOS
                            #USO DEL CAMPO SERVICIOS REQUERIDOS PARA IDENTIFICAR CUANTAS SECCIONES CONTIENE Y EL ORDEN DE ESTOS.
                            servicios_requeridos = sale_order.x_servicios_requeridos
                            filtro_servicios = []
                            if servicios_requeridos == 's1s2': filtro_servicios = ['s1','s2']
                            elif servicios_requeridos == 's1s2s3': filtro_servicios = ['s1','s2','s3']
                            elif servicios_requeridos == 's2s3': filtro_servicios = ['s2','s3']
                            else: filtro_servicios.append(self.pending_settlements_select)
                            
                            #PASO 5: IDENTIFICAR LAS CARACTERISTICAS IMPORTANTES DE CADA LINEA DE LA COTIZACION Y CUAL ES LA ULTIMA LINEA
                            line_detail = []
                            for order_line in sale_order.order_line:
                                if order_line.product_id.id and not(order_line.display_type):
                                    line_detail.append({'display_type':'product','line_id':order_line.id})
                                else:
                                    if order_line.display_type!='line_note':
                                        line_detail.append({'display_type':'section_note','line_id':'no'})                            
                            
                            #PASO 6: DETERMINAR DONDE EMPIEZA Y TERMINA CADA SECCION Y A QUE SERVICIO CORRESPONDE
                            section,start,end = 0,0,0                            
                            section_range = []
                            last_element = line_detail[-1]
                            service_index = 0  # sirve como variable de control para asignar el tipo de servicio reservado al picking
                            for section_detail in line_detail:
                                if section_detail['display_type'] == 'section_note':
                                    section = section + 1
                                    if section > 0 and end > 0:
                                        # la cotizacion tiene secciones pero no empieza con una
                                        section_range.append({'start': start, 'end': end, 'type': filtro_servicios[service_index]})
                                        service_index = service_index + 1
                                        end = end + 1
                                        start = end + 1
                                    if section > 0 and end == 0:
                                        # la cotizacion tiene secciones y empieza con una, la primera seccion no genera corte
                                        start = start + 1
                                        continue
                                else:
                                    end = end + 1
                                    if section_detail == last_element:  #ultimo elemento de la cotizacion para generar el ultimo corte
                                        section_range.append({'start': start, 'end': end, 'type': filtro_servicios[service_index]})
                                        service_index = service_index + 1
                                        
                            #ITERACION PARA COMPROBAR SI RANGOS DE SECCIONES ESTAN CALCULADOS CORRECTAMENTE (FALTA CALCULAR CON 3 SERVICIOS)
#                             for verification_section_array in section_range:
#                                 _logger.info('start = {}, end = {}, type = {}'.format(verification_section_array['start'],verification_section_array['end'],verification_section_array['type']))

                            #PASO 7: CARGAR LAS LINEAS DE LA COTIZACION AL FORMULARIO DE LIQUIDACION SOLICITADAS POR EL SELECT SETTLEMENTS_SERVICES

                            #modificacion 1: ver si es mejor que cargue las lineas y despues actualice y elimine o que solo cargue lo del cierre,
                            #para esto tener en consideracion los productos de tipo servicio.
                            
                            for section_line in section_range:
                                line_index = 0
                                if section_line['type'] in settlement_services:                                    
                                    for settlement_line in sale_order.order_line: 
                                        if line_index<section_line['start']:
                                            line_index += 1
                                            continue
                                        elif line_index >= section_line['start'] and line_index<=section_line['end']:
                                            self.write({
                                                'order_line': [(0, 0, {
                                                    'product_id': settlement_line.product_id.id,
                                                    'name': settlement_line.name,
                                                    'product_uom_qty': settlement_line.product_uom_qty,
                                                    'sale_qty': settlement_line.product_uom_qty,
                                                    'product_uom': settlement_line.product_uom.id,
                                                    'price_unit': settlement_line.price_unit,
                                                    'utilidad_porcentaje': settlement_line.utilidad_porcentaje,
                                                    'precio_venta': settlement_line.precio_venta,
                                                    'tax_id': settlement_line.tax_id,
                                                    'last_update_price_date': settlement_line.last_update_price_date,
                                                    'last_update_price_partner': settlement_line.last_update_price_partner,
                                                    'last_update_type_selector': settlement_line.last_update_type_selector,
                                                    'number_days_context': settlement_line.number_days_context,
                                                    'discount': settlement_line.discount,
                                                    'price_subtotal': settlement_line.price_subtotal,
                                                    'margen_total': settlement_line.margen_total,
                                                    'settlement_line': True,
                                                    'customer_lead': settlement_line.customer_lead,
                                                })]
                                            })
                                            if line_index == section_line['end']: break
                                            else: line_index += 1
                            
                            #PASO 8: CARGADAS LAS LINEAS, RECORRER LOS PICKINGS DE CIERRE CONFIRMADOS PARA ACTUALIZAR LAS CANTIDADES DE LA
                            #LIQUIDACION CON LAS CANTIDADES CONSUMIDAS, DE MANERA QUE LA INFORMACION DE LA LIQUIDACION SEA FIDEDIGNA AL CIERRE

                            #modificacion 2: al buscar los pickings, no tiene que estar con el state en done
                            
                            for picking_id in sale_order.picking_ids:
                                # if picking_id.state == 'done':
                                # closure_pickings = self.env['stock.picking'].search([('id','!=',picking_id.id),('servicio_reservado','=',picking_id.servicio_reservado),('origin','=',sale_order.name),('service_shutdown_creator','!=',False),('state','=','done')])
                                closure_pickings = self.env['stock.picking'].search([('id','!=',picking_id.id),('servicio_reservado','=',picking_id.servicio_reservado),('origin','=',sale_order.name),('service_shutdown_creator','!=',False)])
                                if closure_pickings:
                                    for closure_picking in closure_pickings:                                        
                                        if not(closure_picking.settlement_code) and closure_picking.servicio_reservado in settlement_services:
                                            #PASO 9: SI EL PRODUCTO DE LA COTIZACION ESTA EN EL PICKING SE ACTUALIZA LA CANTIDAD, SI EL PRODUCTO
                                            #ESTA EN EL PICKING Y NO EN LA COTIZACION Y NO CORRESPONDE A UN PRODUCTO DE SERVICIO 1, SE DEBE AÑADIR,
                                            #SI SE SOLICITA QUE UN/OS PRODUCTOS NUNCA SE AÑADAN A PESAR DE LA DIFERENCIA, CREAR UNA VALIDACION EN 
                                            #ESTA PARTE DEL CODIGO                                            
                                            if closure_picking.servicio_reservado == 's1':
                                                #PASO 10: VERIFICAMOS LA VARIEDAD DE PULGADAS EXISTENTES, EN CASO QUE SEA UN POZO TELESCOPICO
                                                variedad_pulgadas = []
                                                for picking_line in closure_picking.move_line_ids_without_package:
                                                    if picking_line.product_id.categ_id.display_name == "OPERACIÓN PERFORACIÓN / TUBOS Y CAÑERIAS / ACERO CARBONO" and picking_line.product_id.inches:
                                                        if picking_line.product_id.inches not in variedad_pulgadas:
                                                            variedad_pulgadas.append(picking_line.product_id.inches)
                                                
                                                #PASO 11: DETECTADA LA VARIEDAD DE PULGADAS, CREAMOS UN DICCIONARIO PARA ALMACENAR LA SUMA POR
                                                #PULGADAS
                                                diccionario_pulgadas = []
                                                if len(variedad_pulgadas)>0:
                                                    for medida_pulgadas in variedad_pulgadas:
                                                        diccionario_pulgadas.append({'medida_pulgadas':medida_pulgadas,
                                                                                    'suma_total':0})
                                                #PASO 12: RECORREMOS LOS PRODUCTOS DEL PICKING IDENTIFICANDO SU MEDIDA DE PULGADAS Y HACEMOS LA 
                                                #SUMATORIA, ESTO SIRVE PARA IDENTIFICAR UNA DIFERENCIA ENTRE LA PROFUNDIDAD COTIZADA Y LA CERRADA
                                                if len(diccionario_pulgadas)>0:
                                                    for picking_line in closure_picking.move_line_ids_without_package:
                                                        if picking_line.product_id.categ_id.display_name == "OPERACIÓN PERFORACIÓN / TUBOS Y CAÑERIAS / ACERO CARBONO" and picking_line.product_id.inches:
                                                            index = 0                                                                
                                                            for medida_pulgadas in variedad_pulgadas:
                                                                if diccionario_pulgadas[index]['medida_pulgadas'] == picking_line.product_id.inches:
                                                                    diccionario_pulgadas[index]['suma_total'] += picking_line.qty_done
                                                                    index += 1
                                                                else:
                                                                    index += 1
                                                                    continue

                                                    #COMPROBAMOS QUE LA SUMA POR PULGADAS SE ESTA CALCULANDO CORRECTAMENTE
#                                                         for validation_data in diccionario_pulgadas:
#                                                             _logger.info('medida_pulgadas = {}, suma_total = {}'.format(validation_data['medida_pulgadas'],validation_data['suma_total']))

                                                #PASO 13: RECORREMOS LOS PRODUCTOS DE LA COTIZACION BUSCANDO LOS PRODUCTOS TIPO SERVICIO Y
                                                #ACTUALIZAMOS SU CANTIDAD CON LA SUMA POR PULGADAS CALCULADA ANTERIORMENTE
                                                for order_line in self.order_line:                                                        
                                                    if order_line.product_id.categ_id.display_name == 'SERVICIOS / PERFORACION':
                                                        for asignacion_suma in diccionario_pulgadas:
                                                            if order_line.product_id.inches == asignacion_suma['medida_pulgadas']:
                                                                order_line.write({'product_uom_qty':asignacion_suma['suma_total']})
                                                            else: continue
                                                    elif order_line.product_id.categ_id.display_name == 'OPERACIÓN PERFORACIÓN / HERRAMIENTAS PERFORACIÓN / CORONAS':
                                                        #PASO 14: SI ENCONTRAMOS UNA CORONA, VAMOS A REVISAR EL PICKING SI ESTA ESA MISMA CORONA Y
                                                        #ACTUALIZAMOS LA CANTIDAD, SI ENCONTRAMOS UNA CORONA DISTINTA PERO DE LA MISMA MEDIDA
                                                        #EN PULGADAS LA AGREGAMOS A LA LIQUIDACION (EN CASO QUE SUCEDIERA UN CAMBIO/CORTE DE
                                                        #CORONA)                                                            
                                                        for picking_line in closure_picking.move_line_ids_without_package:
                                                            if picking_line.product_id.categ_id.display_name == 'OPERACIÓN PERFORACIÓN / HERRAMIENTAS PERFORACIÓN / CORONAS':
                                                                if picking_line.product_id.id == order_line.product_id.id:
                                                                    order_line.write({'product_uom_qty':picking_line.qty_done})
                                                                elif picking_line.product_id.inches == order_line.product_id.inches:
                                                                    self.write({
                                                                        'order_line': [(0, 0, {
                                                                            'product_id': picking_line.product_id.id,
                                                                            'name': picking_line.product_id.product_tmpl_id.name,
                                                                            'product_uom_qty': picking_line.qty_done,
                                                                            'product_uom': picking_line.product_id.product_tmpl_id.uom_id.id,
                                                                            'price_unit': picking_line.product_id.product_tmpl_id.list_price,
                                                                            'utilidad_porcentaje': 45,
                                                                            'tax_id': picking_line.product_id.product_tmpl_id.taxes_id,
                                                                            'last_update_price_date': picking_line.product_id.product_tmpl_id.last_update_pricelist_date,
                                                                            'last_update_price_partner': picking_line.product_id.product_tmpl_id.last_update_pricelist_partner,
                                                                            'last_update_type_selector': picking_line.product_id.product_tmpl_id.last_update_type_selector,
                                                                            'last_update_number_days': picking_line.product_id.product_tmpl_id.last_update_number_days,
                                                                            'discount': 0,
                                                                            'customer_lead': self._get_customer_lead(picking_line.product_id.product_tmpl_id),
                                                                        })]
                                                                    })
                                                    else: continue
                                            else:
                                                #PASO 15: SI EL PICKING QUE SE ESTA ANALIZANDO NO ES DE SERVICIO 1, ENTONCES SE DEBE ACTUALIZAR LA
                                                #CANTIDAD DE TODOS LOS PRODUCTOS QUE ESTEN EN LA LIQUIDACION CON LA CANTIDAD DE LOS PRODUCTOS DEL
                                                #PICKING, SI UN PRODUCTO ESTA EN EL PICKING DE CIERRE Y NO EN LA LIQUIDACION, SE DEBEN AÑADIR
                                                for section_line in section_range:
                                                    #VERIFICAMOS QUE SE HARA RECORRIDO SOLO DE LOS PRODUCTOS DE LA LIQUIDACION QUE CORRESPONDEN CON
                                                    #EL SERVICIO DEL PICKING DE CIERRE A ANALIZAR
                                                    if section_line['type'] == closure_picking.servicio_reservado:
                                                        #CREAMOS UN ARRAY PARA ALMACENAR LOS PRODUCT_ID YA REVISADOS PARA EVITAR REPETIR EL PROCESO
                                                        #DE ACTUALIZACION DE CANTIDAD EN PRODUCTOS QUE SE REPITEN EN LA LIQUIDACION
                                                        product_id_list = []
                                                        number_lines = (section_line['end'] - section_line['start']) + 1
                                                        lines_limit = section_line['end']
                                                        line_start = lines_limit - number_lines
                                                        for picking_line in closure_picking.move_line_ids_without_package:
                                                            encontrado = False
                                                            line_index = 1                                                                
                                                            for order_line in self.order_line:
                                                                if line_index<line_start:
                                                                    line_index += 1
                                                                    continue
                                                                else:
                                                                    if order_line.product_id.id not in product_id_list:
                                                                        if picking_line.product_id.id == order_line.product_id.id:
                                                                            _logger.info('producto encontrado, name = {}'.format(picking_line.product_id.name))
                                                                            order_line.write({'product_uom_qty': picking_line.qty_done})
                                                                            encontrado = True
                                                                            product_id_list.append(picking_line.product_id.id)
                                                                            if line_index == lines_limit: break
                                                                            else:
                                                                                line_index += 1
                                                                                continue
                                                                        else:
                                                                            if line_index == lines_limit: break
                                                                            else:
                                                                                line_index += 1
                                                                                continue    
                                                                    else:
                                                                        if line_index == lines_limit: break
                                                                        else:
                                                                            line_index += 1
                                                                            continue
                                                                    
                                                            if encontrado == False:
                                                                _logger.info('producto no encontrado, name = {}'.format(picking_line.product_id.name))
                                                                self.write({
                                                                    'order_line': [(0, 0, {
                                                                        'product_id': picking_line.product_id.id,
                                                                        'name': picking_line.product_id.product_tmpl_id.name,
                                                                        'product_uom_qty': picking_line.qty_done,
                                                                        'product_uom': picking_line.product_id.product_tmpl_id.uom_id.id,
                                                                        'price_unit': picking_line.product_id.product_tmpl_id.list_price,
                                                                        'utilidad_porcentaje': 45,
                                                                        'tax_id': picking_line.product_id.product_tmpl_id.taxes_id,
                                                                        'last_update_price_date': picking_line.product_id.product_tmpl_id.last_update_pricelist_date,
                                                                        'last_update_price_partner': picking_line.product_id.product_tmpl_id.last_update_pricelist_partner,
                                                                        'last_update_type_selector': picking_line.product_id.product_tmpl_id.last_update_type_selector,
                                                                        'last_update_number_days': picking_line.product_id.product_tmpl_id.last_update_number_days,
                                                                        'settlement_added_product': True,
                                                                        'settlement_line': True,
                                                                        'discount': 0,
                                                                        'customer_lead': self._get_customer_lead(picking_line.product_id.product_tmpl_id),
                                                                    })]
                                                                })
                                else: continue
                else: raise ValidationError("No se pudo encontrar el requerimiento")
    
    
    state = fields.Selection(selection_add=[('cerrar','Cerrado'),('liquidar', 'Liquidado')])
    state_settlement = fields.Selection([('cerrar','Cerrado'),('liquidar', 'Liquidado')],string="Estado liquidación")
    encabezado_liquidacion = fields.Html(string='Titulo principal')
    detalle_abonos_liquidacion = fields.Html(string='Detalle abonos')
    pending_settlements_select = fields.Selection([('s1','S1'),('s2','S2'),('s3','S3'),('s4','S4'),('s1s2','S1 + S2'),('s1s2s3','S1 + S2 + S3'),('s2s3','S2 + S3'),('no','No hay')],string="Liquidaciones pendientes") 
    order_lines_special_view = fields.Boolean(string="Vista tree especial",default=False)
    order_lines_special_view2 = fields.Boolean(string="Vista tree especial.")
    partner_invoice_id = fields.Many2one(
        'res.partner', string='Invoice Address',
        readonly=True, required=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)], 'cerrar': [('readonly', False)], 'liquidar': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    partner_shipping_id = fields.Many2one(
        'res.partner', string='Delivery Address', readonly=True, required=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)], 'cerrar': [('readonly', False)], 'liquidar': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist', check_company=True,  # Unrequired company
        required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'cerrar': [('readonly', False)], 'liquidar': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="If you change the pricelist, only newly added lines will be affected.")