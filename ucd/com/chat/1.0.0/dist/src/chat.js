define('com/chat/1.0.0:chat', ['com/global/1.0.0:dollar', 'lib/art-dialog/6.0.5:art-dialog', 'com/global/1.0.0:validator'], function(require, exports, module) {

  var $ = require('com/global/1.0.0:dollar');
  var dialog = require('lib/art-dialog/6.0.5:art-dialog');
  var Validator = require('com/global/1.0.0:validator');
  var unique = 1;
  var max = 999999999;
  // 咨询弹窗
  $(document).on('click', '.rank-item-consult', function (e) {
      e.preventDefault();
      var chatId = $(this).data('chat-id');
      var chat;
      if (!chatId) {
          chatId = 'chat-'+ unique;
  
          $(this).data('chat-id', chatId);
          unique++;
          var html = $(this).find('.chat-box-wrap').html();
          chat = dialog({
              id: chatId,
              content: html
          });
          chat.showModal();
          var $node = $(chat.node);
          $node.find('.chat-online-close').data('chat-id', chatId);
          var $form = $node.find('form');
          $form.data('chat', chat);
          if ($form.length) {
              var validator = new Validator({
                  element: $form
              });
              validator.before('formSuccessHandle', function(res) {
                  var html = res.data.html;
                  // todo 是否关闭
                  $node.find('.chat-online-body').append(html).scrollTop(max)
                  //setTimeout(function() {
                  //    chat.close();
                  //}, res.formSuccess.duration || res.duration || 3000);
              });
              validator.addItem({
                  element: '.chat-text-field',
                  required: true,
                  display: '咨询内容'
              });
          }
      } else {
          chat = dialog.get(chatId);
          chat && chat.showModal();
      }
      //window.xxx = $node.find('.chat-online-body');
      $node.find('.chat-online-body').scrollTop(max);
  
  
  }).on('click', '.chat-online-close', function (e) {
      e.preventDefault();
      var chatId = $(this).data('chat-id');
      var chat = dialog.get(chatId);
      chat && chat.close();
  }).on('click', '.chat-box .send-btn', function (e) {
      e.preventDefault();
      $(this).closest('form').trigger('submit');
  })
  
  
  
  // @require 'com/chat/1.0.0:chat.css'
  

});
