define('com/global/1.0.0:region', ['com/global/1.0.0:dollar', 'com/global/1.0.0:selects'], function(require, exports, module) {

  var $ = require('com/global/1.0.0:dollar');
  var Selects = require('com/global/1.0.0:selects');
  var Region = Selects.extend({
      // 对后台返回的数据进行处理
      convertData: function (level, data) {
          if (level === 1) {
              data.data.unshift([0, '请选择省份'])
          } else if (level === 2) {
              data.data.unshift([0, '请选择市'])
          }
          return data.data;
      },
  
      getUrl: function (level, value) {
          var url = 'http://www.baoxiangj.com/api/area_list';
          //return url;
          if(value === '0') {
              return null;
          }
          if (level === 0) {
              return url + '?callback=?&level=0'
          } else if(level < 2) {
              return url + '?callback=?&areaid=' + value + '&level=' + level;
          } else {
              return null;
          }
      }
  });
  Region.initAll = function () {
      $('.atm-region').each(function () {
  
          var $node = $(this);
          if($node.data('region')) {
              return;
          }
          var arr = [];
          var defaults = $node.data('defaults');
          if (defaults) {
              arr = defaults.split(',');
          }
          var name = $node.data('name') || 'region';
          var region = new Region({
              defaults: arr,
              element: $node,
              selectName: name
          });
          $node.data('region', region);
      });
  };
  module.exports = Region;

});
