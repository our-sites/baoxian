define('www/site/1.0.0:site', ['www/common/1.0.0:common', 'com/global/1.0.0:dollar'], function(require, exports, module) {

  require('www/common/1.0.0:common');
  
  var $ = require('com/global/1.0.0:dollar'),
  	$doc = $(document);
  
  //表单的提交
  $doc.on('submit', '.reserve-modal-form, .question-advisory-form, .advisory-modal form, .ask-question-modal form', function(e) {
  	e.preventDefault();
  	var $this = $(this),
  		_d = $this.serialize(),
  		_u = $this.attr('action'),
  		_m = $this.attr('method').toLowerCase() || 'get';
  	
  	$[_m](_u, _d, function(r) {
  		if(r.status) {
  			alert(r.msg);
  		} else {
  			alert(r.msg);
  		}
  	}, 'json');
  });
  
  //滚动
  var $list = $('.has-reserve-list');
  var tipScroll = setInterval(function() {
  		$list.animate({marginTop: '-44px'}, 1000,function() {
  		
  			var $first = $list.find('li').eq(0).clone();
  			$list.append($first);
  			$list.find('li:first').remove();
  			$list.css('marginTop', 0);
  		});
  		
  	}, 2000);
  
  var $askList = $('.has-ask-box ul');
  var listScroll = setInterval(function() {
  		$askList.animate({marginTop: '-28px'}, 1000, function() {
  			var $first = $askList.find('li').eq(0).clone();
  			$askList.append($first);
  			$askList.find('li:first').remove();
  			$askList.css('marginTop', 0);
  		});
  	}, 2000);
  
  //头部导航当前状态样式
  $doc.on('click', '.header-nav a', function(e) {
  	//e.preventDefault();
  	var $this = $(this);
  	$this.addClass('nav-active');
  	$this.closest('li').siblings().find('a').removeClass('nav-active');
  });
  
  
  // @require 'www/site/1.0.0:site.css'

});
