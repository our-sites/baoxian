define('work/user/1.0.0:login', ['com/global/1.0.0:dollar'], function(require, exports, module) {

  var $ = require('com/global/1.0.0:dollar');
  require.async(['work/user/1.0.0:common']);
  //var Validator = require('validator');
  
  (function () {
      var $wrap = $('#Login');
      var $form = $wrap.find('form');
      if ($form.length) {
          var validator = new Validator({
              element: $form
          });
          validator.addItem({
              element: '#username',
              required: true
          }).addItem({
              element: '#password',
              required: true
          });
      }
  })();
  
   //@require work/user/1.0.0:login.css
  

});
