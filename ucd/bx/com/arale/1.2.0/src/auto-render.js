// 删掉了autoRenderAll方法
var $ = require('jquery');

// 自动渲染接口，子类可根据自己的初始化逻辑进行覆盖
exports.autoRender = function(config) {
  return new this(config).render()
}


var isDefaultOff = $(document.body).attr('data-api') === 'off'

// 是否没开启 data-api
exports.isDataApiOff = function(element) {
  var elementDataApi = $(element).attr('data-api')

  // data-api 默认开启，关闭只有两种方式：
  //  1. element 上有 data-api="off"，表示关闭单个
  //  2. document.body 上有 data-api="off"，表示关闭所有
  return  elementDataApi === 'off' ||
      (elementDataApi !== 'on' && isDefaultOff)
}