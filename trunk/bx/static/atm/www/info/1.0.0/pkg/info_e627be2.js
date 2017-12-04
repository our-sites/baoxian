;/*!www/info/1.0.0:common*/
define("www/info/1.0.0:common",["www/common/1.0.0:common"],function(o){o("www/common/1.0.0:common")});
;/*!www/info/1.0.0:index*/
define("www/info/1.0.0:index",["www/info/1.0.0:common"],function(n){n("www/info/1.0.0:common")});
;/*!www/info/1.0.0:detail*/
define("www/info/1.0.0:detail",["www/info/1.0.0:common"],function(w){w("www/info/1.0.0:common")});
;/*!www/info/1.0.0:info*/
define("www/info/1.0.0:info",["com/global/1.0.0:dollar","www/info/1.0.0:common"],function(o){var n=o("com/global/1.0.0:dollar");o("www/info/1.0.0:common");var l=n(".slide-nav-container");if(l.length){var a=l.offset().top,f=n(window);console.log(a),f.on("load scroll resize",function(){var o=f.scrollTop();o>=a?l.addClass("fn-fixed"):l.removeClass("fn-fixed")})}});