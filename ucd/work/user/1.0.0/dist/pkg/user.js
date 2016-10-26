;/*!work/user/1.0.0:login*/
define('work/user/1.0.0:login', [], function(require, exports, module) {

  // @require work/user/1.0.0:login.css

});

;/*!work/user/1.0.0:register*/
define('work/user/1.0.0:register', ['com/global/1.0.0:dollar'], function(require, exports, module) {

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
