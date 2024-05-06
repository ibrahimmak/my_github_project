from odoo import api, fields, models, _


class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"

    date_appointment = fields.Date(string='Date', required=True)
    patient_id = fields.Many2one("hospital.patient", string="Patient", required=True)
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor", required=True)

    def action_create_appointment(self):
        print("Button Is Clicked")
        vals = {
            'patient_id': self.patient_id.id,
            'date_appointment': self.date_appointment,
            'doctor_id': self.doctor_id.id
        }
        appointment_rec = self.env['hospital.appointment'].create(vals)
        print("appointment", appointment_rec.id)
        return {
            'name': 'Appointment',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'res_id': self.id
        }

    @api.model
    def default_get(self, fields):
        res = super(CreateAppointmentWizard, self).default_get(fields)
        if self._context.get('active_id'):
            res['patient_id'] = self._context.get('active_id')
        return res

    # def action_view_appointment(self):
    #     # method1
    #     action = self.env.ref('hospital.action_hospital_appointment').read()[0]
    #     action['domain'] = [('patient_id', '=', self.patient_id.id)]
    #     return action

    # method2
    # action = self.env["ir.actions.actions"]._for_xml_id("hospital.action_hospital_appointment")
    # action['domain'] = [('patient_id', '=', self.patient_id.id)]
    # return action

    # method3
    # return {
    #     'type': 'ir.actions.act_window',
    #     'name': 'Appointments',
    #     'res_model': 'hospital.appointment',
    #     'view_type': 'form',
    #     'view_mode': 'tree,form',
    #     'domain': [('patient_id', '=', self.patient_id.id)],
    #     'target': 'current',
    # }
