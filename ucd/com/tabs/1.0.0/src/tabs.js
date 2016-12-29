// Tabs

var $ = require('jquery');

var defaults = {
    type: 'mouseover',
    menuNode: null,
    contNode: null,
    className: null,
    callback: null
};

$.fn.tabs = function(options) {

    options = $.extend({}, defaults, options);

    return this.each(function() {
        var $wrapper = $(this),
            $trigger = $(options.menuNode, $wrapper),
            $content = $(options.contNode, $wrapper);

        for (var i = 0, l = $trigger.length; i < l; i += 1) {
            $trigger.eq(i).data('order', i);
        }

        $trigger.on(options.type, function(e) {

            e.preventDefault();

            options.callback && options.callback($(this));

            var order = $(this).data('order');
            $trigger.removeClass(options.className).eq(order).addClass(options.className);
            $content.hide().eq(order).show();

        });

    });
};

