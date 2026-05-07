# Sale Price From Purchase — Odoo 18 Custom Module

> Tự động tính giá bán dựa trên giá mua và tỷ lệ lợi nhuận theo danh mục sản phẩm  
> Phát triển trong khuôn khổ Đồ án môn học **Hoạch định Nguồn lực Doanh nghiệp** — Đại học Văn Lang, 2025

---

## Bối cảnh & Vấn đề (Pain Points)

Doanh nghiệp nghiên cứu: **Biti's** (mạng lưới bán lẻ giày dép đa kênh tại Việt Nam)

| Vấn đề | Hậu quả |
|--------|---------|
| Sales nhập giá bán thủ công trên từng đơn hàng | Sai sót, bán lỗ, mất doanh thu |
| Không kiểm soát biên lợi nhuận (margin) theo dòng sản phẩm | Hunter vs dép xốp áp dụng cùng margin → không đạt KPI |
| Phụ thuộc Excel để tính giá | Không đồng bộ giữa các kênh Retail / Wholesale / E-commerce |

---

## Giải pháp

Module `sale_price_from_purchase` mở rộng phân hệ **Sales** của Odoo 18, tự động tính và gán giá bán đề xuất ngay khi nhân viên chọn sản phẩm trong báo giá.

### Công thức tính giá

```
Giá bán = Giá mua × (1 + Tỷ lệ lợi nhuận %)
```

- **Giá mua**: ưu tiên lấy từ Vendor Pricelist, fallback về `standard_price`
- **Tỷ lệ lợi nhuận**: ưu tiên theo danh mục sản phẩm, fallback về cấu hình mặc định hệ thống

---

## Kiến trúc Module

```
sale_price_from_purchase/
├── __manifest__.py
├── models/
│   ├── profit_config.py        # Singleton config — Smart Defaults pattern
│   ├── product_category.py     # Thêm field markup_percentage
│   └── sale_order_line.py      # Onchange tính giá — Observer pattern
├── views/
│   ├── profit_config_view.xml
│   ├── product_category_view.xml
│   └── menu.xml
└── security/
    └── ir.model.access.csv
```

### Design Patterns sử dụng

| Pattern | Áp dụng tại | Mục đích |
|---------|------------|---------|
| Singleton | `profit_config.py` | Tự tạo config nếu chưa có, cài xong dùng ngay |
| Observer | `sale_order_line.py` | Chọn sản phẩm → tự tính giá real-time |
| Chain of Responsibility | Logic margin | Danh mục → Mặc định, linh hoạt với 1000+ SKU |

---

## Tính năng chính

- Tự động tính giá bán khi chọn sản phẩm trong `sale.order.line`
- Cấu hình tỷ lệ lợi nhuận mặc định toàn hệ thống
- Cấu hình tỷ lệ lợi nhuận riêng theo từng danh mục sản phẩm
- Phân quyền: Admin/Sales Manager cấu hình — Sales User chỉ xem & áp dụng
- Tích hợp sâu vào quy trình tạo báo giá chuẩn của Odoo

---

## Yêu cầu hệ thống

- Odoo 17–18 Community
- Python 3.10+
- Các module phụ thuộc: `sale`, `product`

---

## Cài đặt

```bash
# 1. Clone repo về máy
git clone https://github.com/hoquocbieqw/ERP_Odoo_Modules.git

# 2. Copy thư mục module vào addons path của Odoo
cp -r sale_price_from_purchase/ /path/to/odoo/addons/

# 3. Khởi động lại Odoo server
./odoo-bin -u sale_price_from_purchase -d <your_database>
```

Hoặc cài trực tiếp qua **Apps** trong giao diện Odoo:
1. Bật Developer Mode
2. Vào Apps → Update Apps List
3. Tìm "Sale Price From Purchase" → Install

---

## Hướng dẫn sử dụng

**Bước 1 — Bật tính năng & cấu hình margin mặc định**  
Sales → Mức Lợi Nhuận → Cấu hình lợi nhuận → Bật "Tính giá tự động" → Nhập tỷ lệ % mặc định

**Bước 2 — Cấu hình margin theo danh mục**  
Sales → Mức Lợi Nhuận → Danh mục sản phẩm → Chọn danh mục → Nhập tỷ lệ lợi nhuận (%)

**Bước 3 — Tạo báo giá**  
Sales → Quotations → Create → Thêm sản phẩm → Giá bán tự động được tính và điền vào Unit Price

---

## BPMN Workflows

Dự án bao gồm 3 quy trình nghiệp vụ được mô hình hóa bằng BPMN 2.0:

| # | Quy trình | Công cụ |
|---|-----------|---------|
| 1 | Quy trình Sản xuất Giày Biti's (Sales → Inventory → Accounting) | bpmn.io |
| 2 | Quy trình Bán hàng đa kênh | bpmn.io |
| 3 | Quy trình Thay đổi Bảng giá | bpmn.io |

File BPMN: xem tại [Google Drive — ERP_Odoo Folder](https://drive.google.com/drive/folders/1B52A_VW2dWEK0ZvLKmBhoEBzM21WTHeu)

---

## Demo

| Nội dung | Link |
|---------|------|
| Video hướng dẫn sử dụng module | [Xem trên YouTube](https://www.youtube.com/watch?v=h47Hz8iy3QU&t=38s) |
| Video giải thích code | [Xem trên YouTube](https://www.youtube.com/watch?v=TFS9HS9ZMRA&t=2s) |
| Video quy trình sản xuất (BPMN demo) | [Xem trên YouTube](https://www.youtube.com/watch?v=s3KqPlECtt8&t=43s) |
| Video quy trình bán hàng (BPMN demo) | [Xem trên YouTube](https://www.youtube.com/watch?v=o8FrZBXzG_E) |

---

## Nhóm thực hiện

| Thành viên | Vai trò | Đóng góp |
|-----------|---------|---------|
| **Hồ Quốc Biên** | BA & Developer | Kịch bản quy trình, BPMN sản xuất & bán hàng, quay video demo |
| Lê Đặng Phước Thọ | Lead Developer | Thiết kế & xây dựng module, báo cáo chương 2-3-6-7 |
| Phạm Thanh Phi | BA & Editor | Phân tích bài toán, kịch bản vận hành 1, edit video |
| Võ Quốc Thành | BA | BPMN thay đổi bảng giá, báo cáo chương 5 |

**GVHD:** ThS. Huỳnh Thanh Tuấn · ThS. Nguyễn Tuyên Linh  
**Trường:** Đại học Văn Lang — Khoa Công nghệ Thông tin, 2025

---

## Hướng mở rộng

- Cảnh báo khi margin thấp hơn ngưỡng tối thiểu
- Workflow phê duyệt giá đặc biệt
- Dashboard theo dõi lợi nhuận theo sản phẩm / danh mục / thời gian
- Đề xuất giá bán theo phân khúc khách hàng

---

*Đồ án môn học — Hoạch định Nguồn lực Doanh nghiệp (ERP) · Đại học Văn Lang · 2025*
