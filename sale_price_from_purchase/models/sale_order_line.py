from odoo import models, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id_set_price_from_purchase(self):
        for line in self:
            if not line.product_id:
                continue
            config = self.env['profit.config'].search([], order='id desc', limit=1)

            # Nếu không tìm thấy cấu hình HOẶC tính năng đang Tắt (False)
            if not config or not config.enable_auto_price:
                # Dừng hàm ngay lập tức -> Odoo sẽ dùng giá mặc định (Pricelist)
                continue 

            # --- PHẦN TÍNH TOÁN GIÁ ---
            purchase_price = 0.0
            
            # 1. Lấy giá mua từ Nhà cung cấp đầu tiên (Ưu tiên)
            supplier_info = line.product_id.seller_ids[:1]
            if supplier_info:
                purchase_price = supplier_info.price
            else:
                # 2. Nếu không có NCC, lấy giá vốn (Cost)
                purchase_price = line.product_id.standard_price

            # Nếu giá mua = 0 thì không cần tính tiếp
            if purchase_price <= 0:
                continue

            # 3. Lấy tỷ lệ lợi nhuận (Ưu tiên: Danh mục -> Mặc định)
            markup = config.default_markup
            
            # Kiểm tra xem sản phẩm có danh mục và danh mục đó có cài % riêng không
            if line.product_id.categ_id and line.product_id.categ_id.markup_percentage > 0:
                markup = line.product_id.categ_id.markup_percentage

            # 4. Tính giá bán và GÁN vào đơn hàng
            sale_price = purchase_price * (1 + markup / 100)
            line.price_unit = sale_price