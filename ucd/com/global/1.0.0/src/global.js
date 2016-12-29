var $ = require('jquery');
var Validator = require('./validator.js');
var $form = $('.bx-header form.ui-form');
if ($form.length) {
    $form.on('click', '.bx-header-search-box a', function (e) {
        e.preventDefault();
        $form.trigger('submit');
    });
    var validator = new Validator({
        element: $form
    });
    validator.addItem({
        element: '#search-kw',
        required: true,
        display: '搜索内容'
    });
}

// @require ./global.css
