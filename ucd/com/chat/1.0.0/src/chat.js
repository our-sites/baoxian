var $ = require('$');
var dialog = require('art-dialog:art-dialog');
var Validator = require('validator');
var unique = 1;
var max = 999999999;
// 咨询弹窗
$(document).on('click', '.rank-item-consult,.i-want-to-ask', function (e) {
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

            validator.addItem({
                element: '.cellphone',
                required: true,
                display: '手机号码'
            });
            validator.addItem({
                element: '.ask-text',
                required: true,
                display: '咨询内容'
            });
        }
    } else {
        chat = dialog.get(chatId);
        chat && chat.showModal();
    }
    //window.xxx = $node.find('.chat-online-body');
    // $node.find('.chat-online-body').scrollTop(max);


}).on('click', '.chat-online-close', function (e) {
    e.preventDefault();
    var chatId = $(this).data('chat-id');
    var chat = dialog.get(chatId);
    chat && chat.close();
});



// @require './chat.css'
