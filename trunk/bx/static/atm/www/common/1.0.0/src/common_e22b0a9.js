define("www/common/1.0.0:common",["com/global/1.0.0:global","com/global/1.0.0:dollar","com/tabs/1.0.0:tabs","com/global/1.0.0:region","com/chat/1.0.0:chat","lib/layer/3.0.1:layer","com/global/1.0.0:validator"],function(e){e("com/global/1.0.0:global");var a=e("com/global/1.0.0:dollar");e("com/tabs/1.0.0:tabs"),e("com/global/1.0.0:region").initAll(),e("com/chat/1.0.0:chat");e("lib/layer/3.0.1:layer");a(".warmheart-advisers").tabs({type:"click",menuNode:".rank-title-tab a",contNode:".rank-type",className:"active"});var l=e("com/global/1.0.0:validator"),t=a("#custom-form");if(t.length){var o=new l({element:t});o.addItem({element:"#contact",required:!0,display:"联系电话"})}var i=a("#customized-form");if(i.length){var o=new l({element:i});o.addItem({element:"#name",required:!0}),o.addItem({element:"#cellphone",required:!0}),o.addItem({element:"#time-frame",required:!0})}a(".letter-filter").each(function(){function e(){o.removeClass("active").filter('[data-key="all"]').addClass("active"),i.show()}function l(e){o.removeClass("active").filter('[data-key="'+e+'"]').addClass("active"),i.hide().filter('[data-belong="'+e+'"]').show()}var t=a(this),o=t.find("[data-key]"),i=t.find("[data-belong]");t.on("click","[data-key]",function(t){t.preventDefault();var o=a(this).data("key");"all"===o?(console.log(i.length),e()):l(o)})});var r=a(".lively-advisers");if(r.length){var n=r.offset().top,c=a(window);c.on("load scroll resize",function(){var e=c.scrollTop();e-n>1?r.addClass("fn-fixed"):r.removeClass("fn-fixed")})}});