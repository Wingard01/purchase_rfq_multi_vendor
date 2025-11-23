# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Request Reference', required=True, copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('purchase.request') or '/')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    department_id = fields.Many2one('hr.department', string='Department')
    date_request = fields.Date(default=fields.Date.context_today)
    line_ids = fields.One2many('purchase.request.line','request_id', string='Request Lines')
    state = fields.Selection([
        ('draft','Draft'),
        ('requested','Requested'),
        ('approved','Approved'),
        ('rfq','RFQ Created'),
        ('done','Done'),
    ], default='draft', tracking=True)

    def action_send_to_procurement(self):
        self.state = 'requested'
        self.message_post(body=_("Purchase request submitted: %s") % self.name)

    def action_create_rfq(self):
        for req in self:
            order_vals = {
                'origin': req.name,
                'order_line': [],
            }
            for line in req.line_ids:
                order_vals['order_line'].append((0,0,{
                    'product_id': line.product_id.id,
                    'name': line.description or (line.product_id and line.product_id.display_name) or '',
                    'product_qty': line.quantity,
                    'price_unit': 0.0,
                }))
            po = self.env['purchase.order'].create(order_vals)
            req.state = 'rfq'
        return True

class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    request_id = fields.Many2one('purchase.request', string='Request', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product')
    description = fields.Char('Description')
    quantity = fields.Float('Quantity', default=1.0)
