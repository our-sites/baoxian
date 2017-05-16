require('www/common:common.js');
require('slick:slick');
var $ = require('$');
$(".regular").slick({
    dots: true,
    infinite: true,
    arrows: false,
    slidesToShow: 1,
    slidesToScroll: 1,
    centerMode: true,
    centerPadding: 0,
	autoplay: true
}).on('setPosition', function(){
    var wrapWith = $('.slider-item').width();
    var left = (wrapWith - 1890)/2 + 'px';
    $('.slider-helper').css({
        left: left
    })

});


// @require './index.css'
