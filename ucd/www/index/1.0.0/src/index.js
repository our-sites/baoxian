require('www/common:common.js');
require('slick:slick');
var $ = require('$');
$(".regular").slick({
    dots: true,
    infinite: true,
    arrows: false,
    slidesToShow: 1,
    slidesToScroll: 1,
    centerMode: true
});


// @require './index.css'