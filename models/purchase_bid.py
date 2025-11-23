# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class PurchaseBid(models.Model):
    _name = 'purchase.bid'
    _description = 'Purchase Bid'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    name = fields.Char('Reference', required=True, copy=False, default='New')
    order_id = fields.Many2one('purchase.order', string='RFQ', required=True, ondelete='cascade', index=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True, domain="[('supplier_rank','>',0)]")
    date = fields.Datetime(string='Received On', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft','Draft'),
        ('invited','Invited'),
        ('submitted','Submitted'),
        ('accepted','Accepted'),
        ('rejected','Rejected'),
    ], default='draft', tracking=True)
    note = fields.Text(string='Notes')
    bid_line_ids = fields.One2many('purchase.bid.line','bid_id', string='Lines')
    total = fields.Monetary(string='Total', currency_field='currency_id', compute='_compute_total', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', related='order_id.currency_id', store=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            seq = self.env['ir.sequence'].next_by_code('purchase.bid') or '/'
            vals['name'] = seq
        return super().create(vals)

    @api.depends('bid_line_ids.price_unit','bid_line_ids.product_qty')
    def _compute_total(self):
        for rec in self:
            rec.total = sum((l.price_unit or 0.0) * (l.product_qty or 0.0) for l in rec.bid_line_ids)

    def action_submit(self):
        for rec in self:
            rec.state = 'submitted'

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'

    def action_accept(self):
        """Create a purchase.order (PO) from the winning bid."""
        for rec in self:
            if rec.state == 'accepted':
                continue
            order_vals = {
                'partner_id': rec.vendor_id.id,
                'origin': rec.order_id.name or False,
                'order_line': [],
            }
            for l in rec.bid_line_ids:
                order_vals['order_line'].append((0, 0, {
                    'product_id': l.product_id.id,
                    'name': l.name or (l.product_id and l.product_id.display_name) or '',
                    'product_qty': l.product_qty,
                    'price_unit': l.price_unit,
                    'date_planned': rec.order_id.date_order or fields.Datetime.now(),
                }))
            po = self.env['purchase.order'].create(order_vals)
            rec.state = 'accepted'
        return True

class PurchaseBidLine(models.Model):
    _name = 'purchase.bid.line'
    _description = 'Purchase Bid Line'

    bid_id = fields.Many2one('purchase.bid', string='Bid', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    name = fields.Char(string='Description')
    product_qty = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Monetary(string='Unit Price', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='bid_id.currency_id', store=True)
