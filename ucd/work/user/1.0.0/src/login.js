var $ = require('$');
require('./common.js');
var Validator = require('validator');

(function () {
    var $wrap = $('#Login');
    var $form = $wrap.find('form');
    if ($form.length) {
        var validator = new Validator({
            element: $form
        });
        validator.addItem({
            element: '#username',
            required: true,
            display: '用户名'
        }).addItem({
            element: '#password',
            required: true,
            display: '密码'
        });
    }
})();

// @require ./login.css
