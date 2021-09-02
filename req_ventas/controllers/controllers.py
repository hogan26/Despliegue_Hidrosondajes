# -*- coding: utf-8 -*-
# from odoo import http


# class ReqVentas(http.Controller):
#     @http.route('/req_ventas/req_ventas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/req_ventas/req_ventas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('req_ventas.listing', {
#             'root': '/req_ventas/req_ventas',
#             'objects': http.request.env['req_ventas.req_ventas'].search([]),
#         })

#     @http.route('/req_ventas/req_ventas/objects/<model("req_ventas.req_ventas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('req_ventas.object', {
#             'object': obj
#         })
