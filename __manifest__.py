# -*- coding: utf-8 -*-
{
    'name': "Meeting Room",

    'summary': """
        This feature will save you time to find a meeting room for daily meetings, and optimize your meeting/appointment planning.""",

    'description': """
        This feature will save you time to find a meeting room for daily meetings, and optimize your meeting/appointment planning.
    """,

    'author': "Ahmed Gaber",
    'website': "https://www.freelancer.com/u/AhmedGaberEgy",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'calendar', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/meeting_room.xml',
        'views/calendar_event.xml',
    ],
}
