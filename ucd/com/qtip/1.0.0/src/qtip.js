/*
 * @description: qTip v1.0
 * @author: Tony
 * @update: 2013-07-22 by Tony
 */


var $ = require('$'),
    $win = $(window);

$('<style> \
	   #qTip{z-index:9999;width:100%;text-align:center;height:0;} \
	   #qTip .qtip-ok,#qTip .qtip-error{display:inline-block;color:#fff;padding:0 30px;height: 32px;line-height:32px;font-size:14px;box-shadow:1px 1px 3px rgba(0,0,0,.2);*margin-bottom:-32px;*position:relative;} \
	   .qtip-ok{background-color:#5dad52;} \
	   .qtip-error{background-color:#f84a4a;} \
	   </style>').prependTo(document.body);

var ie6 = !window.XMLHttpRequest;

var defaults = {
    text: '',
    type: true,
    top: 0, /* 支持百分比 */
    delayTime: 3000,
    fadeTime: 500
};

var Tips = {
    init: function(opts) {
        var opts = $.extend({}, defaults, opts);
        var	DOM = this.DOM || (this.DOM = this._getDOM());

        this.opts = opts;
        this.wrap = DOM['wrap'];
        this.main = DOM['main'];
        this.clear();

        this.setText(opts.text);
        this.setType(opts.type);
        this.setDelay(opts.delayTime, opts.fadeTime);
        this.setTop(opts.top);

        return this;
    },

    _getDOM: function() {
        var _wrap = $('<div id="qTip" style="position:'+ (ie6 ? 'absolute' : 'fixed') +';" />').prependTo(document.body),
            _main = $('<span />').appendTo(_wrap);
        this._bindFixed();
        return {'wrap': _wrap, 'main': _main};
    },

    _bindFixed: function() {
        var that = this;
        if (ie6) {
            $win.scroll(function() {
                if (that.visible == true) {
                    $win.trigger('fixed-wrap');
                }
            });
        }
    },

    setText: function(text) {
        this.main.html(text);
    },

    setType: function(isOK) {
        var className = isOK ? 'qtip-ok': 'qtip-error';
        this.main.removeClass().addClass(className);
    },

    setTop: function(top) {
        var that = this,
            top = top.toString(),
            top = top.indexOf('%') > -1 ? $win.height() * (parseInt(top, 10) / 100) : parseInt(top, 10);

        if (!that.visible) {
            that.wrap.css({
                'top': top - 50,
                'opacity': 0
            });
        }

        that.visible = true;

        // ie6不加动画
        if (ie6) {
            that.wrap.css('opacity', 1);
            $win.off('fixed-wrap').on('fixed-wrap', function() {
                that.wrap.css('top', ($win.scrollTop() + top) + 'px');
            }).trigger('scroll');
        } else {
            that.wrap.animate({
                'top': top,
                'opacity': 1
            }, 400);
        }
    },

    setDelay: function(delayTime, fadeTime) {
        var that = this;
        this.delay = setTimeout(function() {
            that.animate = that.wrap.animate({
                'top': '-=50px',
                'opacity': 0
            }, 400, function() {
                that.visible = false;
            });
        }, delayTime);
    },

    clear: function() {
        this.delay && clearTimeout(this.delay);
        this.animate && this.animate.stop(true, true);
    }
};

$.qTip = $.qtip = module.exports = function (opts) {
    return Tips.init(opts);
};

