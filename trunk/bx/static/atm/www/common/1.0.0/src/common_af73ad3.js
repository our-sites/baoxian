define("www/common/1.0.0:common",["com/global/1.0.0:global","com/global/1.0.0:dollar","com/tabs/1.0.0:tabs","com/global/1.0.0:region","lib/slick/1.6.0:slick","com/global/1.0.0:validator"],function(e){e("com/global/1.0.0:global");var a=e("com/global/1.0.0:dollar");e("com/tabs/1.0.0:tabs"),e("com/global/1.0.0:region").initAll(),e("lib/slick/1.6.0:slick"),a(".warmheart-advisers").tabs({type:"click",menuNode:".rank-title-tab a",contNode:".rank-type",className:"active"}),a(".ask-list-left").tabs({type:"click",menuNode:".ask-list-header-tab",contNode:".ask-list-type",className:"active"});var l=e("com/global/1.0.0:validator"),o=a("#custom-form");if(o.length){var t=new l({element:o});t.addItem({element:"#contact",required:!0,display:"联系电话"})}var i=a("#customized-form");if(i.length){var t=new l({element:i});t.addItem({element:"#name",required:!0}),t.addItem({element:"#cellphone",required:!0}),t.addItem({element:"#time-frame",required:!0})}a(".letter-filter").each(function(){function e(){t.removeClass("active").filter('[data-key="all"]').addClass("active"),i.show()}function l(e){t.removeClass("active").filter('[data-key="'+e+'"]').addClass("active"),i.hide().filter('[data-belong="'+e+'"]').show()}var o=a(this),t=o.find("[data-key]"),i=o.find("[data-belong]");o.on("click","[data-key]",function(o){o.preventDefault();var t=a(this).data("key");"all"===t?e():l(t)})});var r=a(".lively-advisers");if(r.length){var s=r.offset().top,n=a(window);n.on("load scroll resize",function(){var e=n.scrollTop();e-s>41?r.addClass("fn-fixed"):r.removeClass("fn-fixed")})}var c=a('<div class="bx-rtk-wrap"></div>').appendTo("body");a(".bx-rtk").clone().appendTo(c),a.getJSON("//www.bao361.cn/top_roll_message_api",function(e){var l="";e&&(e.forEach(function(e){l+='<li><a href="'+e.url+'">'+e.msg+"</a></li>"}),a(".bx-rtk ul").html(l).slick({dots:!1,infinite:!0,arrows:!1,slidesToShow:1,slidesToScroll:1,vertical:!0,autoplay:!0,autoplaySpeed:2e3}))});var d=a(window);d.on("scroll resize load",function(){var e=d.scrollTop();e>=40?c.show():c.hide()})});