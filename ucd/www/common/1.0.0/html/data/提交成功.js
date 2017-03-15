module.exports = function () {
    return {
        errorCode: 0,
        msg: '表单提交成功',
        formSuccess: {
            //redirect: '/index',
            duration: 3000,
            //tip: 'dfsadfsafads'
        },
        data: {
            html:   '<div class="chat-online-item clf right">' +
                        '<img src="/files/bx/www/common/1.0.0/html/img/test-avatar.png" alt="" class="chat-online-item-avatar">' +
                        '<div class="chat-online-item-content">' +
                            '这是刚才提交的问题' +
                        '</div>' +
                    '</div>'+
                    '<div class="chat-online-item clf left">' +
                        '<img src="/files/bx/www/common/1.0.0/html/img/test-avatar.png" alt="" class="chat-online-item-avatar">' +
                        '<div class="chat-online-item-content">这是刚才的回复</div>' +
                    '</div>'
        }
    }
};