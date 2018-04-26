from odoo import models, fields, api, exceptions


class TakeCustomerWiz(models.TransientModel):
    _name = 'tr.take.customer.wiz'

    # Creating Fuction for get take customer
    def _get_default_take_customer_ids(self):
        take_customer_env = self.env['tr.take.customer']
        take_customer_search = take_customer_env.search(
            [
                '|'
                , ('state', '=', 'reject')
                , '&'
                , ('state', '=', 'draft')
                , ('budget_use', '<', 1000)
            ]
        )

        vals = []

        for take_customer_id in take_customer_search:
            vals.append(
                (
                    0
                    , 0
                    , {
                        'date_visit': take_customer_id.date_visit
                        , 'name': take_customer_id.name
                        , 'project_id': take_customer_id.project_id
                        , 'balance': take_customer_id.balance
                        , 'budget_use': take_customer_id.budget_use
                        , 'state': take_customer_id.state
                    }
                )
            )

        return vals

    take_customer_ids = fields.One2many(
        'tr.take.customer.list.wiz'
        , 'take_customer_id'
        , string="Customer"
        , readonly=True
        , copy=True
        , default=_get_default_take_customer_ids
    )

    # Deleting take customer visit
    def action_confirm_delete(self):
        take_customer_env = self.env['tr.take.customer']
        take_customer_delete = take_customer_env.search(
            [
                '|'
                , ('state', '=', 'reject')
                , '&'
                , ('state', '=', 'draft')
                , ('budget_use', '<', 1000)
            ]
        )

        for take_customer in take_customer_delete:
            take_customer.unlink()


class TakeCustomerList(models.TransientModel):
    _name = "tr.take.customer.list.wiz"
    _description = "Take Customer List"

    take_customer_id = fields.Many2one(
        'tr.take.customer'
        , string="Customer"
    )

    date_visit = fields.Datetime(
        default=fields.Date.today
        , string='Date Visit'
    )

    name = fields.Many2one(
        'res.partner'
        , string='Customer Name'
        , readonly=True
    )

    project_id = fields.Many2one(
        'tr.project'
        , string='Project Name'
        , readonly=True
    )

    balance = fields.Float(
        string='Balance'
        , related='project_id.balance'
        , readonly=True
    )

    budget_use = fields.Float(
        string='Use Budget'
        , digits=(10, 2)
        , readonly=True
    )

    state = fields.Selection(
        [
            ('draft', "Draft"),
            ('wait', "Wait"),
            ('approve', "Approve"),
            ('reject', "Reject"),
        ]
        , default='draft'
        , string='state'
    )