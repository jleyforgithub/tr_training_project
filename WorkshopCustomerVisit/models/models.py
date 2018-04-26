from odoo import models, fields, api, exceptions


class Project(models.Model):
    _name = 'tr.project'

    name = fields.Char(
        string='Project Name'
        , required=True
    )

    code = fields.Char(
        string='Project Code'
        , required=True
    )

    # Checking Duplicate Code
    @api.constrains('code')
    def _check_duplicate(self):
        if len(self.search([('code', '=', self.code)])) > 1:
            raise exceptions.ValidationError("This code has been already used!")

    budget = fields.Float(
        string='Budget'
        , digits=(10, 2)
        , required=True
    )
    """
    # Convert budget if budget be in the red to be in surplus
    @api.onchange('budget')
    def _Convert_Plus(self):
        if self.budget < 0:
            self.budget = abs(self.budget)
    """
    balance = fields.Float(
        string='Balance'
        , digits=(10, 2)
        , readonly=True
        , compute='_cal_balance'
    )

    take_customer_ids = fields.One2many(
        'tr.take.customer'
        , 'project_id'
        , string='Customer'
        , readonly=True
        , domain=[
            ('state', '!=', 'reject')
        ]
    )
    
    # Calculate Balance
    @api.depends('take_customer_ids')
    def _cal_balance(self):
        for rec in self:
            budget_use = 0.0
            for use in rec.take_customer_ids:
                if use.state == 'approve':
                    budget_use += use.budget_use

            rec.balance = rec.budget - budget_use


class TakeCustomer(models.Model):
    _name = 'tr.take.customer'

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

    @api.multi
    def action_request(self):
        if self.budget_use > self.balance:
            self.state = 'wait'
        else:
            self.state = 'approve'

    @api.multi
    def action_approve(self):
        self.state = 'approve'

    @api.multi
    def action_reject(self):
        self.state = 'reject'

    date_visit = fields.Datetime(
        default=fields.Date.today
        , string='Date Visit'
        , states={
            'wait': [
                ('readonly', True)
            ]
            , 'approve': [
                ('readonly', True)
            ]
            , 'reject': [
                ('readonly', True)
            ]
        }
    )

    name = fields.Many2one(
        'res.partner'
        , string='Customer Name'
        , required=True
        , domain=[
                    ('customer', '=', True)
        ]
        , states={
            'wait': [
                ('readonly', True)
            ]
            , 'approve': [
                ('readonly', True)
            ]
            , 'reject': [
                ('readonly', True)
            ]
        }
    )

    project_id = fields.Many2one(
        'tr.project'
        , string='Project Name'
        , required=True
        , states={
            'wait': [
                ('readonly', True)
            ]
            , 'approve': [
                ('readonly', True)
            ]
            , 'reject': [
                ('readonly', True)
            ]
        }
    )

    balance = fields.Float(
        string='Balance'
        , related='project_id.balance'
        , readonly=True
    )

    sales_ids = fields.Many2many(
        'res.users'
        , string='Sales'
        , states={
            'wait': [
                ('readonly', True)
            ]
            , 'approve': [
                ('readonly', True)
            ]
            , 'reject': [
                ('readonly', True)
            ]
        }
    )

    budget_use = fields.Float(
        string='Use Budget'
        , digits=(10, 2)
        , required=True
        , states={
            'wait': [
                ('readonly', True)
            ]
            , 'approve': [
                ('readonly', True)
            ]
            , 'reject': [
                ('readonly', True)
            ]
        }
    )

    # Calculate balance real time
    @api.onchange('budget_use')
    def _cal_balanceOnchange(self):
        if self.budget_use < 0:
            self.budget_use = abs(self.budget_use)

        self.balance -= self.budget_use

    sale_id = fields.Many2one(
        'sale.order'
        , string='Sale Order'
    )

