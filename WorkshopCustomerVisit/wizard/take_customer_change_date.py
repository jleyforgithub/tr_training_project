from odoo import models, fields, api, exceptions
from datetime import datetime


class TakeCustomerChangeDateVisit(models.TransientModel):
    _name = 'tr.take.customer.change.date.wiz'

    # Default Date Visit
    def _get_default_date_visit(self):
        active_model = self._context['active_model']
        active_id = self._context['active_id']
        take_customer_env = self.env[active_model]
        take_customers = take_customer_env.browse(active_id)

        return take_customers['date_visit']

    take_customer_date_visit = fields.Datetime(
        string='Date Visit'
        , default=_get_default_date_visit
    )

    # Checking out of date
    def _check_out_of_date(self):
        date_visit = datetime.strptime(self.take_customer_date_visit, '%Y-%m-%d %H:%M:%S')
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_now = datetime.strptime(date_now, '%Y-%m-%d %H:%M:%S')

        if date_visit < date_now:
            raise exceptions.ValidationError("Date Visit out of date")

    # Changing date visit on state approve
    def action_change_date_visit(self):
        active_model = self._context['active_model']
        active_id = self._context['active_id']
        take_customer_env = self.env[active_model]
        take_customers = take_customer_env.browse(active_id)

        self._check_out_of_date()

        for take_customer in take_customers:
            take_customer.write(
                {
                    'date_visit': self.take_customer_date_visit
                }
            )
