{
    'name': 'Sale Price From Purchase',
    'version': '17.0.2.0.0',
    'summary': 'Tự động tính giá bán dựa trên giá mua với cấu hình linh hoạt',
    'description': 'Cho phép bật/tắt tính năng, chỉnh tỷ lệ lợi nhuận mặc định và theo danh mục sản phẩm.',
    'author': 'ERP-Team2 Developer',
    'depends': ['sale', 'product'],
    'data': [
        'security/ir.model.access.csv',
        
    
        'data/profit_config_data.xml', 
       
        
        'view/profit_config_view.xml',
        'view/product_category_view.xml',
        'view/menu.xml',
    ],
    'installable': True,
    'application': False,
}