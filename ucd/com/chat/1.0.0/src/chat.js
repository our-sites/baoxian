var $ = require('$');
var dialog = require('art-dialog:art-dialog');
var Validator = require('validator');
var unique = 1;
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
        if ($form.length) {
            var validator = new Validator({
                element: $form
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

}).on('click', '.chat-online-close', function (e) {
    e.preventDefault();
    var chatId = $(this).data('chat-id');
    var chat = dialog.get(chatId);
    chat && chat.close();
}).on('click', '.chat-box .send-btn', function (e) {
    e.preventDefault();
    $(this).closest('form').trigger('submit');
})



// @require './chat.css'
