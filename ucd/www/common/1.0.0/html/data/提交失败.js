module.exports = function () {
    return {
        errorCode: 500,
        formError: {
            fields: [
                {
                    name: 'text',
                    msg: '内容必须填写'
                }
            ]
        }
    }
};