odoo.define("cetmix_sample_module.signature", function (require) {
        "use strict";
        var SignatureForm = require('portal.signature_form').SignatureForm;

        // Tweak Portal Signature
        SignatureForm.include(
            {
                _onClickSignSubmit: function (ev) {
                    // Check if selected options are stored
                    const selected_options = $("#accept").data("selected-options");
                    if (typeof selected_options === typeof undefined){
                        return  this._super.apply(this, arguments);
                    }

                    var self = this;
                    ev.preventDefault();

                    if (!this.nameAndSignature.validateSignature()) {
                        return;
                    }

                    var name = this.nameAndSignature.getName();
                    var signature = this.nameAndSignature.getSignatureImage()[1];

                    // Cetmix
                    // Pass selected options to the controller

                    return this._rpc({
                        route: this.callUrl,
                        params: _.extend(this.rpcParams, {
                            'name': name,
                            'signature': signature,
                            'selected_options': selected_options,
                        }),
                    }).then(function (data) {
                        if (data.error) {
                            self.$('.o_portal_sign_error_msg').remove();
                            self.$controls.prepend(qweb.render('portal.portal_signature_error', {widget: data}));
                        } else if (data.success) {
                            var $success = qweb.render('portal.portal_signature_success', {widget: data});
                            self.$el.empty().append($success);
                        }
                        if (data.force_refresh) {
                            if (data.redirect_url) {
                                window.location = data.redirect_url;
                            } else {
                                window.location.reload();
                            }
                            // no resolve if we reload the page
                            return new Promise(function () { });
                        }
                    });
                },
            }
        )
    }
);
