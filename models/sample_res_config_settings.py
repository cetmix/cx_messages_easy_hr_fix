from odoo import models, fields, api, _


###################
# Config Settings #
###################
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # -- Config setting. Many2one, Char, Integer can use simple definition
    sample_product_id = fields.Many2one(string="Sample Product Many2one",
                                        domain="[('type', '=', 'service')]",
                                        comodel_name='product.product',
                                        config_parameter='cetmix_module_template.sample_product_id',
                                        default=False)

    # -- Many2many can be handled like this
    sample_product_additional_ids = fields.Many2many(string="Additional Products",
                                                     comodel_name='product.product',
                                                     domain=[('type', '=', 'service')])

    # -- Add some action button in config
    def sample_wizard(self):
        self.ensure_one()

        return {
            'name': _("Some Action Wizard"),
            "views": [[False, "form"]],
            'res_model': 'sample.action.wiz',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    # -- Save Many2many values
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param('cetmix_module_template.sample_product_additional_ids',
                          ','.join(str(i) for i in self.sample_product_additional_ids.ids))

    # -- Read values
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()

        # Get Many2many from config
        sample_product_additional_ids = ICPSudo.get_param('cetmix_module_template.sample_product_additional_ids', default=False)
        if sample_product_additional_ids:
            res.update(sample_product_additional_ids=[int(r) for r in sample_product_additional_ids.split(',')])

        return res
