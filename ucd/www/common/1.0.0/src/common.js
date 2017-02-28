require('global');
var $ = require('$');
require('com/tabs:tabs');
require('region').initAll();
require('slick:slick');
var layer = require('layer:layer');

// 代理人模块选项卡
$('.warmheart-advisers').tabs({
    type: 'click',
    menuNode: '.rank-title-tab a',
    contNode: '.rank-type',
    className: 'active'
});

// 问吧模块选项卡
$('.ask-list-left').tabs({
    type: 'click',
    menuNode: '.ask-list-header-tab',
    contNode: '.ask-list-type',
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


// 量身订制模块的验证
var $form2 = $('#customized-form');
if ($form2.length) {
    var validator = new Validator({
        element: $form2
    });
    validator.addItem({
        element: '#name',
        required: true
    });
    validator.addItem({
        element: '#cellphone',
        required: true
    });
    validator.addItem({
        element: '#time-frame',
        required: true
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


// 活跃顾问悬浮效果
var $fixedArea = $('.lively-advisers');
if ($fixedArea.length) {
    var top = $fixedArea.offset().top;
    var $window = $(window);
    $window.on('load scroll resize', function () {
        var scrollTop = $window.scrollTop();
        if (scrollTop - top > 1) {
            $fixedArea.addClass('fn-fixed');
        } else {
            $fixedArea.removeClass('fn-fixed');
        }
    });
}

// 顶部消息
$('.bx-rtk-content ul').slick({
    dots: false,
    infinite: true,
    arrows: false,
    slidesToShow: 1,
    slidesToScroll: 1,
    vertical: true,
    autoplay: true,
    autoplaySpeed: 2000
});


// @require './common.css';
