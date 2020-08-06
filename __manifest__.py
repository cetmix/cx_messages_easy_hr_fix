{
    "name": "Cetmix Custom Module",
    "version": "12.0.0.0.1",
    "summary": "Cetmix Module for Custom Features",
    "author": "Cetmix",
    "license": "LGPL-3",
    "category": "Discuss",
    "website": "https://cetmix.com",
    "live_test_url": "https://demo.cetmix.com",
    "description": """
    Some Custom Module that does weird magic
    """,
    # 'images': ['static/description/banner.png'],
    "depends": [
        "base", "mail"
    ],
    'external_dependencies': {
        # 'python' : ['some-python-package'],
    },
    "data": [
        # "security/groups.xml",
        # "security/ir.model.access.csv",
        # "security/record_rules.xml",
        # "views/root_menu.xml",
        # "views/view.xml",
        # "views/res_config_settings.xml",
    ],
    "qweb": [],
    "installable": True,
    "application": True,
}
