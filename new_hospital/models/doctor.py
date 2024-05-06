from odoo import api, fields, models, _


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Doctor"
    _rec_name = 'doctor_name'
    _order = "id desc"  # arrange the records (asc^/desc)

    doctor_name = fields.Char(string='Doctor Name', required=True, tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender")
    note = fields.Text(string='Description')
    image = fields.Binary(string="Patient Image")
    reference = fields.Char(string="Order Reference", required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))  # sequence field
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')
    active = fields.Boolean(string="Active", default="True")
    # operation_name = fields.Char(string="Operation Name")

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Doctor'
        if vals.get('reference', _("New")) == _("New"):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.doctor') or _("New")
        res = super(HospitalDoctor, self).create(vals)
        return res

    # @api.model
    # def name_create(self, name):
    #     return self.create({'name': name}).name_get()[0]

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('doctor_name'):
            default['doctor_name'] = _("%s(copy)", self.doctor_name)
        default['note'] = "Copied Record"
        return super(HospitalDoctor, self).copy(default)

    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('doctor_id', '=', rec.id)])
            rec.appointment_count = appointment_count
