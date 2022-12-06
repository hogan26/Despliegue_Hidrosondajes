# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    def action_update_quotation(self):
        #raise ValidationError('probando boton')
        requerimiento = self.opportunity_id
        

        #VALIDACIONES PARA ACTUALIZAR ENCABEZADOS --- MODELO SALE.ORDER
        suma_metros = 0
        for calculo_profundidad in requerimiento.lead_matriz_lines_ids:
            suma_metros = suma_metros + calculo_profundidad.cantidad_metros
        
        self.update({'profundidad_calculada':suma_metros})        
        self.update({'duracion_servicio1':requerimiento.duracion_s1})
        
        if requerimiento.caudal_crm:
            self.update({'caudal_crm':requerimiento.caudal_crm})
        if requerimiento.caudal_text:
            self.update({'caudal_text':requerimiento.caudal_text})
        self.update({'duracion_s2':requerimiento.duracion_s2})
        
        if requerimiento.kits:                
            search_kit = self.env['product.product'].search([('name','=',requerimiento.kits.name)])
            search_kit = search_kit.name.lower()
            self.update({'kit_store':search_kit})            

        if requerimiento.bomba_crm:                
            search_bomba = self.env['product.product'].search([('name','=',requerimiento.bomba_crm.name)])
            search_bomba = search_bomba.name.lower()
            self.update({'bombas_store':search_bomba})
        
        if requerimiento.motor_crm:                
            search_motor = self.env['product.product'].search([('name','=',requerimiento.motor_crm.name)])
            search_motor = search_motor.name.lower()
            self.update({'motor_store':search_motor})

        if requerimiento.prueba_bombeo_crm:
            search_pbb = self.env['product.product'].search([('name','=',requerimiento.prueba_bombeo_crm.name)])
            search_pbb = search_pbb.name.lower()
            self.update({'prueba_bombeo_crm':search_pbb})        
            
        if requerimiento.bomba_centrifuga:
            search_bomba_cen = self.env['product.product'].search([('name','=',requerimiento.bomba_centrifuga.name)])
            aux_final = str(requerimiento.bomba_centrifuga.name).find('HP')
            aux_inicial = aux_final - 3
            self.update({'bomba_centrifuga':float(str(requerimiento.bomba_centrifuga.name[aux_inicial:aux_final]))})
        
        if requerimiento.estanque_hidroneumatico:
            search_est_hid = self.env['product.product'].search([('name','=',requerimiento.estanque_hidroneumatico.name)])
            aux_final = str(requerimiento.estanque_hidroneumatico.name).find('LT')
            aux_inicial = aux_final - 3
            self.update({'estanque_hidroneumatico':int(str(requerimiento.estanque_hidroneumatico.name[aux_inicial:aux_final]))})
        
        if requerimiento.x_duracion_s3:
            self.update({'duracion_s3':requerimiento.x_duracion_s3})
        
        if requerimiento.x_cloracion:
            self.update({'bomba_cloro':True})
        else:
            self.update({'bomba_cloro':False})
            
        if requerimiento.x_superficie:
            pre_string = ''
            if 'ESTANQUE VERTICAR ESTANDAR' in requerimiento.estanque_acumulacion_sup.name:
                pre_string = requerimiento.estanque_acumulacion_sup.name.replace('ESTANQUE VERTICAR ESTANDAR','')
                if 'LTS' in pre_string:
                    pre_string = pre_string.replace('LTS','')
                if '.' in pre_string:
                    pre_string = pre_string.replace('.','')
                    
            if 'ESTANQUE VERTICAR REFORZADO' in requerimiento.estanque_acumulacion_sup.name:
                pre_string = requerimiento.estanque_acumulacion_sup.name.replace('ESTANQUE VERTICAR REFORZADO','')
                if 'LTS' in pre_string:
                    pre_string = pre_string.replace('LTS','')
                if '.' in pre_string:
                    pre_string = pre_string.replace('.','')
                
            if pre_string:
                self.update({'estanque_acumulacion':int(str(pre_string))})
            
            
            # aux_final = str(requerimiento.estanque_acumulacion_sup.name).find('LTS')
            # aux_inicial = aux_final - 7
            # pre_string = requerimiento.estanque_acumulacion_sup.name[aux_inicial:aux_final].replace('.','')
            # self.update({'estanque_acumulacion':int(str(pre_string))})
        
        if requerimiento.x_enterrado_s3:
            pre_string = ''
            if 'ESTANQUE HORIZONTAL REFORZADO' in requerimiento.estanque_acumulacion_sup.name:
                pre_string = requerimiento.estanque_acumulacion_sup.name.replace('ESTANQUE HORIZONTAL REFORZADO','')
                if 'LTS' in pre_string:
                    pre_string = pre_string.replace('LTS','')
                if '.' in pre_string:
                    pre_string = pre_string.replace('.','')
                    
            if pre_string:
                self.update({'estanque_acumulacion':int(str(pre_string))})
            
            
            # aux_final = str(requerimiento.estanque_acumulacion_ent.name).find('LTS')
            # aux_inicial = aux_final - 7
            # pre_string = requerimiento.estanque_acumulacion_ent.name[aux_inicial:aux_final].replace('.','')
            # self.update({'estanque_acumulacion':int(str(pre_string))})
            
        if requerimiento.losa_hormigon:
            losa_name = requerimiento.losa_hormigon.name
            losa_split = losa_name.split()                    
            self.update({'losa_hormigon':losa_split[3]})

        # VALIDACIONES PARA ACUERDOS DE PAGO
        for acuerdo_pago in requerimiento.payment_agreed_matriz_ids:
            if acuerdo_pago.fijar_ac:
                self.update({'abono_porcentaje':acuerdo_pago.Abono_porcentaje})
                self.update({'abono_monto':acuerdo_pago.Abono_monto})
                self.update({'descuento_iva':acuerdo_pago.descuento_iva})
                self.update({'descuento_neto_porcentaje':acuerdo_pago.descuento_neto_porcentaje})
                self.update({'descuento_neto_monto':acuerdo_pago.descuento_neto_monto})
                self.update({'num_cuotas':acuerdo_pago.num_cuotas})
                self.update({'payment_method':acuerdo_pago.payment_method})
                self.update({'observaciones':acuerdo_pago.comentarios})                
                self.update({'total_tax_discount':acuerdo_pago.descuento_iva})
                self.update({'untaxed_percentage_discount':acuerdo_pago.descuento_neto_porcentaje})
                self.update({'untaxed_amount_discount':acuerdo_pago.descuento_neto_monto})

        for line in self.order_line:
            if line.display_type not in ['line_section','line_note']:                
                #_logger.info('product_id= {}'.format(line.product_template_id.id))
                #_logger.info('name= {}'.format(line.product_template_id.name))

                # VALIDACIONES PARA LINEAS DE PRESUPUESTO ----- MODELO ORDER.LINE
                
                #CHECKEO DE LINEA DE MATRIZ DE PERFORACION
                for matriz_perforacion in requerimiento.lead_matriz_lines_ids:
                    if matriz_perforacion.tipo_servicio_perforacion.id == line.product_template_id.id:
                        line.update({
                            'product_uom_qty':matriz_perforacion.cantidad_metros,
                            'price_unit':matriz_perforacion.valor_metro,
                        })

                        
                        
                # CAMPOS SELECCIONABLES EN FORMULARIO DE REQUERIMIENTOS
                if line.product_template_id.categ_id.display_name == 'SERVICIOS / PRUEBAS': #PRUEBA DE BOMBEO
                    if requerimiento.prueba_bombeo_crm.id: 
                        if requerimiento.prueba_bombeo_crm.id != 2211: 
                            search_pbb = self.env['product.product'].search([('name','=',requerimiento.prueba_bombeo_crm.name)])
                            line.update({
                                'name': search_pbb.name,
                                'price_unit': requerimiento.x_valorpb,                            
                                'product_id': search_pbb.id,                                    
                                'customer_lead': self._get_customer_lead(search_pbb),
                                'last_update_price_date': search_pbb.last_update_pricelist_date,
                                'last_update_price_partner': search_pbb.last_update_pricelist_partner,
                            })
                            
                if line.product_template_id.categ_id.display_name == 'OPERACIÓN BOMBEO / BOMBAS': #BOMBA
                    if requerimiento.bomba_crm.id:
                        search_bomba = self.env['product.product'].search([('name','=',requerimiento.bomba_crm.name)])
                        line.update({
                            'name': search_bomba.name,
                            'price_unit': search_bomba.list_price,                            
                            'product_id': search_bomba.id,                                    
                            'customer_lead': self._get_customer_lead(search_bomba),
                            'last_update_price_date': search_bomba.last_update_pricelist_date,
                            'last_update_price_partner': search_bomba.last_update_pricelist_partner,
                        })
                
                if line.product_template_id.categ_id.display_name == 'OPERACIÓN BOMBEO / MOTORES': #MOTOR
                    if requerimiento.motor_crm.id:
                        search_motor = self.env['product.product'].search([('name','=',requerimiento.motor_crm.name)])
                        line.update({
                            'name': search_motor.name,
                            'price_unit': search_motor.list_price,                            
                            'product_id': search_motor.id,                                    
                            'customer_lead': self._get_customer_lead(search_motor),
                            'last_update_price_date': search_motor.last_update_pricelist_date,
                            'last_update_price_partner': search_motor.last_update_pricelist_partner,
                        })
                        
                if line.product_template_id.categ_id.display_name == 'OPERACIÓN BOMBEO / KITS': #MOTOR
                    if requerimiento.kits.id:
                        search_kit = self.env['product.product'].search([('name','=',requerimiento.kits.name)])
                        line.update({
                            'name': search_kit.name,
                            'price_unit': search_kit.list_price,                            
                            'product_id': search_kit.id,                                    
                            'customer_lead': self._get_customer_lead(search_kit),
                            'last_update_price_date': search_kit.last_update_pricelist_date,
                            'last_update_price_partner': search_kit.last_update_pricelist_partner,
                        })
                        
                if line.product_template_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TUBOS Y CAÑERIAS / PVC': #TUBERIA DE PVC
                    line.update({
                        'product_uom_qty':requerimiento.x_impulsion,
                    })
                    
                if line.product_template_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TUBOS Y CAÑERIAS / V-WELL': #TUBERIA V-WELL
                    if requerimiento.x_impulsion%3>0:
                        calc_impulsion = round((requerimiento.x_impulsion/3)+0.5)
                    else:
                        calc_impulsion = round(requerimiento.x_impulsion/3)
                        
                    line.update({
                        'product_uom_qty':calc_impulsion,
                    })
                
                if line.product_template_id.categ_id.display_name == 'OPERACIÓN BOMBEO / FITTING / PVC / TERMINALES': #TERMINALES PVC
                    if requerimiento.x_impulsion%6>0:
                        cant_terminales = round((requerimiento.x_impulsion/6)+0.5)
                    else:
                        cant_terminales = round(requerimiento.x_impulsion/6)
                    
                    line.update({
                        'product_uom_qty':cant_terminales,
                    }) 
        
                if line.product_template_id.categ_id.display_name == 'OPERACIÓN BOMBEO / TUBOS Y CAÑERIAS / CONDUIT': #TUBERIA CONDUIT
                    line.update({
                        'product_uom_qty':requerimiento.x_impulsion,
                    })
                    
                if line.product_id.product_tmpl_id.id == 535:    #CUERDA DE POLIPROPILENO                     
                    line.update({                            
                        'product_uom_qty': requerimiento.x_impulsion,                            
                    })
                    
                if line.product_id.product_tmpl_id.categ_id.display_name == 'HERRAMIENTAS Y EQUIPOS / INSUMOS ELECTRICOS / CORDONES Y CABLES' and (line.product_id.product_tmpl_id.id == 498 or line.product_id.product_tmpl_id.id == 56 or line.product_id.product_tmpl_id.id == 497 or line.product_id.product_tmpl_id.id == 495 or line.product_id.product_tmpl_id.id == 496 or line.product_id.product_tmpl_id.id == 2352 or line.product_id.product_tmpl_id.id == 2353):  #CABLES PLANOS SUMERGIBLES                                                
                            
                    if requerimiento.hp_text:                            
                        if requerimiento.hp_text.find(',')!=-1:                            
                            hp_motor = float(requerimiento.hp_text.replace(',','.'))                                
                        else:
                            hp_motor = float(requerimiento.hp_text)
                    else:
                        hp_motor = requerimiento.x_hp_fl

                    if hp_motor <= 7.5 and line.product_id.product_tmpl_id.id == 495:                            
                        line.update({                                
                            'product_uom_qty': requerimiento.x_impulsion+5,                                
                        })                        

                    if hp_motor > 7.5 and hp_motor < 30 and line.product_id.product_tmpl_id.id == 56:                            
                        line.update({                                
                            'product_uom_qty': (requerimiento.x_altura*2)+5,                                
                        })                            

                    if hp_motor >= 30 and hp_motor < 50 and line.product_id.product_tmpl_id.id == 496:                            
                        line.update({                                
                            'product_uom_qty': (requerimiento.x_altura*2)+5,                                
                        })                        

                    if hp_motor >= 50 and hp_motor < 75 and line.product_id.product_tmpl_id.id == 497:                            
                        line.update({                                
                            'product_uom_qty': (requerimiento.x_altura*2)+5,                                
                        })                            

                    if hp_motor >= 75 and hp_motor < 100 and (line.product_id.product_tmpl_id.id == 498 or line.product_id.product_tmpl_id.id == 2352):                            
                        line.update({                                
                            'product_uom_qty': (requerimiento.x_altura*2)+5,                                
                        })                                                    

                    if hp_motor >= 100 and line.product_id.product_tmpl_id.id == 2353:                            
                        line.update({                                
                            'product_uom_qty': (requerimiento.x_altura*2)+5,                                
                        })

                if line.product_id.product_tmpl_id.categ_id.display_name == 'HERRAMIENTAS Y EQUIPOS / INSUMOS ELECTRICOS / CORDONES Y CABLES' and line.product_id.product_tmpl_id.id == 55:    #CABLE SONDA                     
                    line.update({                        
                        'product_uom_qty': (requerimiento.x_impulsion+5)*2,                        
                    })
    