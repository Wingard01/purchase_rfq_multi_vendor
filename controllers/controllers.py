# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseRfqMultiVendor(http.Controller):
#     @http.route('/purchase_rfq_multi_vendor/purchase_rfq_multi_vendor', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_rfq_multi_vendor/purchase_rfq_multi_vendor/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_rfq_multi_vendor.listing', {
#             'root': '/purchase_rfq_multi_vendor/purchase_rfq_multi_vendor',
#             'objects': http.request.env['purchase_rfq_multi_vendor.purchase_rfq_multi_vendor'].search([]),
#         })

#     @http.route('/purchase_rfq_multi_vendor/purchase_rfq_multi_vendor/objects/<model("purchase_rfq_multi_vendor.purchase_rfq_multi_vendor"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_rfq_multi_vendor.object', {
#             'object': obj
#         })

