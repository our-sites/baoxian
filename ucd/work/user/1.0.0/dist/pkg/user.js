;/*!work/user/1.0.0:common*/
define('work/user/1.0.0:common', ['com/global/1.0.0:dollar', 'work/common/1.0.0:common'], function(require, exports, module) {

  var $ = require('com/global/1.0.0:dollar');
  require('work/common/1.0.0:common');
  
  // @require work/user/1.0.0:common.css
  

});

;/*!work/user/1.0.0:login*/
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

;/*!work/user/1.0.0:register*/
define('work/user/1.0.0:register', ['work/user/1.0.0:common', 'com/global/1.0.0:dollar'], function(require, exports, module) {

  require('work/user/1.0.0:common')
  var $ = require('com/global/1.0.0:dollar');
  var regiester = $('#Register');
  var Register = {
      init: function () {
          this.roleTab();
      },
      roleTab: function () {
          regiester.find('.role input[type="radio"]').on('change', function () {
              if($(this).prop('checked')){
                  var label = $(this).parent(),
                      select = regiester.find('select');
                  label.addClass('active').siblings('label').removeClass('active');
                  if(label.hasClass('agency')){
                      select.show();
                  }else{
                      select.hide();
                  }
              }
          })
      }
  };
  
  Register.init();
  
  // @require work/user/1.0.0:register.css
  

});
