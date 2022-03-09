# -*- coding: utf-8 -*-
{
    'name': "req_ventas",

    'summary': """
        sale hidrosondajes requeriments""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Hidrosondajes",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','req_crm'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/utility_lines_view.xml',
        'views/last_update_price_partner.xml',
        #'views/sale_order_template_id_prueba.xml',
        'views/sheet_width_increase.xml',
        #'views/total_tax_discount.xml',
        'views/liquidation.xml',
    ],    
}
