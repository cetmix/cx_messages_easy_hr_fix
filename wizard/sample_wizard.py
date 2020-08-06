from odoo import models, fields, api


########################
# Cetmix Sample Wizard #
########################
class CetmixSampleWizard(models.TransientModel):
    _name = 'cetmix.sample.wiz'
    _description = "Cetmix Sample Wizard"

    partner_id = fields.Many2one(string="Partner",
                                 comodel_name='res.partner')
