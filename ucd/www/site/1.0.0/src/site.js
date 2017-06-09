require('www/common:common.js');

var $ = require('$'),
	$doc = $(document);

//表单的提交
$doc.on('submit', '.reserve-modal-form, .question-advisory-form', function(e) {
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





// @require './site.css'