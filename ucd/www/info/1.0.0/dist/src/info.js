define('www/info/1.0.0:info', ['com/global/1.0.0:dollar', 'www/info/1.0.0:common'], function(require, exports, module) {

  var $ = require('com/global/1.0.0:dollar');
  
  require('www/info/1.0.0:common');
  
  // @require 'www/info/1.0.0:info.css';
  
  
  // 保险咨询左侧导航浮动
  var $slideNav = $('.slide-nav-container');
  if ($slideNav.length) {
      var top = $slideNav.offset().top;
      var $window = $(window);
      console.log(top);
      $window.on('load scroll resize', function () {
          var scrollTop = $window.scrollTop();
          if (scrollTop >= top) {
              $slideNav.addClass('fn-fixed');
          } else {
              $slideNav.removeClass('fn-fixed');
          }
      });
  }

});
