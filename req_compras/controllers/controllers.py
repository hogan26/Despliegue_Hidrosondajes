# -*- coding: utf-8 -*-
# from odoo import http


# class ReqCompras(http.Controller):
#     @http.route('/req_compras/req_compras/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/req_compras/req_compras/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('req_compras.listing', {
#             'root': '/req_compras/req_compras',
#             'objects': http.request.env['req_compras.req_compras'].search([]),
#         })

#     @http.route('/req_compras/req_compras/objects/<model("req_compras.req_compras"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('req_compras.object', {
#             'object': obj
#         })
