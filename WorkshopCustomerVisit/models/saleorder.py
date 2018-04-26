from odoo import models, fields, api, exceptions

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tr_project_id = fields.Many2one(
        'tr.project'
        , string='Project'
    )

    tr_take_customer_ids = fields.One2many(
        'tr.take.customer'
        , 'sale_id'
        , string='Take Customer'
    )

    @api.onchange('tr_project_id')
    def _transfer_take_customer(self):
        project_id = self.tr_project_id
        take_list = []
        for line in project_id.take_customer_ids:
            take_list.append(line.id)

        self.tr_take_customer_ids = take_list
    """
    @api.muti
    def write(self, vals):
        if 'tr_project_id' in vals and vals.get('tr_project_id'):
            take_list = []
            project_obj = self.env['tr.project'].browse(vals.get('tr_project_id'))

            for line in project_obj.take_customer_ids:
                take_list.appen(line.id)
    """
