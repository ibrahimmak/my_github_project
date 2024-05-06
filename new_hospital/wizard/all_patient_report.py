from odoo import api, fields, models, _


class PatientReportWizard(models.TransientModel):
    _name = "patient.report.wizard"
    _description = "Print Patient Wizard"

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender")
    age = fields.Integer(string="Age")

    def action_print_report_patient(self):
        data = {
            'form_data': self.read()[0],
        }
        return self.env.ref('new_hospital.report_all_patient').report_action(self, data=data)
