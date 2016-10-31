define('www/common/1.0.0:common', ['com/global/1.0.0:global', 'com/global/1.0.0:dollar', 'com/tabs/1.0.0:tabs'], function(require, exports, module) {

  require('com/global/1.0.0:global');
  var $ = require('com/global/1.0.0:dollar');
  require('com/tabs/1.0.0:tabs');
  $('.warmheart-advisers').tabs({
      type: 'click',
      menuNode: '.rank-title-tab a',
      contNode: '.rank-type',
      className: 'active'
  });
  // @require 'www/common/1.0.0:common.css';
  

});
