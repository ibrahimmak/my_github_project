from odoo import api, fields, models
from odoo.addons.sale.models.sale_order import SaleOrder as OdooSaleOrder


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_description = fields.Char(string='Sale Description')

    def _unlink_except_draft_or_cancel(self):
        return super(OdooSaleOrder, self).unlink()

    OdooSaleOrder.unlink = _unlink_except_draft_or_cancel
