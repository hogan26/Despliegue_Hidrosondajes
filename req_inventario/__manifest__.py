# -*- coding: utf-8 -*-
{
    'name': "req_inventario",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        campos para visualizar la ultima actualizacion de precio de un producto del catalogo
    """,

    'author': "Hidrosondajes",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',        
        'views/last_update_pricelist_date_view.xml',
        'views/composite_product_form_view.xml',
        'views/servicio_reservado.xml',
        'views/web_odoo_warehouse_config_fields_view.xml',
        'views/picking_list_view_columns.xml',
        'views/warehouse_picking_stock_view.xml',
        'views/detailed_operations_warehouse_stock_view.xml',
        'views/search_picking_ot_origen.xml',
        'views/inches_field_view.xml',
        'views/supplementary_closure_information.xml',
        'views/button_autocomplete_picking_ot.xml',
        'views/product_name_location_list.xml',
    ],    
}
