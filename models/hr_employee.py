from odoo import models, fields


###################
# Public Employee #
###################
class EmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    hide_notifications = fields.Boolean(string="Hide notifications",
                                        help="Hide notifications")
    hide_notes = fields.Boolean(string="Hide notes",
                                help="Hide notes")
    hide_messages = fields.Boolean(string="Hide messages",
                                   help="Hide messages")
