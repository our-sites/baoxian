var $ = require('$');
require.async('./common.js');
//var Validator = require('validator');

(function () {
    var $wrap = $('#Login');
    var $form = $wrap.find('form');
    if ($form.length) {
        var validator = new Validator({
            element: $form
        });
        validator.addItem({
            element: '#username',
            required: true
        }).addItem({
            element: '#password',
            required: true
        });
    }
})();

 //@require ./login.css
