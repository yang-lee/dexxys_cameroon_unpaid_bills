{
    'name' : 'Dexxys Cameroon Vendor Bills Tracker',
    'version' : '1.0',
    'author' : 'Dexxys Cameroon',
    'summary' : 'Cashier Managers Customers Bills',
    'description' : 'ALert Cashiers and Managers for unpaid vendor bills',
    'category' : 'Sales and Account Management',
    'depends' : ['base', 'mail', 'account'],
    'data':[
        'views/ir_cron.xml',
        'data/email_template.xml'
    ],
    'installable': True
}
