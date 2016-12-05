define('work/user/1.0.0:register', ['work/user/1.0.0:common', 'com/global/1.0.0:validator', 'com/global/1.0.0:dollar', 'com/global/1.0.0:region'], function(require, exports, module) {

  require('work/user/1.0.0:common');
  var Validator = require('com/global/1.0.0:validator');
  
  var $ = require('com/global/1.0.0:dollar');
  var $wrap = $('#Register');
  var activeClass = 'active';
  var $doc = $(document);
  var $form = $wrap.find('form');
  var isCounting = false;
  
  var $getCode = $('#get-code');
  var $mobile = $('#mobile');
  Validator.addRule('checkMobile', function(options, commit) {
      $.getJSON($mobile.data('validate-url') + $mobile.val(), {}, function(res) {
          commit(!res.errorCode, res.msg);
      });
  });
  var validator = new Validator({
      element: $form
  });
  // 初始化地区
  var Region = require('com/global/1.0.0:region');
  Region.initAll();
  
  var Register = {
      init: function () {
          this.roleTab();
      },
      roleTab: function () {
          $wrap.find('.role input[type="radio"]').on('change', function () {
              if($(this).prop('checked')){
                  var label = $(this).parent(),
                      agencyOnly = $wrap.find('.agency-only');
                  label.addClass('active').siblings('label').removeClass('active');
                  if(label.hasClass('agency')){
                      agencyOnly.show();
                  }else{
                      agencyOnly.hide();
                  }
              }
          })
      }
  };
  
  Register.init();
  
  
  (function () {
      validator.addItem({
          element: '#mobile',
          required: true,
          rule: 'mobile checkMobile',
          display:'手机号',
          onItemValidated: function (err, message, element, event) {
              if (!err) {
                  // 验证成功之后,如果不是在倒计时状态,则让按钮变为可点击状态
                  !isCounting && $getCode.addClass(activeClass);
              } else {
                  // 验证失败,让按钮不可点击
                  $getCode.removeClass(activeClass);
              }
          }
      });
  
  
      validator.addItem({
          element: '#safe-code',
          required: true,
          display: '验证码',
          errormessage: '验证码错误'
      }).addItem({
          element: '#email',
          required: true,
          display: '邮箱'
      })
          .addItem({
              element: '#password',
              required: true,
              display: '密码'
          });
  
      $doc.on('click', '#get-code', function (e) {
          e.preventDefault();
          var $this = $(this);
          if ($this.is('.' + activeClass)) {
              var url = $this.data('send-url');
              $.getJSON(url + $('#mobile').val(), {}, function (res) {
                  var html = $getCode.html();
                  if (!res.errorCode) {
                      var defaultDuration = 60000;
                      var duration = res.data ? (res.data.duration || defaultDuration) : defaultDuration;
                      duration = Math.ceil(duration/1000);
                      isCounting = true;
                      setDuration();
                      var interval = setInterval(function () {
                          setDuration();
                          if (duration < 0) {
                              isCounting = false;
                              $getCode.addClass(activeClass).html(html);
                              clearInterval(interval);
                          }
                      }, 1000);
  
                      function setDuration() {
                          $getCode.removeClass(activeClass).html('已发送 ' + duration + 's');
                          duration--
                      }
                  } else {
                      validator.showError('#get-code', res.msg);
                  }
  
              });
  
          }
      });
  
  })();
  
  
  
  // @require work/user/1.0.0:register.css
  

});
