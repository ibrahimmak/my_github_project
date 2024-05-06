from odoo import api, fields, models, _
# from odoo.tools.save_eval import save_eval


class OdooPlayGround(models.Model):
    _name = "odoo.playground"
    _description = "Odoo PlayGround"

    DEFAULT_ENV_VARIABLES = """ #Available Variables:
    # - self: Current Object
    # - self.env: Odoo Environment on which the action is triggered
    # - self.env.user: Return the current user (as an instance)
    # - self.env.is_system: Return whether the current user has group "settings", or superuser mode
    # - self.env.is_admin: Return whether the current user has group "Access Rights", or superuser mode
    # - self.env.is_superuser: Return whether the environment is in superuser mode
    # - self.env.compony: Return the current compony (as an instance)
    # - self.env.companies: Return a recordset of the enable companies by the user
    # - self.env.lag: Return the current language code \n\n\n\n """

    model_id = fields.Many2one('ir.model', string="Model")
    code = fields.Text(string="Code", default="DEFAULT_ENV_VARIABLES")
    result = fields.Text(string="Result")

    # def action_execute(self):
    #     try:
    #         if self.model_id:
    #             model = self.env[self.model_id.model]
    #         else:
    #             model = self
    #             self.result = save_eval(self.code.strip(), {'self': model})
    #     except Exception as e:
    #         self.result = str(e)
