{
    'name': "Photovoltaic Management Extended",
    'version': '13.0.1.0.1',
    'depends': ['photovoltaic_mgmt'],
    'author': "Librecoop",
    'category': 'Sales',
    'description': """
    This module extendes the functionality of the Photovoltaic Management module
    """,
    "installable": True,
    "auto_install": True,
    "data": [
        "views/contract_participation.xml",
        "views/photovoltaic_power_station.xml",
        "wizard/account_allocation_state_update_wizard_view.xml",
        "views/account_allocation.xml"
    ],
}
