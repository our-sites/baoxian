require('global');
var $ = require('$');
require('com/tabs:tabs');
require('region').initAll();

// 代理人模块选项卡
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

// 条件筛选
$('.letter-filter').each(function () {
    var $filterWrap = $(this);
    var $keys = $filterWrap.find('[data-key]');
    var $belongs = $filterWrap.find('[data-belong]');

    function showAll() {
        $keys.removeClass('active').filter('[data-key="all"]').addClass('active');
        $belongs.show();
    }
    function showLetter(letter) {
        $keys.removeClass('active').filter('[data-key="' + letter + '"]').addClass('active');
        $belongs.hide().filter('[data-belong="' + letter + '"]').show();
    }
    $filterWrap.on('click', '[data-key]', function (e) {
        e.preventDefault();
        var letter = $(this).data('key');
        if (letter === 'all') {
            console.log($belongs.length);
            showAll();
        } else {
            showLetter(letter);
        }
    });
});



// @require './common.css';
