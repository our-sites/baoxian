require('global');
var $ = require('$');
require('com/tabs:tabs');
require('region').initAll();

$('.warmheart-advisers').tabs({
    type: 'click',
    menuNode: '.rank-title-tab a',
    contNode: '.rank-type',
    className: 'active'
});

// 私人订制模块的验证
var Validator = require('validator');
var $form = $('#custom-form');
if ($form.length) {
    var validator = new Validator({
        element: $form
    });
    validator.addItem({
        element: '#contact',
        required: true,
        display: '联系电话'
    });
}
// @require './common.css';
