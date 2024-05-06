from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import date
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"
    _order = "id desc"  # arrange the records (asc^ or desc)

    name = fields.Char(string='Name', required=True, translate=True, tracking=True)
    reference = fields.Char(string="Order Reference", required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))  # sequence field
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(string='Age', tracking=True, compute='_compute_age',
                         inverse='_inverse_compute_age', search='_search_age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    note = fields.Text(string='Description', tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], default='draft', string="status",
                             tracking=True)

    responsible_id = fields.Many2one("res.partner", string="Responsible")
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')
    image = fields.Binary(string="Patient Image")
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    hide_note = fields.Boolean(string="Hide Note Column")
    tag_ids = fields.Many2many('patient.tag', string="Tags")
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('married', 'Married'),
                                       ('single', 'Single'),
                                       ('divorced', 'Divorced'),
                                       ('widow', 'Widow')], tracking=True)
    partner_name = fields.Char(string="Partner Name")

    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]

    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age <= 0:
                raise ValidationError(_("The entered Age is not valid!"))

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("You cannot delete a patient with appointments!"))

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_test(self):
        return

    def name_get(self):
        result = []
        for rec in self:
            name = '[' + rec.reference + '] ' + rec.name
            result.append((rec.id, name))
        return result

    def action_open_appointments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'target': 'current',
        }

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Patient'
        if vals.get('reference', _("New")) == _("New"):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _("New")
        res = super(HospitalPatient, self).create(vals)
        return res

    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patients = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError(_("Name %s Already Exist" % self.name))

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError(_("Age Cannot Be Zero..!"))

    def _unlink_except_draft_or_cancel(self):
        for rec in self:
            if rec.state not in ('cancel'):
                raise UserError('you must delete state in cancel')
        return super(HospitalPatient, self).unlink()
