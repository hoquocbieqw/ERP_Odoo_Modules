from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    markup_percentage = fields.Float(string="Tỷ lệ lợi nhuận (%)", default=0.0)