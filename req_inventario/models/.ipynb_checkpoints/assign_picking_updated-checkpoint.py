# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from itertools import groupby
from odoo.exceptions import UserError
from odoo.addons.stock.models.stock_move import StockMove as OriginalStockMove

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _assign_picking(self):
        Picking = self.env['stock.picking']
        grouped_moves = groupby(sorted(self, key=lambda m: [f.id for f in m._key_assign_picking()]),key=lambda m: [m._key_assign_picking()])
        for group, moves in grouped_moves:
            moves = self.env['stock.move'].concat(*list(moves))
            new_picking = False
            picking = moves[0]._search_picking_for_assignation()
            if picking:
                if any(picking.partner_id.id != m.partner_id.id or picking.origin != m.origin for m in moves):
                    picking.write({
                        'partner_id': False,
                        'origin': False,
                    })
            else:
                if moves.sale_line_id.order_id.opportunity_id:
                    opportunity_id = moves.sale_line_id.order_id.opportunity_id.id
                    sale_order_id = moves.sale_line_id.order_id.id
                    sale_order = self.env['sale.order'].search([('id', '=', sale_order_id)])
                    order_lines = []
                    # analizamos las lineas del presupuesto e identificamos la posicion de las secciones
                    for lines in sale_order.order_line:
                        if lines.product_id.id and not (lines.display_type):
                            if lines.product_type!='service':
                                order_lines.append({'display_type': lines.display_type, 'product_id': lines.product_id.id})
                        else:
                            order_lines.append({'display_type': 'section_note', 'product_id': 0})

                    # identificamos que servicios fueron requeridos en el presupuesto
                    servicios_requeridos = sale_order.x_servicios_requeridos

                    if servicios_requeridos == 's1':
                        servicios_requeridos_array = ['s1']
                    if servicios_requeridos == 's2':
                        servicios_requeridos_array = ['s2']
                    if servicios_requeridos == 's3':
                        servicios_requeridos_array = ['s3']
                    if servicios_requeridos == 's4':
                        servicios_requeridos_array = ['s4']
                    if servicios_requeridos == 's1s2':
                        servicios_requeridos_array = ['s1', 's2']
                    if servicios_requeridos == 's2s3':
                        servicios_requeridos_array = ['s2', 's3']
                    if servicios_requeridos == 's1s2s3':
                        servicios_requeridos_array = ['s1', 's2', 's3']

                    section = 0
                    start = 0
                    end = 0
                    slices = []
                    last_element = order_lines[-1]
                    service_index = 0  # sirve como variable de control para asignar el tipo de servicio reservado al picking
                    # creamos los grupos de productos basandose en la posicion de las secciones
                    for compute_slice in order_lines:
                        if compute_slice['display_type'] == 'section_note':
                            section = section + 1
                            if section > 0 and end > 0:
                                # la cotizacion tiene secciones pero no empieza con una
                                slices.append({'start': start, 'end': end, 'type': servicios_requeridos_array[service_index]})
                                service_index = service_index + 1
                                start = end
                            if section > 0 and end == 0:
                                # la cotizacion tiene secciones y empieza con una, la primera seccion no genera corte
                                continue
                        else:
                            end = end + 1
                            if compute_slice == last_element:  # verifica que sea el ultimo elemento de la cotizacion para generar el ultimo corte
                                slices.append({'start': start, 'end': end, 'type': servicios_requeridos_array[service_index]})
                                service_index = service_index + 1

                    # busqueda y cancelacion de picking que estan en espera en cotizacion confirmada anterior y que coinciden que picking del mismo
                    # servicio de la cotizacion confirmada en curso.

                    sales_orders_confirmed = self.env['sale.order'].search([('id', '!=', sale_order_id), ('opportunity_id', '=', opportunity_id), ('state', '=', 'sale')])
                    if sales_orders_confirmed:
                        for sale_order_analisis in sales_orders_confirmed:  # recorre los presupuestos
                            for picking_analisis in sale_order_analisis.picking_ids:  # recorre los pickings de cada presupuestos
                                if picking_analisis.servicio_reservado and picking_analisis.state in ['confirmed','assigned']:#val. pre-comp.
                                    for service_comparison in slices:  # preparacion para comparacion
                                        if picking_analisis.servicio_reservado == service_comparison['type']:  # comparacion
                                            # llamamos a la funcion que cancela el picking
                                            picking_analisis.action_cancel()

                    # creamos los pickings con los productos separados por servicios incluidos
                    for pickings in slices:
                        new_picking = True
                        picking = Picking.create(moves[slice(pickings['start'], pickings['end'])]._get_new_picking_values())
                        # luego de crear el picking, asignamos el tipo de servicio que servira como validacion para el siguiente proceso
                        picking.write({'servicio_reservado': pickings['type']})
                        moves[slice(pickings['start'], pickings['end'])].write({'picking_id': picking.id})
                        moves[slice(pickings['start'], pickings['end'])]._assign_picking_post_process(new=new_picking)
                        picking.action_assign()

                else:
                    new_picking = True
                    picking = Picking.create(moves._get_new_picking_values())
                    location_dest_id = self.env['stock.location'].search([('complete_name','=',moves.sale_line_id.order_id.x_equipo_asignado+'/Stock')])
                    picking.write({
                        'servicio_reservado': moves.sale_line_id.order_id.service,
                        'origin':moves.sale_line_id.order_id.origin_sale_order,
                        'ot_origen':moves.sale_line_id.order_id.name,
                        'location_dest_id':location_dest_id.id
                                  })
                    moves.write({'picking_id': picking.id})
                    moves._assign_picking_post_process(new=new_picking)
                    
#                     moves.sale_line_id.order_id.service

                    # funcion que consolida la reserva generada por la orden de trabajo y la reserva generada por la cotizacion vinculada
                    current_ot = moves.sale_line_id.order_id  # tomamos la ot en curso
                   
                    if current_ot.origin_sale_order and not(current_ot.ot_origen):
                        # vamos a buscar la cotizacion desde la cual viene la ot
                        linked_sale_order = self.env['sale.order'].search([('name','=',current_ot.origin_sale_order)])  
                        for pickings in linked_sale_order.picking_ids:  # vamos a buscar los pickings de la cotizacion
                            if pickings.state in ['confirmed', 'assigned']:  # los que estan en estado de espera
                                # validamos si el picking que esta creando la ot corresponde al picking del mismo servicio de la cotizacion
                                if pickings.servicio_reservado == current_ot.service: 
                                    pickings.write({'ot_origen': current_ot.name})
                                    # pickings = picking del presupuesto
                                    # picking = picking de la ot (recien creado)
                                    for move_lines_picking_ot in picking.move_lines:
                                        encontrado = False
                                        for move_lines_picking_presupuesto in pickings.move_lines:
                                            if move_lines_picking_ot.product_id == move_lines_picking_presupuesto.product_id:
                                                encontrado = True
                                                datos_para_actualizar = move_lines_picking_ot
                                                linea_a_actualizar = move_lines_picking_presupuesto

                                        if encontrado == True:  # hay que actualizar product_uom_qty
                                            line_to_update = self.env['stock.move'].search([('id', '=', linea_a_actualizar.id)])
                                            line_to_update.write({'product_uom_qty': datos_para_actualizar.product_uom_qty})
                                        else:  # hay que agregar un product_id y product_uom_qty
                                            picking_to_modify = self.env['stock.picking'].search([('id', '=', pickings.id)])
                                            picking_to_modify.write({
                                                'move_lines': [(0, 0, {
                                                    'product_id': move_lines_picking_ot.product_id.id,
                                                    'product_uom_qty': move_lines_picking_ot.product_uom_qty,
                                                    'name': move_lines_picking_ot.product_id.name,
                                                    'product_uom': move_lines_picking_ot.product_uom.id,
                                                    'location_id': move_lines_picking_ot.location_id.id,
                                                    'location_dest_id': move_lines_picking_ot.location_dest_id.id
                                                })]
                                            })
                                    #finalizado el proceso llamar a action confirm para accionar el boton "marcar 'por realizar'" lo que cambia
                                    #el estado de 'borrador'->'en espera' haciendo que el picking aparezca en la seccion 'a procesar' en la
                                    #seccion 'ordenes de entrega' de la vista principal 
                                    pickings.action_confirm()                                    
                                    pickings.action_assign()
                                    
                        # luego llamar a la funcion action_cancel pasando picking como id del record
                        picking.action_cancel()                                    
                        

        OriginalStockMove._assign_picking = self._assign_picking
        return True


class Picking(models.Model):
    _inherit = 'stock.picking'

    servicio_reservado = fields.Selection([('s1', 'S1'), ('s2', 'S2'), ('s3', 'S3'), ('s4', 'S4'), ('ot', 'OT')],
                                          string='Servicio Reservado')
    location_dest_id = fields.Many2one(
        'stock.location', "Destination Location",
        default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_dest_id,
        check_company=True, readonly=True, required=True,
        states={'draft': [('readonly', False)]})
    ot_origen = fields.Char(string="Codigo OT")
    service_shutdown_creator = fields.Char(string='Operador')

    def action_load_stock_origin_location(self):
        stock_origin_location = self.env['stock.location'].search([('id','=',self.location_id.id)])
        for cantidades in stock_origin_location.quant_ids:            
            self.update({
                'move_line_ids': [(0, 0, {
                    'product_id': cantidades.product_id.id,
                    'qty_done': cantidades.quantity,
                    'product_uom_id': cantidades.product_uom_id.id,
                    'location_id': cantidades.location_id.id,
                    'location_dest_id': self.location_dest_id.id
                })]
            })
            
    @api.onchange('location_dest_id')
    def onchange_location_dest_id(self):
        for picking_line in self.move_line_ids_without_package:
            picking_line.update({
                'location_dest_id':self.location_dest_id.id
            })