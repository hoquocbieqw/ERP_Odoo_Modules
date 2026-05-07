from odoo import models, fields, api

class ProfitConfig(models.Model):
    _name = 'profit.config'
    _description = 'Cấu hình lợi nhuận'
    _rec_name = 'display_name'

    enable_auto_price = fields.Boolean(
        string="Bật tính năng tự động tính giá", 
        default=True,
        help="Khi bật, giá bán sẽ tự động được tính dựa trên giá mua và tỷ lệ lợi nhuận"
    )
    default_markup = fields.Float(
        string="Tỷ lệ lợi nhuận mặc định (%)", 
        default=20.0,
        help="Tỷ lệ lợi nhuận sẽ được áp dụng nếu danh mục sản phẩm không có cấu hình riêng"
    )
    display_name = fields.Char(
        string="Tên hiển thị",
        compute="_compute_display_name",
        store=True
    )

    @api.depends('default_markup', 'enable_auto_price')
    def _compute_display_name(self):
        for record in self:
            status = "Đang bật" if record.enable_auto_price else "Đã tắt"
            record.display_name = f"Cấu hình lợi nhuận ({status} - {record.default_markup}%)"

    @api.model
    def get_config(self):
        """Lấy cấu hình, tự động tạo nếu chưa có"""
        config = self.search([], limit=1)
        if not config:
            config = self.create({
                'enable_auto_price': True,
                'default_markup': 20.0
            })
        return config

    def toggle_auto_price(self):
        """Toggle trạng thái bật/tắt"""
        for record in self:
            record.enable_auto_price = not record.enable_auto_price
        return True