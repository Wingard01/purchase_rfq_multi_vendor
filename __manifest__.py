{
    'name': 'RFQ Multi Vendor',
    'version': '1.0',
    'category': 'Purchases',
    'summary': 'Assign multiple vendors to an RFQ and handle bids + purchase requests',
    'depends': ['purchase', 'hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
        'views/purchase_bid_views.xml',
        'views/purchase_request_views.xml',
    ],
    'installable': True,
    'application': False,
}
