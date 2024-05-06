import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import relativedelta


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    appointment_id = fields.Many2one("hospital.appointment", string="Appointment", required=True,
                                     domain=[('state', '=', 'draft')])
    date_cancel = fields.Date(string='Date Cancel', required=True)
    reason = fields.Text(string="Reason")

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    def action_cancel(self):
        cancel_days = self.env['ir.config_parameter'].get_param('new_hospital.cancel_days')
        allowed_date = self.appointment_id.date_appointment - relativedelta.relativedelta(days=int(cancel_days))
        if allowed_date < date.today():
            raise ValidationError(_("Sorry, Cancellation is not allowed for this appointment"))
        self.appointment_id.state = 'cancel'
