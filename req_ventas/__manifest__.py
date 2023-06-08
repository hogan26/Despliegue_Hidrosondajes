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
    'depends': ['sale','req_crm','sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/last_update_price_partner.xml',
        'views/utility_lines_view.xml',        
        'views/sale_order_template_id_prueba.xml',
        # 'views/sheet_width_increase.xml', no funciona
        'views/total_tax_discount.xml',
        'views/liquidation.xml',
        'views/update_quotation_button.xml',
        'views/ot_button.xml',
        'views/sale_order_template_service.xml',
        'views/redirect_ot_coti.xml',
        'views/origin_sale_order_search_view.xml',
        'views/origin_sale_order_tree_view.xml',
        'views/redirect_coti_opportunity.xml',
        'views/pending_settlements_select.xml',
        'views/hidden_standart_confirm_button.xml',
        'wizard/alert_action_confirm_wizard.xml',
        'views/new_transfer_from_ot.xml',
    ],    
}
