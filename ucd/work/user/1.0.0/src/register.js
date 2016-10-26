require('./common.js')
var $ = require('$');
var regiester = $('#Register');
var Register = {
    init: function () {
        this.roleTab();
    },
    roleTab: function () {
        regiester.find('.role input[type="radio"]').on('change', function () {
            if($(this).prop('checked')){
                var label = $(this).parent(),
                    select = regiester.find('select');
                label.addClass('active').siblings('label').removeClass('active');
                if(label.hasClass('agency')){
                    select.show();
                }else{
                    select.hide();
                }
            }
        })
    }
};

Register.init();

// @require ./register.css
