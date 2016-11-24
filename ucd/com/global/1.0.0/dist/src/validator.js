define('com/global/1.0.0:validator', ['com/validator/0.10.3:validator', 'com/global/1.0.0:dollar', 'com/qtip/1.0.0:qtip'], function(require, exports, module) {

  var Validator = require('com/validator/0.10.3:validator');
  var $ = require('com/global/1.0.0:dollar');
  var qtip = require('com/qtip/1.0.0:qtip');
  module.exports = Validator.extend({
  
      // 显示错误
      // info.selector 要提示错误的selector
      // info.message 错误信息
      showError: function (selector, msg) {
          var that = this;
          var item = that.query(selector);
  
          // 强制显示字段的错误信息
          item && that.get('showMessage').call(that, msg, item.element);
      },
      // 显示默认错误
      showErrors: function (arr) {
          var that = this;
          if ($.isArray(arr)) {
              for (var i in arr) {
                  var obj = arr[i];
                  that.showError(obj.selector, obj.msg);
              }
          }
      },
      getSubmitData: function () {
          return this.element.serialize();
      },
  
      // 把返回字段里面的name属性转换为selector
      transformSelectors: function (data, wrapSelector) {
          for (var i in data) {
              var obj = data[i];
              var selector = '[name="' + obj.name + '"]';
              data[i].selector = wrapSelector ? wrapSelector + ' ' + selector : selector;
          }
          return data;
      },
  
      // 返回数据失败时的回调
      resErrorCallback: function (res) {
          res.data = this.transformSelectors(res.data);
          this.showErrors(res.data);
      },
  
      // 返回数据成功时的回调
      resOkCallback: function (res) {
  
          var data = res.data || {};
          var duration = data.duration || 0;
  
          if (res.url) {
              if (!duration) {
                  location.href = res.url;
              } else {
                  setTimeout(function () {
                      location.href = res.url;
                  }, duration);
              }
  
          }
  
          if (data.msg) {
              //popup.alert(data.msg, true, duration);
              qtip({
                  type: true,
                  text: data.msg,
                  delayTime: duration,
                  fadeTime: 0
              });
          }
  
  
      },
  
      // ajax提交后的回调函数
      submitCallback: function (res) {
          if (res.code === 200) {
              this.resOkCallback(res);
          } else {
              if (res.needSafeCode) {
                  var landerVeri = $('#lander-veri');
                  landerVeri.show();
                  var $img = $('#verify-img'),
                      src = $img.attr('src');
                  // 验证码点击
                  $img.on('click', function () {
                      $img.attr('src', src + '&timestamp=' + $.now())
                  });
  
              }
              this.resErrorCallback(res);
          }
      },
      attrs: {
          autoFocus: false,
          autoSubmit: false,
          failSilently: true,
          onFormValidated: function (error, result, element) {
              // 如果element有data-unajax="true" 属性, 则跳出该函数
              if (element.data('unajax')) {
                  return;
              }
              if (!error) {
                  var that = this;
  
                  var url = element.data('url') || element.attr('action');
                  var method = element.data('method') || element.attr('method') || 'GET';
                  var dataType = element.data('type') || 'json';
  
  
                  $.ajax({
                      url: url,
                      type: method,
                      dataType: dataType,
                      data: that.getSubmitData(),
                      success: function (res) {
                          that.submitCallback(res);
                      }
                  });
  
              }
          }
      }
  });
  
  // @require com/global/1.0.0:validator.css

});
