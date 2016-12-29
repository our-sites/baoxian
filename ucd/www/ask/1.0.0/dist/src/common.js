define('www/ask/1.0.0:common', ['www/common/1.0.0:common', 'com/global/1.0.0:dollar', 'com/global/1.0.0:validator'], function(require, exports, module) {

  require('www/common/1.0.0:common');
  var $ = require('com/global/1.0.0:dollar');
  
  var Validator = require('com/global/1.0.0:validator');
  var $form = $('form#ask');
  if ($form.length) {
      var $content = $('#content');
      var $currentLength = $('.current-length');
      var validator = new Validator({
          element: $form
      });
      validator.addItem({
          element: '#content',
          required: true,
          display: '提问内容'
      });
  
      $form.on('keyup', '#content', function () {
          var len = $content.val().length;
          $currentLength.html(len);
      });
  }
  
  
  
  
  // @require 'www/ask/1.0.0:common.css';
  

});
