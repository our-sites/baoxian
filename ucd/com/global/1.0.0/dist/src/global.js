define('com/global/1.0.0:global', ['lib/jquery/1.11.3:jquery', 'com/global/1.0.0:validator'], function(require, exports, module) {

  var $ = require('lib/jquery/1.11.3:jquery');
  var Validator = require('com/global/1.0.0:validator');
  var $form = $('.bx-header form.ui-form');
  if ($form.length) {
      $form.on('click', '.bx-header-search-box a', function (e) {
          e.preventDefault();
          $form.trigger('submit');
      });
      var validator = new Validator({
          element: $form
      });
      validator.addItem({
          element: '#search-kw',
          required: true,
          display: '搜索内容'
      });
  }
  
  // @require com/global/1.0.0:global.css
  

});
