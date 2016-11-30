module.exports = function () {
    return {
        errorCode: 500,
        formError: {
            fields: [
                {
                    name: 'username',
                    msg: '手机号出错'
                }
            ]
        }
    }
};