define('www/product/1.0.0:index', ['www/product/1.0.0:common', 'com/global/1.0.0:dollar'], function(require, exports, module) {

  require('www/product/1.0.0:common');
  var $ = require('com/global/1.0.0:dollar');
  //// 条件筛选
  //var $filterWrap = $('.letter-filter');
  //
  //var $keys = $filterWrap.find('[data-key]');
  //var $belongs = $filterWrap.find('[data-belong]');
  //function showAll() {
  //    $keys.removeClass('active').filter('[data-key="all"]').addClass('active');
  //    $belongs.show();
  //}
  //function showLetter(letter) {
  //    $keys.removeClass('active').filter('[data-key="' + letter + '"]').addClass('active');
  //    $belongs.hide().filter('[data-belong="' + letter + '"]').show();
  //}
  //$filterWrap.on('click', '[data-key]', function (e) {
  //    e.preventDefault();
  //    var letter = $(this).data('key');
  //    if (letter === 'all') {
  //        showAll();
  //    } else {
  //        showLetter(letter);
  //    }
  //});
  
  // @require 'www/product/1.0.0:index.css';
  

});
