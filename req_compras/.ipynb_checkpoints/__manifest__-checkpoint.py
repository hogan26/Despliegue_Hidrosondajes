# -*- coding: utf-8 -*-
{
    'name': "req_compras",

    'summary': """
        purshase requerimient of hidrosondajes""",
    
    'author': "Hidrosondajes",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'custom modules',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase','req_inventario','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/fijar_proveedor_form_view.xml',
        'views/fijar_proveedor_tree_view.xml',
        'views/line_discount_view.xml',
    ],    
}
