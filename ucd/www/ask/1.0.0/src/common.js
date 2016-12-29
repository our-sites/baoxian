require('www/common:common');
var $ = require('$');

var Validator = require('validator');
var $form = $('form#ask');
if ($form.length) {
    var $content = $('#content');
    var $currentLength = $('.current-length');
    var validator = new Validator({
        element: $form
    });
    validator.addItem({
        element: '#content',
        required: true,
        display: '提问内容'
    });

    $form.on('keyup', '#content', function () {
        var len = $content.val().length;
        $currentLength.html(len);
    });
}




// @require './common.css';
