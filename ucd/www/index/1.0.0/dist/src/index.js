define('www/index/1.0.0:index', ['www/common/1.0.0:common', 'lib/slick/1.6.0:slick', 'com/global/1.0.0:dollar'], function(require, exports, module) {

  require('www/common/1.0.0:common');
  require('lib/slick/1.6.0:slick');
  var $ = require('com/global/1.0.0:dollar');
  $(".regular").slick({
      dots: true,
      infinite: true,
      arrows: false,
      slidesToShow: 1,
      slidesToScroll: 1,
      centerMode: true
  });
  
  
  // @require 'www/index/1.0.0:index.css'

});
