# -*- coding: utf-8 -*-
# from odoo import http


# class ReqCrm(http.Controller):
#     @http.route('/req_crm/req_crm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/req_crm/req_crm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('req_crm.listing', {
#             'root': '/req_crm/req_crm',
#             'objects': http.request.env['req_crm.req_crm'].search([]),
#         })

#     @http.route('/req_crm/req_crm/objects/<model("req_crm.req_crm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('req_crm.object', {
#             'object': obj
#         })
