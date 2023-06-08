# -*- coding: utf-8 -*-
{
    'name': "req_crm",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        modificacion del formulario de requerimientos en crm para facilitar la generacion automatica de cotizaciones
    """,

    'author': "Hidrosondajes",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    
    'depends': ['base','crm','sale','sale_crm'],


    # always loaded
    'data': [
        'security/ir.model.access.csv',        
        'views/automatic_quotations_inputs_view.xml',
        'views/servicios_requeridos_label.xml',
        'views/crm_form_view_required_fields.xml',
        'views/create_date_kanban_view.xml',
        'views/verification_settlements_button_view.xml',
        'views/hidden_action_set_won_view.xml',
        'views/closure_pickings_list_view.xml',
    ],    
}
