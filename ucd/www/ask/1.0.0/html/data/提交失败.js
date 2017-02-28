var fs = require('fs');
var path = require('path');
module.exports = function () {
    return {
        errorCode: 800,
        formError: {
            fields: [
                {
                    name: 'username',
                    msg: '手机号出错'
                }
            ]
        },
        data: {
            html: fs.readFileSync(path.join(__dirname, './弹窗.html'), 'utf-8')
        }
    }
};