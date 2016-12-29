define('work/user/1.0.0:login', ['com/global/1.0.0:dollar', 'work/user/1.0.0:common', 'com/global/1.0.0:validator'], function(require, exports, module) {

  var $ = require('com/global/1.0.0:dollar');
  require('work/user/1.0.0:common');
  var Validator = require('com/global/1.0.0:validator');
  
  (function () {
      var $wrap = $('#Login');
      var $form = $wrap.find('form');
      if ($form.length) {
          var validator = new Validator({
              element: $form
          });
          validator.addItem({
              element: '#username',
              required: true,
              display: '用户名'
          }).addItem({
              element: '#password',
              required: true,
              display: '密码'
          });
      }
  })();
  
  // @require work/user/1.0.0:login.css
  

});
