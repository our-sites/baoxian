### 表单里面的name可以修改,id不可修改
### 通用交互数据格式
```
{
    // 状态码
    errorcode: 0,  // 0表示成功状态,其他可定义一些常见的错误代码

    // 提示信息
    msg: '操作成功/操作失败',

    // 相关数据
    data: {},

    // 表单提交错误
    formError: {
        // 错误字段名及该字段对应的错误信息
        fields: [
            {
                name: 'mobile',         // 错误字段名称
                msg: '手机号出错'         // 错误字段提示信息
            },
            {
                name: 'email',
                msg: '邮箱被占用'
            }
        ]
    },

    formSuccess: {
        // 是否重定向,值为重定向到的地址,若不需要重定向,则设置为null或不留该字段
        redirect: 'http://***/index',

        // 是否同时使用短暂提示
        tip: true

        // 提示停留时间或多长时间后重定向
        duration: 5000,

        // 成功提示信息,若无,则使用上级的msg字段
        msg: '成功提示信息'
    }
}

```

### 注册页手机号交互方式
*. 验证手机号是否被占用的地址, 从手机号字段的 `data-validate-url`属性获取,然后在该地址后面加上手机号进行验证
*. 发送验证码的地址,从 获取验证码 按钮的`data-send-url`属性获取,然后在该地址后面加上手机号向服务器发送异步请求

### 省市区组件


* 给select外面的div增加 atm-region 的class
* 默认值设置: data-defaults="410000,410100" 用逗号隔开
* name设置: data-name="region" 则第一个select的name为region1, 第二级为region2,依次类推

