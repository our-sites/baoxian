define('com/global/1.0.0:validator', ['com/validator/0.10.3:validator', 'com/global/1.0.0:dollar', 'lib/toastr/2.1.3:toastr'], function(require, exports, module) {

  var Validator = require('com/validator/0.10.3:validator');
  var $ = require('com/global/1.0.0:dollar');
  var toastr = require('lib/toastr/2.1.3:toastr');
  module.exports = Validator.extend({
  
      // 显示错误
      showError: function (selector, msg) {
          var that = this;
          var item = that.query(selector);
  
          // 强制显示字段的错误信息
          item && that.get('showMessage').call(that, msg, item.element);
      },
  
      // 显示默认错误
      showErrors: function (errorFields) {
          var that = this;
          if ($.isArray(errorFields)) {
              for (var i in errorFields) {
                  var errorField = errorFields[i];
                  that.showError(errorField.selector, errorField.msg);
              }
          }
      },
  
      // 获取表单要提交的数据
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
  
      // 表单出错的处理
      formErrorHandle: function (res) {
          var formError = res.formError || {};
          var errorFields = formError.fields || [];
          if (errorFields.length) {
              errorFields = this.transformSelectors(errorFields);
              this.showErrors(errorFields);
          }
      },
  
      // 表单提交成功的处理
      formSuccessHandle: function (res) {
          var formSuccess = res.formSuccess || {};
          var duration = formSuccess.duration || 5000;
          if (formSuccess.tip !== false) {
              toastr.success(formSuccess.msg || res.msg || '', {timeOut: duration});
          }
          if (formSuccess.redirect) {
              setTimeout(function () {
                  location.href = formSuccess.redirect;
              }, duration);
          }
      },
  
      // ajax提交后的回调函数
      formHandle: function (res) {
          if (res.errorCode) {
              this.formErrorHandle(res);
          } else {
              this.formSuccessHandle(res);
          }
      },
      attrs: {
          autoFocus: false,
          autoSubmit: false,
          failSilently: true,
          onFormValidated: function (error, result, element) {
              // 如果element有data-formIsSubmitting="true" 属性, 则跳出该函数
              if (element.data('form-is-submitting')) {
                  return;
              }
              if (!error) {
                  var that = this;
  
                  var url = element.data('url') || element.attr('action');
                  var method = element.data('method') || element.attr('method') || 'GET';
                  var dataType = element.data('type') || 'json';
                  element.data('form-is-submitting', true);
                  $.ajax({
                      url: url,
                      type: method,
                      dataType: dataType,
                      data: that.getSubmitData(),
                      complete: function () {
                          element.data('form-is-submitting', false);
                      },
                      success: function (res) {
                          that.formHandle(res);
                      }
                  });
  
              }
          }
      }
  });
  
  // @require com/global/1.0.0:validator.css

});
