{
    'name': 'Lots Serial',
    'category': 'Inventory',
    'summary': "Manage Lot's Serial",
    'depends': ['stock','account'],
    'license': 'LGPL-3',
    'version': '1.0',
    'data': [
        # 'security/ir.model.access.csv',
        'views/lot_serial_views.xml',
        'views/res_partner_views.xml',
        # 'views/account_move_view.xml',
        # 'views/delivery_locations_views.xml',
    ],


    'installable': True,
    'auto_install': False,
    'application': False,
}