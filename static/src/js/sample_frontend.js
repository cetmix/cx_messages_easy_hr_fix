odoo.define("cetmix_sample_module.join_meeting", function (require) {
    "use strict";

    /// This module gets BBB Meeting URL using controller and shows modal depending on result
    require("web.dom_ready");

    // Bus for Odoo 12
    require('bus.BusService');  // Not necessary sometimes?

    const ajax = require("web.ajax");
    var core = require('web.core');
    var _t = core._t;

    // Bus Odoo 11
    var bus = require('bus.bus').bus;


    var Chatter = require('mail.Chatter');

    Chatter.include({
        //action by click
        events: _.extend(Chatter.prototype.events, {
            // Cetmix events
            'click .notif_checkbox': '_onCheckboxClick',
            'click .note_checkbox': '_onCheckboxClick',
            'click .message_checkbox': '_onCheckboxClick',
        }),

        // Start
        start: function () {
            const res = this._super.apply(this, arguments);
            // Store length value to var
            for(var i = 0, i_length = this.messages.length; i < i_length; i++) {
                console.log("Avoid computing 'this.messages.length' each iteration");
            }
            // Set checkboxes values
            if (typeof this.fields.thread !== typeof undefined && this.fields.thread !== false && typeof this.record !== typeof undefined && this.record !== false && typeof this.record.res_id !== typeof undefined && this.record.res_id !== false) {
                this.getMessageFilters(this.fields.thread.model, this.record.res_id);
            }
            // Add bus listener for model update Odoo 11
            bus.on('notification', this, this._onMessageUpdated); // This function is used in Messages Pro module

            // Add bus listener for model update Odoo 12
            this.call('bus_service', 'onNotification', this, this._onNotification);

            return res;
        },
    });



    // Show correct fields when document is loaded
    $(document).ready(function () {
        const button_conference = $("#button-conference");
        if (button_conference.length) {

            // Get join URL on button click
            button_conference.click(function () {
                ajax.jsonRpc("/cetmix_sample_module/get_bbb_join_url", "call",
                    {seller_id: button_conference.attr("seller-id")}
                ).then(function (data) {
                    const error = data.error;
                    const url = data.url;
                    if (error) {
                        $('#warn-message-text').text(error)
                        $('#modalNotification').modal('show');
                    } else if (url) {
                        var win = window.open(url, '_blank');
                        if (win) {
                            win.focus();
                        } else {
                            alert(_t("Please allow pop-ups in browser for this page!"));
                        }
                    } else {
                        // In case some error happened during get_url() and we have error and url both false
                        $('#warn-message-text').text(_t("Seller is not available right now!"))
                        $('#modalNotification').modal('show');
                    }
                })
            })
        }
    });
});
