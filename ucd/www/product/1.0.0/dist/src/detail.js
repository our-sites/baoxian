define('www/product/1.0.0:detail', ['www/product/1.0.0:common', 'com/global/1.0.0:dollar'], function(require, exports, module) {

  require('www/product/1.0.0:common');
  var $ = require('com/global/1.0.0:dollar');
  $('.product-information').tabs({
      type: 'click',
      menuNode: '.product-information-tabs li',
      contNode: '.product-info-detail,.product-info-example,.product-info-process',
      className: 'active'
  });
  // @require 'www/product/1.0.0:detail.css';
  

});
