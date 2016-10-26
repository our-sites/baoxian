define('com/arale/1.2.0:base', ['com/arale/1.2.0:class', 'com/arale/1.2.0:events', 'com/arale/1.2.0:aspect', 'com/arale/1.2.0:attribute'], function(require, exports, module) {

  // 来源于arale-base 1.2.0
  // ---------
  // Base 是一个基础类，提供 Class、Events、Attrs 和 Aspect 支持。
  
  var Class = require('com/arale/1.2.0:class');
  var Events = require('com/arale/1.2.0:events');
  var Aspect = require('com/arale/1.2.0:aspect');
  var Attribute = require('com/arale/1.2.0:attribute');
  
  
  module.exports = Class.create({
    Implements: [Events, Aspect, Attribute],
  
    initialize: function(config) {
      this.initAttrs(config);
  
      // Automatically register `this._onChangeAttr` method as
      // a `change:attr` event handler.
      parseEventsFromInstance(this, this.attrs);
    },
  
    destroy: function() {
      this.off();
  
      for (var p in this) {
        if (this.hasOwnProperty(p)) {
          delete this[p];
        }
      }
  
      // Destroy should be called only once, generate a fake destroy after called
      // https://github.com/aralejs/widget/issues/50
      this.destroy = function() {};
    }
  });
  
  
  function parseEventsFromInstance(host, attrs) {
    for (var attr in attrs) {
      if (attrs.hasOwnProperty(attr)) {
        var m = '_onChange' + ucfirst(attr);
        if (host[m]) {
          host.on('change:' + attr, host[m]);
        }
      }
    }
  }
  
  function ucfirst(str) {
    return str.charAt(0).toUpperCase() + str.substring(1);
  }
  

});
