# -*- coding: utf-8 -*-
from odoo import models, fields, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Vendors',
        domain=[('supplier_rank', '>', 0)],
        help='Select multiple vendors for this RFQ'
    )

    bid_count = fields.Integer(string='Bids', compute='_compute_bid_count')

    def _compute_bid_count(self):
        for order in self:
            order.bid_count = self.env['purchase.bid'].search_count([('order_id', '=', order.id)])

    def action_view_bids(self):
        self.ensure_one()
        action = self.env.ref('purchase_rfq_multi_vendor.action_purchase_bid').read()[0]
        action['domain'] = [('order_id','=',self.id)]
        return action

    def send_rfq_to_vendors(self):
        # Create invited bids for each vendor selected
        for vendor in self.vendor_ids:
            self.env['purchase.bid'].create({
                'order_id': self.id,
                'vendor_id': vendor.id,
                'state': 'invited',
            })
        return True
