# -*- coding: utf-8 -*-
{
    'name': "Workshop Project",

    'summary': """Manage trainings""",

    'description': """
        Workshop Project module for view period:
            - Project Name
            - Take Customer
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale',
        'purchase',
    ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/take_customer_delete_unused.xml',
        'wizard/take_customer_change_date.xml',
        'wizard/take_customer_mark_approve.xml',
        'views/customervisit.xml',
        'views/saleorder.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}