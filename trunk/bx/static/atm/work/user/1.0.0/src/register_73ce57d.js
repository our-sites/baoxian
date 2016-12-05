define("work/user/1.0.0:register",["work/user/1.0.0:common","com/global/1.0.0:validator","com/global/1.0.0:dollar","com/global/1.0.0:region"],function(e){e("work/user/1.0.0:common");var a=e("com/global/1.0.0:validator"),o=e("com/global/1.0.0:dollar"),l=o("#Register"),i="active",r=o(document),t=l.find("form"),n=!1,d=o("#get-code"),s=o("#mobile");a.addRule("checkMobile",function(e,a){o.getJSON(s.data("validate-url")+s.val(),{},function(e){a(!e.errorCode,e.msg)})});var c=new a({element:t}),m=e("com/global/1.0.0:region");m.initAll();var u={init:function(){this.roleTab()},roleTab:function(){l.find('.role input[type="radio"]').on("change",function(){if(o(this).prop("checked")){var e=o(this).parent(),a=l.find(".agency-only");e.addClass("active").siblings("label").removeClass("active"),e.hasClass("agency")?a.show():a.hide()}})}};u.init(),function(){c.addItem({element:"#mobile",required:!0,rule:"mobile checkMobile",display:"手机号",onItemValidated:function(e){e?d.removeClass(i):!n&&d.addClass(i)}}),c.addItem({element:"#safe-code",required:!0,display:"验证码",errormessage:"验证码错误"}).addItem({element:"#email",required:!0,display:"邮箱"}).addItem({element:"#password",required:!0,display:"密码"}),r.on("click","#get-code",function(e){e.preventDefault();var a=o(this);if(a.is("."+i)){var l=a.data("send-url");o.getJSON(l+o("#mobile").val(),{},function(e){function a(){d.removeClass(i).html("已发送 "+r+"s"),r--}var o=d.html();if(e.errorCode)c.showError("#get-code",e.msg);else{var l=6e4,r=e.data?e.data.duration||l:l;r=Math.ceil(r/1e3),n=!0,a();var t=setInterval(function(){a(),0>r&&(n=!1,d.addClass(i).html(o),clearInterval(t))},1e3)}})}})}()});