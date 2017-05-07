define('www/common/1.0.0:common', ['com/global/1.0.0:global', 'com/global/1.0.0:dollar', 'com/tabs/1.0.0:tabs', 'com/global/1.0.0:region', 'lib/slick/1.6.0:slick', 'com/global/1.0.0:validator'], function(require, exports, module) {

  require('com/global/1.0.0:global');
  var $ = require('com/global/1.0.0:dollar');
  require('com/tabs/1.0.0:tabs');
  require('com/global/1.0.0:region').initAll();
  require('lib/slick/1.6.0:slick');
  // var layer = require('layer:layer');
  
  // 代理人模块选项卡
  $('.warmheart-advisers').tabs({
      type: 'click',
      menuNode: '.rank-title-tab a',
      contNode: '.rank-type',
      className: 'active'
  });
  
  // 问吧模块选项卡
  $('.ask-list-left').tabs({
      type: 'click',
      menuNode: '.ask-list-header-tab',
      contNode: '.ask-list-type',
      className: 'active'
  });
  
  // 私人订制模块的验证
  var Validator = require('com/global/1.0.0:validator');
  var $form = $('#custom-form');
  if ($form.length) {
      var validator = new Validator({
          element: $form
      });
      validator.addItem({
          element: '#contact',
          required: true,
          display: '联系电话'
      });
  }
  
  
  // 量身订制模块的验证
  var $form2 = $('#customized-form');
  if ($form2.length) {
      var validator = new Validator({
          element: $form2
      });
      validator.addItem({
          element: '#name',
          required: true
      });
      validator.addItem({
          element: '#cellphone',
          required: true
      });
      validator.addItem({
          element: '#time-frame',
          required: true
      });
  }
  
  // 条件筛选
  $('.letter-filter').each(function () {
      var $filterWrap = $(this);
      var $keys = $filterWrap.find('[data-key]');
      var $belongs = $filterWrap.find('[data-belong]');
  
      function showAll() {
          $keys.removeClass('active').filter('[data-key="all"]').addClass('active');
          $belongs.show();
      }
      function showLetter(letter) {
          $keys.removeClass('active').filter('[data-key="' + letter + '"]').addClass('active');
          $belongs.hide().filter('[data-belong="' + letter + '"]').show();
      }
      $filterWrap.on('click', '[data-key]', function (e) {
          e.preventDefault();
          var letter = $(this).data('key');
          if (letter === 'all') {
              showAll();
          } else {
              showLetter(letter);
          }
      });
  });
  
  
  // 活跃顾问悬浮效果
  var $fixedArea = $('.lively-advisers');
  if ($fixedArea.length) {
      var top = $fixedArea.offset().top;
      var $window = $(window);
      $window.on('load scroll resize', function () {
          var scrollTop = $window.scrollTop();
          if (scrollTop - top > 41) {
              $fixedArea.addClass('fn-fixed');
          } else {
              $fixedArea.removeClass('fn-fixed');
          }
      });
  }
  
  var $messageWrap = $('<div class="bx-rtk-wrap"></div>').appendTo('body');
  $('.bx-rtk').clone().appendTo($messageWrap)
  
  
  // 首先把
  // 顶部消息
  $('.bx-rtk ul').slick({
      dots: false,
      infinite: true,
      arrows: false,
      slidesToShow: 1,
      slidesToScroll: 1,
      vertical: true,
      autoplay: true,
      autoplaySpeed: 2000
  });
  
  var $win = $(window);
  $win.on('scroll resize load', function() {
  	var top = $win.scrollTop();
  	if (top >= 40) {
  		$messageWrap.show();
  	} else {
  		$messageWrap.hide();
  	}
  })
  
  
  // @require 'www/common/1.0.0:common.css';
  

});
