# -*- coding: utf-8 -*-
# from odoo import http


# class ReqInventario(http.Controller):
#     @http.route('/req_inventario/req_inventario/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/req_inventario/req_inventario/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('req_inventario.listing', {
#             'root': '/req_inventario/req_inventario',
#             'objects': http.request.env['req_inventario.req_inventario'].search([]),
#         })

#     @http.route('/req_inventario/req_inventario/objects/<model("req_inventario.req_inventario"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('req_inventario.object', {
#             'object': obj
#         })
