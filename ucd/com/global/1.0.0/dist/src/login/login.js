define('com/global/1.0.0:login/login', ['com/validator/0.10.3:validator', 'lib/art-dialog/6.0.5:art-dialog', 'com/global/1.0.0:dollar'], function(require, exports, module) {

  var Validator = require('com/validator/0.10.3:validator');
  var dialog = require('lib/art-dialog/6.0.5:art-dialog');
  var $ = require('com/global/1.0.0:dollar');
  var unique = 1;
  module.exports = Validator.extend({
      // 表单出错的处理
      formErrorHandle: function (res) {
          var that = this;
          if (res.errorCode === 800) {
              // 弹出登录窗口
              var ins = dialog({
                  content: res.data.html
              });
              ins.showModal();
              var $node = $(ins.node);
              var $form = $node.find('form');
              //$form.data('dialog', ins);
              if ($form.length) {
                  var validator = new Validator({
                      element: $form
                  });
  
                  $form.find('.popup-login-input-text').each(function() {
                      var id = 'login-text-' + unique++;
                      $(this).attr('id', id);
                      var display = $(this).attr('placeholder');
                      validator.addItem({
                          element: '#' + id,
                          required: true,
                          display: display
                      });
                  });
                  $form.on('click', '.popup-login-close', function(e) {
                      e.preventDefault();
                      ins.remove();
                  });
                  console.log(validator);
                  validator.after('formSuccessHandle', function() {
                      alert(3);
                  })
              }
          } else {
              var formError = res.formError || {};
              var errorFields = formError.fields || [];
              if (errorFields.length) {
                  errorFields = this.transformSelectors(errorFields);
                  this.showErrors(errorFields);
              }
          }
  
      },
  });
  
  // @require ./validator.css

});
