from odoo import http
from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.http import request


import logging
_logger = logging.getLogger(__name__)


##########################
# Some Custom Controller #
##########################
class CetmixCustomController(http.Controller):
    @http.route(
        ["/cetmix/custom_controller"], type="http", auth="public", website=True
    )
    def cetmix_controller(self, **post):
        _logger.info("Hi!")
        return


###############################
# Some Custom JSON Controller #
###############################
class CetmixCustomControllerJSON(http.Controller):
    @http.route(['/cetmix/custom_json_controller'], type='json', auth="user", website=True)
    def cetmix_controller_json(self, **kw):

        # Check if country and zip are in request
        val = kw.get("some_val", False)
        if not val:
            return {'data': False}
        else:
            return {'data': val}


#############################
# Some Inherited Controller #
#############################
class SomeInheritedController(CustomerPortal):
    @http.route(
        ["/my/orders/<int:order_id>",], type="http", auth="public", website=True
    )
    def portal_order_page(self, order_id=None, **post):
        response = super(SomeInheritedController, self).portal_order_page(order_id=order_id, **post)
        ip = request.httprequest.environ["REMOTE_ADDR"]
        so = request.env["sale.order"].browse(order_id).sudo()
        so.ooops_signature_view(
            partner_id=so.partner_id.id, user_id=request.env.user.id, date=False, ip=ip
        )
        return response

