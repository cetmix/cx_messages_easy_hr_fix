from odoo import _, models, fields, api
from odoo.exceptions import UserError
from odoo.api import SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)
"""
Check DEPENDENCIES_MET param in case the module depends on some external Python lib 
"""
# DEPENDENCIES_MET = True
# try:
#     from some_python_lib import SomePythonLibFunction
# except ImportError:
#     DEPENDENCIES_MET = False
#     pass

# -- Get the duration value between the 2 given dates.
def get_duration(start, stop):
    """ Borrowed from Odoo calendar module. """
    if start and stop:
        diff = fields.Datetime.from_string(stop) - fields.Datetime.from_string(start)
        if diff:
            duration = float(diff.days) * 24 + (float(diff.seconds) / 3600)
            return round(duration, 2)
        return 0.0


##############
# Some Model #
##############
class CetmixCustomModel(models.Model):
    _name = "cetmix.custom.model"
    _description = "Cetmix Custom Model"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _mail_post_access = "read"

    # Basic fields example
    name = fields.Char(string="Name",
                       required=True,
                       copy=False,
                       readonly=True,
                       states={'1': [('readonly', False)]},
                       index=True,
                       default=lambda self: _('New'))
    partner_id = fields.Many2one(string="Partner",
                                 comodel_name='res.partner',
                                 required=True)

    state = fields.Selection(string="Selection",
                             selection=[
                                 ('1', 'New'),
                                 ('4', 'Running'),
                                 ('7', 'Finished'),
                             ],
                             default='1',
                             readonly=True,
                             copy=False,
                             track_visibility="onchange"
                             )
    custom_date = fields.Datetime(string="Custom Date")

    # Using domain in fields
    product_uom = fields.Many2one(string='Unit of Measure',
                                  comodel_name='uom.uom',
                                  domain="[('category_id', '=', product_uom_category_id)]")

    # -- Create
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            seq_date = None
            if 'custom_date' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['custom_date']))
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'cetmix.custom.model', sequence_date=seq_date) or _('New')
            else:
                vals['name'] = self.env['ir.sequence']. \
                                   next_by_code('cetmix.custom.model', sequence_date=seq_date) or _('New')

        return super(CetmixCustomModel, self).create(vals)

    # -- Custom function <-- Always add brief
    @api.model
    def custom_function(self, partner_id):
        """
        Always add descriptions to functions if it implements some
        complicated evaluations!
        E.g. "this function does some weird magic to Partner"
        :param Integer partner_id:  id of the Partner
        :return:                    True if success else False

        """
        # Get partner by id <-- Use brief inline comments for each important step
        partner = self.env['res.partner'].browse(partner_id)

        # Cet setting value from config
        sample_product_id = int(self.env['ir.config_parameter'].sudo().get_param('cetmix_module_template.sample_product_id', False))
        if sample_product_id:
            sample_product = self.env['product.product'].browse(sample_product_id)
            return sample_product
        return partner

    # -- Open View From code
    def open_view(self):
        return {
            'name': _("View Title"),
            "views": [[False, "form"]],
            'res_model': "some.target.model",
            'res_id': False,    # put ID here to open exact record
            'type': "ir.actions.act_window",
            'target': "new",    # current for same view
            'context': {},
            'domain': []
        }

    # -- Run from XML
    @api.model
    def run_from_xml(self):
        print("WOW! This code is triggered from XML!")
        """
        We can override 'noupdate=1' with this code.
        Just add function call BEFORE xml definition of the read-only data you want to modify
        """
        ref = self.env["ir.model.data"].sudo().search(
            [
                ("name", "=", "some_noupdatable_ref"),
                ("noupdate", "=", True)
            ], limit=1
        )
        if ref:
            ref.sudo().write({"noupdate": False})
