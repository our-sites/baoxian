define("lib/layer/3.0.1:layer",["lib/jquery/1.11.3:jquery"],function(e,t,i){var n=e("lib/jquery/1.11.3:jquery"),a=n(window),o={getPath:function(){var e=document.scripts,t=e[e.length-1],i=t.src;if(!t.getAttribute("merge"))return i.substring(0,i.lastIndexOf("/")+1)}(),config:{},end:{},minIndex:0,minLeft:[],btn:["&#x786E;&#x5B9A;","&#x53D6;&#x6D88;"],type:["dialog","page","iframe","loading","tips"]},r={v:"3.0.1",ie:function(){var e=navigator.userAgent.toLowerCase();return window.ActiveXObject||"ActiveXObject"in window?(e.match(/msie\s(\d+)/)||[])[1]||"11":!1}(),index:window.layer&&window.layer.v?1e5:0,path:o.getPath,config:function(e){return e=e||{},r.cache=o.config=n.extend({},o.config,e),r.path=o.config.path||r.path,"string"==typeof e.extend&&(e.extend=[e.extend]),e.extend?this:this},alert:function(e,t,i){var a="function"==typeof t;return a&&(i=t),r.open(n.extend({content:e,yes:i},a?{}:t))},confirm:function(e,t,i,a){var l="function"==typeof t;return l&&(a=i,i=t),r.open(n.extend({content:e,btn:o.btn,yes:i,btn2:a},l?{}:t))},msg:function(e,t,i){var a="function"==typeof t,l=o.config.skin,f=(l?l+" "+l+"-msg":"")||"layui-layer-msg",c=s.anim.length-1;return a&&(i=t),r.open(n.extend({content:e,time:3e3,shade:!1,skin:f,title:!1,closeBtn:!1,btn:!1,resize:!1,end:i},a&&!o.config.skin?{skin:f+" layui-layer-hui",anim:c}:function(){return t=t||{},(-1===t.icon||void 0===t.icon&&!o.config.skin)&&(t.skin=f+" "+(t.skin||"layui-layer-hui")),t}()))},load:function(e,t){return r.open(n.extend({type:3,icon:e||0,resize:!1,shade:.01},t))},tips:function(e,t,i){return r.open(n.extend({type:4,content:[e,t],closeBtn:!1,time:3e3,shade:!1,resize:!1,fixed:!1,maxWidth:210},i))}},l=function(e){var t=this;t.index=++r.index,t.config=n.extend({},t.config,o.config,e),document.body?t.creat():setTimeout(function(){t.creat()},50)};l.pt=l.prototype;var s=["layui-layer",".layui-layer-title",".layui-layer-main",".layui-layer-dialog","layui-layer-iframe","layui-layer-content","layui-layer-btn","layui-layer-close"];s.anim=["layer-anim","layer-anim-01","layer-anim-02","layer-anim-03","layer-anim-04","layer-anim-05","layer-anim-06"],s.html=n("html"),l.pt.config={type:0,shade:.3,fixed:!0,move:s[1],title:"&#x4FE1;&#x606F;",offset:"auto",area:"auto",closeBtn:1,time:0,zIndex:19891014,maxWidth:360,anim:0,icon:-1,moveType:1,resize:!0,scrollbar:!0,tips:2},l.pt.vessel=function(e,t){var i=this,a=i.index,r=i.config,l=r.zIndex+a,f="object"==typeof r.title,c=r.maxmin&&(1===r.type||2===r.type),d=r.title?'<div class="layui-layer-title" style="'+(f?r.title[1]:"")+'">'+(f?r.title[0]:r.title)+"</div>":"";return r.zIndex=l,t([r.shade?'<div class="layui-layer-shade" id="layui-layer-shade'+a+'" times="'+a+'" style="'+("z-index:"+(l-1)+"; background-color:"+(r.shade[1]||"#000")+"; opacity:"+(r.shade[0]||r.shade)+"; filter:alpha(opacity="+(100*r.shade[0]||100*r.shade)+");")+'"></div>':"",'<div class="'+s[0]+(" layui-layer-"+o.type[r.type])+(0!=r.type&&2!=r.type||r.shade?"":" layui-layer-border")+" "+(r.skin||"")+'" id="'+s[0]+a+'" type="'+o.type[r.type]+'" times="'+a+'" showtime="'+r.time+'" conType="'+(e?"object":"string")+'" style="z-index: '+l+"; width:"+r.area[0]+";height:"+r.area[1]+(r.fixed?"":";position:absolute;")+'">'+(e&&2!=r.type?"":d)+'<div id="'+(r.id||"")+'" class="layui-layer-content'+(0==r.type&&-1!==r.icon?" layui-layer-padding":"")+(3==r.type?" layui-layer-loading"+r.icon:"")+'">'+(0==r.type&&-1!==r.icon?'<i class="layui-layer-ico layui-layer-ico'+r.icon+'"></i>':"")+(1==r.type&&e?"":r.content||"")+'</div><span class="layui-layer-setwin">'+function(){var e=c?'<a class="layui-layer-min" href="javascript:;"><cite></cite></a><a class="layui-layer-ico layui-layer-max" href="javascript:;"></a>':"";return r.closeBtn&&(e+='<a class="layui-layer-ico '+s[7]+" "+s[7]+(r.title?r.closeBtn:4==r.type?"1":"2")+'" href="javascript:;"></a>'),e}()+"</span>"+(r.btn?function(){var e="";"string"==typeof r.btn&&(r.btn=[r.btn]);for(var t=0,i=r.btn.length;i>t;t++)e+='<a class="'+s[6]+t+'">'+r.btn[t]+"</a>";return'<div class="'+s[6]+" layui-layer-btn-"+(r.btnAlign||"")+'">'+e+"</div>"}():"")+(r.resize?'<span class="layui-layer-resize"></span>':"")+"</div>"],d,n('<div class="layui-layer-move"></div>')),i},l.pt.creat=function(){var e=this,t=e.config,i=e.index,l=t.content,f="object"==typeof l,c=n("body");if(!n("#"+t.id)[0]){switch("string"==typeof t.area&&(t.area="auto"===t.area?["",""]:[t.area,""]),t.shift&&(t.anim=t.shift),6==r.ie&&(t.fixed=!1),t.type){case 0:t.btn="btn"in t?t.btn:o.btn[0],r.closeAll("dialog");break;case 2:var l=t.content=f?t.content:[t.content||"http://layer.layui.com","auto"];t.content='<iframe scrolling="'+(t.content[1]||"auto")+'" allowtransparency="true" id="'+s[4]+i+'" name="'+s[4]+i+'" onload="this.className=\'\';" class="layui-layer-load" frameborder="0" src="'+t.content[0]+'"></iframe>';break;case 3:delete t.title,delete t.closeBtn,-1===t.icon&&0===t.icon,r.closeAll("loading");break;case 4:f||(t.content=[t.content,"body"]),t.follow=t.content[1],t.content=t.content[0]+'<i class="layui-layer-TipsG"></i>',delete t.title,t.tips="object"==typeof t.tips?t.tips:[t.tips,!0],t.tipsMore||r.closeAll("tips")}e.vessel(f,function(a,r,d){c.append(a[0]),f?function(){2==t.type||4==t.type?function(){n("body").append(a[1])}():function(){l.parents("."+s[0])[0]||(l.data("display",l.css("display")).show().addClass("layui-layer-wrap").wrap(a[1]),n("#"+s[0]+i).find("."+s[5]).before(r))}()}():c.append(a[1]),n(".layui-layer-move")[0]||c.append(o.moveElem=d),e.layero=n("#"+s[0]+i),t.scrollbar||s.html.css("overflow","hidden").attr("layer-full",i)}).auto(i),2==t.type&&6==r.ie&&e.layero.find("iframe").attr("src",l[0]),4==t.type?e.tips():e.offset(),t.fixed&&a.on("resize",function(){e.offset(),(/^\d+%$/.test(t.area[0])||/^\d+%$/.test(t.area[1]))&&e.auto(i),4==t.type&&e.tips()}),t.time<=0||setTimeout(function(){r.close(e.index)},t.time),e.move().callback(),s.anim[t.anim]&&e.layero.addClass(s.anim[t.anim]).data("anim",!0)}},l.pt.auto=function(e){function t(e){e=l.find(e),e.height(f[1]-c-d-2*(0|parseFloat(e.css("padding"))))}var i=this,o=i.config,l=n("#"+s[0]+e);""===o.area[0]&&o.maxWidth>0&&(r.ie&&r.ie<8&&o.btn&&l.width(l.innerWidth()),l.outerWidth()>o.maxWidth&&l.width(o.maxWidth));var f=[l.innerWidth(),l.innerHeight()],c=l.find(s[1]).outerHeight()||0,d=l.find("."+s[6]).outerHeight()||0;switch(o.type){case 2:t("iframe");break;default:""===o.area[1]?o.fixed&&f[1]>=a.height()&&(f[1]=a.height(),t("."+s[5])):t("."+s[5])}return i},l.pt.offset=function(){var e=this,t=e.config,i=e.layero,n=[i.outerWidth(),i.outerHeight()],o="object"==typeof t.offset;e.offsetTop=(a.height()-n[1])/2,e.offsetLeft=(a.width()-n[0])/2,o?(e.offsetTop=t.offset[0],e.offsetLeft=t.offset[1]||e.offsetLeft):"auto"!==t.offset&&("t"===t.offset?e.offsetTop=0:"r"===t.offset?e.offsetLeft=a.width()-n[0]:"b"===t.offset?e.offsetTop=a.height()-n[1]:"l"===t.offset?e.offsetLeft=0:"lt"===t.offset?(e.offsetTop=0,e.offsetLeft=0):"lb"===t.offset?(e.offsetTop=a.height()-n[1],e.offsetLeft=0):"rt"===t.offset?(e.offsetTop=0,e.offsetLeft=a.width()-n[0]):"rb"===t.offset?(e.offsetTop=a.height()-n[1],e.offsetLeft=a.width()-n[0]):e.offsetTop=t.offset),t.fixed||(e.offsetTop=/%$/.test(e.offsetTop)?a.height()*parseFloat(e.offsetTop)/100:parseFloat(e.offsetTop),e.offsetLeft=/%$/.test(e.offsetLeft)?a.width()*parseFloat(e.offsetLeft)/100:parseFloat(e.offsetLeft),e.offsetTop+=a.scrollTop(),e.offsetLeft+=a.scrollLeft()),i.attr("minLeft")&&(e.offsetTop=a.height()-(i.find(s[1]).outerHeight()||0),e.offsetLeft=i.css("left")),i.css({top:e.offsetTop,left:e.offsetLeft})},l.pt.tips=function(){var e=this,t=e.config,i=e.layero,o=[i.outerWidth(),i.outerHeight()],r=n(t.follow);r[0]||(r=n("body"));var l={width:r.outerWidth(),height:r.outerHeight(),top:r.offset().top,left:r.offset().left},f=i.find(".layui-layer-TipsG"),c=t.tips[0];t.tips[1]||f.remove(),l.autoLeft=function(){l.left+o[0]-a.width()>0?(l.tipLeft=l.left+l.width-o[0],f.css({right:12,left:"auto"})):l.tipLeft=l.left},l.where=[function(){l.autoLeft(),l.tipTop=l.top-o[1]-10,f.removeClass("layui-layer-TipsB").addClass("layui-layer-TipsT").css("border-right-color",t.tips[1])},function(){l.tipLeft=l.left+l.width+10,l.tipTop=l.top,f.removeClass("layui-layer-TipsL").addClass("layui-layer-TipsR").css("border-bottom-color",t.tips[1])},function(){l.autoLeft(),l.tipTop=l.top+l.height+10,f.removeClass("layui-layer-TipsT").addClass("layui-layer-TipsB").css("border-right-color",t.tips[1])},function(){l.tipLeft=l.left-o[0]-10,l.tipTop=l.top,f.removeClass("layui-layer-TipsR").addClass("layui-layer-TipsL").css("border-bottom-color",t.tips[1])}],l.where[c-1](),1===c?l.top-(a.scrollTop()+o[1]+16)<0&&l.where[2]():2===c?a.width()-(l.left+l.width+o[0]+16)>0||l.where[3]():3===c?l.top-a.scrollTop()+l.height+o[1]+16-a.height()>0&&l.where[0]():4===c&&o[0]+16-l.left>0&&l.where[1](),i.find("."+s[5]).css({"background-color":t.tips[1],"padding-right":t.closeBtn?"30px":""}),i.css({left:l.tipLeft-(t.fixed?a.scrollLeft():0),top:l.tipTop-(t.fixed?a.scrollTop():0)})},l.pt.move=function(){var e=this,t=e.config,i=n(document),l=e.layero,s=l.find(t.move),f=l.find(".layui-layer-resize"),c={};return t.move&&s.css("cursor","move"),s.on("mousedown",function(e){e.preventDefault(),t.move&&(c.moveStart=!0,c.offset=[e.clientX-parseFloat(l.css("left")),e.clientY-parseFloat(l.css("top"))],o.moveElem.css("cursor","move").show())}),f.on("mousedown",function(e){e.preventDefault(),c.resizeStart=!0,c.offset=[e.clientX,e.clientY],c.area=[l.outerWidth(),l.outerHeight()],o.moveElem.css("cursor","se-resize").show()}),i.on("mousemove",function(i){if(c.moveStart){var n=i.clientX-c.offset[0],o=i.clientY-c.offset[1],s="fixed"===l.css("position");if(i.preventDefault(),c.stX=s?0:a.scrollLeft(),c.stY=s?0:a.scrollTop(),!t.moveOut){var f=a.width()-l.outerWidth()+c.stX,d=a.height()-l.outerHeight()+c.stY;n<c.stX&&(n=c.stX),n>f&&(n=f),o<c.stY&&(o=c.stY),o>d&&(o=d)}l.css({left:n,top:o})}if(t.resize&&c.resizeStart){var n=i.clientX-c.offset[0],o=i.clientY-c.offset[1];i.preventDefault(),r.style(e.index,{width:c.area[0]+n,height:c.area[1]+o}),c.isResize=!0}}).on("mouseup",function(){c.moveStart&&(delete c.moveStart,o.moveElem.hide(),t.moveEnd&&t.moveEnd()),c.resizeStart&&(delete c.resizeStart,o.moveElem.hide())}),e},l.pt.callback=function(){function e(){var e=a.cancel&&a.cancel(t.index,i);e===!1||r.close(t.index)}var t=this,i=t.layero,a=t.config;t.openLayer(),a.success&&(2==a.type?i.find("iframe").on("load",function(){a.success(i,t.index)}):a.success(i,t.index)),6==r.ie&&t.IE6(i),i.find("."+s[6]).children("a").on("click",function(){var e=n(this).index();if(0===e)a.yes?a.yes(t.index,i):a.btn1?a.btn1(t.index,i):r.close(t.index);else{var o=a["btn"+(e+1)]&&a["btn"+(e+1)](t.index,i);o===!1||r.close(t.index)}}),i.find("."+s[7]).on("click",e),a.shadeClose&&n("#layui-layer-shade"+t.index).on("click",function(){r.close(t.index)}),i.find(".layui-layer-min").on("click",function(){var e=a.min&&a.min(i);e===!1||r.min(t.index,a)}),i.find(".layui-layer-max").on("click",function(){n(this).hasClass("layui-layer-maxmin")?(r.restore(t.index),a.restore&&a.restore(i)):(r.full(t.index,a),setTimeout(function(){a.full&&a.full(i)},100))}),a.end&&(o.end[t.index]=a.end)},o.reselect=function(){n.each(n("select"),function(){var e=n(this);e.parents("."+s[0])[0]||1==e.attr("layer")&&n("."+s[0]).length<1&&e.removeAttr("layer").show(),e=null})},l.pt.IE6=function(){n("select").each(function(){var e=n(this);e.parents("."+s[0])[0]||"none"===e.css("display")||e.attr({layer:"1"}).hide(),e=null})},l.pt.openLayer=function(){var e=this;r.zIndex=e.config.zIndex,r.setTop=function(e){var t=function(){r.zIndex++,e.css("z-index",r.zIndex+1)};return r.zIndex=parseInt(e[0].style.zIndex),e.on("mousedown",t),r.zIndex}},o.record=function(e){var t=[e.width(),e.height(),e.position().top,e.position().left+parseFloat(e.css("margin-left"))];e.find(".layui-layer-max").addClass("layui-layer-maxmin"),e.attr({area:t})},o.rescollbar=function(e){s.html.attr("layer-full")==e&&(s.html[0].style.removeProperty?s.html[0].style.removeProperty("overflow"):s.html[0].style.removeAttribute("overflow"),s.html.removeAttr("layer-full"))},window.layer=r,r.getChildFrame=function(e,t){return t=t||n("."+s[4]).attr("times"),n("#"+s[0]+t).find("iframe").contents().find(e)},r.getFrameIndex=function(e){return n("#"+e).parents("."+s[4]).attr("times")},r.iframeAuto=function(e){if(e){var t=r.getChildFrame("html",e).outerHeight(),i=n("#"+s[0]+e),a=i.find(s[1]).outerHeight()||0,o=i.find("."+s[6]).outerHeight()||0;i.css({height:t+a+o}),i.find("iframe").css({height:t})}},r.iframeSrc=function(e,t){n("#"+s[0]+e).find("iframe").attr("src",t)},r.style=function(e,t,i){{var a=n("#"+s[0]+e),r=a.find(".layui-layer-content"),l=a.attr("type"),f=a.find(s[1]).outerHeight()||0,c=a.find("."+s[6]).outerHeight()||0;a.attr("minLeft")}l!==o.type[3]&&l!==o.type[4]&&(i||(parseFloat(t.width)<=260&&(t.width=260),parseFloat(t.height)-f-c<=64&&(t.height=64+f+c)),a.css(t),c=a.find("."+s[6]).outerHeight(),l===o.type[2]?a.find("iframe").css({height:parseFloat(t.height)-f-c}):r.css({height:parseFloat(t.height)-f-c-parseFloat(r.css("padding-top"))-parseFloat(r.css("padding-bottom"))}))},r.min=function(e){var t=n("#"+s[0]+e),i=t.find(s[1]).outerHeight()||0,l=t.attr("minLeft")||181*o.minIndex+"px",f=t.css("position");o.record(t),o.minLeft[0]&&(l=o.minLeft[0],o.minLeft.shift()),t.attr("position",f),r.style(e,{width:180,height:i,left:l,top:a.height()-i,position:"fixed",overflow:"hidden"},!0),t.find(".layui-layer-min").hide(),"page"===t.attr("type")&&t.find(s[4]).hide(),o.rescollbar(e),t.attr("minLeft")||o.minIndex++,t.attr("minLeft",l)},r.restore=function(e){{var t=n("#"+s[0]+e),i=t.attr("area").split(",");t.attr("type")}r.style(e,{width:parseFloat(i[0]),height:parseFloat(i[1]),top:parseFloat(i[2]),left:parseFloat(i[3]),position:t.attr("position"),overflow:"visible"},!0),t.find(".layui-layer-max").removeClass("layui-layer-maxmin"),t.find(".layui-layer-min").show(),"page"===t.attr("type")&&t.find(s[4]).show(),o.rescollbar(e)},r.full=function(e){var t,i=n("#"+s[0]+e);o.record(i),s.html.attr("layer-full")||s.html.css("overflow","hidden").attr("layer-full",e),clearTimeout(t),t=setTimeout(function(){var t="fixed"===i.css("position");r.style(e,{top:t?0:a.scrollTop(),left:t?0:a.scrollLeft(),width:a.width(),height:a.height()},!0),i.find(".layui-layer-min").hide()},100)},r.title=function(e,t){var i=n("#"+s[0]+(t||r.index)).find(s[1]);i.html(e)},r.close=function(e){var t=n("#"+s[0]+e),i=t.attr("type"),a="layer-anim-close";if(t[0]){var l="layui-layer-wrap",f=function(){if(i===o.type[1]&&"object"===t.attr("conType")){t.children(":not(."+s[5]+")").remove();for(var a=t.find("."+l),r=0;2>r;r++)a.unwrap();a.css("display",a.data("display")).removeClass(l)}else{if(i===o.type[2])try{var f=n("#"+s[4]+e)[0];f.contentWindow.document.write(""),f.contentWindow.close(),t.find("."+s[5])[0].removeChild(f)}catch(c){}t[0].innerHTML="",t.remove()}"function"==typeof o.end[e]&&o.end[e](),delete o.end[e]};t.data("anim")&&t.addClass(a),n("#layui-layer-moves, #layui-layer-shade"+e).remove(),6==r.ie&&o.reselect(),o.rescollbar(e),t.attr("minLeft")&&(o.minIndex--,o.minLeft.push(t.attr("minLeft"))),setTimeout(function(){f()},r.ie&&r.ie<10||!t.data("anim")?0:200)}},r.closeAll=function(e){n.each(n("."+s[0]),function(){var t=n(this),i=e?t.attr("type")===e:1;i&&r.close(t.attr("times")),i=null})};var f=r.cache||{},c=function(e){return f.skin?" "+f.skin+" "+f.skin+"-"+e:""};r.prompt=function(e,t){var i="";if(e=e||{},"function"==typeof e&&(t=e),e.area){var o=e.area;i='style="width: '+o[0]+"; height: "+o[1]+';"',delete e.area}var l,s=2==e.formType?'<textarea class="layui-layer-input"'+i+">"+(e.value||"")+"</textarea>":function(){return'<input type="'+(1==e.formType?"password":"text")+'" class="layui-layer-input" value="'+(e.value||"")+'">'}();return r.open(n.extend({type:1,btn:["&#x786E;&#x5B9A;","&#x53D6;&#x6D88;"],content:s,skin:"layui-layer-prompt"+c("prompt"),maxWidth:a.width(),success:function(e){l=e.find(".layui-layer-input"),l.focus()},resize:!1,yes:function(i){var n=l.val();""===n?l.focus():n.length>(e.maxlength||500)?r.tips("&#x6700;&#x591A;&#x8F93;&#x5165;"+(e.maxlength||500)+"&#x4E2A;&#x5B57;&#x6570;",l,{tips:1}):t&&t(n,i,l)}},e))},r.tab=function(e){e=e||{};var t=e.tab||{};return r.open(n.extend({type:1,skin:"layui-layer-tab"+c("tab"),resize:!1,title:function(){var e=t.length,i=1,n="";if(e>0)for(n='<span class="layui-layer-tabnow">'+t[0].title+"</span>";e>i;i++)n+="<span>"+t[i].title+"</span>";return n}(),content:'<ul class="layui-layer-tabmain">'+function(){var e=t.length,i=1,n="";if(e>0)for(n='<li class="layui-layer-tabli xubox_tab_layer">'+(t[0].content||"no content")+"</li>";e>i;i++)n+='<li class="layui-layer-tabli">'+(t[i].content||"no  content")+"</li>";return n}()+"</ul>",success:function(t){var i=t.find(".layui-layer-title").children(),a=t.find(".layui-layer-tabmain").children();i.on("mousedown",function(t){t.stopPropagation?t.stopPropagation():t.cancelBubble=!0;var i=n(this),o=i.index();i.addClass("layui-layer-tabnow").siblings().removeClass("layui-layer-tabnow"),a.eq(o).show().siblings().hide(),"function"==typeof e.change&&e.change(o)})}},e))},r.photos=function(e,t,i){function a(e,t,i){var n=new Image;return n.src=e,n.complete?t(n):(n.onload=function(){n.onload=null,t(n)},void(n.onerror=function(e){n.onerror=null,i(e)}))}var o={};if(e=e||{},e.photos){var l=e.photos.constructor===Object,s=l?e.photos:{},f=s.data||[],d=s.start||0;if(o.imgIndex=(0|d)+1,e.img=e.img||"img",l){if(0===f.length)return r.msg("&#x6CA1;&#x6709;&#x56FE;&#x7247;")}else{var u=n(e.photos),y=function(){f=[],u.find(e.img).each(function(e){var t=n(this);t.attr("layer-index",e),f.push({alt:t.attr("alt"),pid:t.attr("layer-pid"),src:t.attr("layer-src")||t.attr("src"),thumb:t.attr("src")})})};if(y(),0===f.length)return;if(t||u.on("click",e.img,function(){var t=n(this),i=t.attr("layer-index");r.photos(n.extend(e,{photos:{start:i,data:f,tab:e.tab},full:e.full}),!0),y()}),!t)return}o.imgprev=function(e){o.imgIndex--,o.imgIndex<1&&(o.imgIndex=f.length),o.tabimg(e)},o.imgnext=function(e,t){o.imgIndex++,o.imgIndex>f.length&&(o.imgIndex=1,t)||o.tabimg(e)},o.keyup=function(e){if(!o.end){var t=e.keyCode;e.preventDefault(),37===t?o.imgprev(!0):39===t?o.imgnext(!0):27===t&&r.close(o.index)}},o.tabimg=function(t){f.length<=1||(s.start=o.imgIndex-1,r.close(o.index),r.photos(e,!0,t))},o.event=function(){o.bigimg.hover(function(){o.imgsee.show()},function(){o.imgsee.hide()}),o.bigimg.find(".layui-layer-imgprev").on("click",function(e){e.preventDefault(),o.imgprev()}),o.bigimg.find(".layui-layer-imgnext").on("click",function(e){e.preventDefault(),o.imgnext()}),n(document).on("keyup",o.keyup)},o.loadi=r.load(1,{shade:"shade"in e?!1:.9,scrollbar:!1}),a(f[d].src,function(t){r.close(o.loadi),o.index=r.open(n.extend({type:1,area:function(){var i=[t.width,t.height],a=[n(window).width()-100,n(window).height()-100];if(!e.full&&(i[0]>a[0]||i[1]>a[1])){var o=[i[0]/a[0],i[1]/a[1]];o[0]>o[1]?(i[0]=i[0]/o[0],i[1]=i[1]/o[0]):o[0]<o[1]&&(i[0]=i[0]/o[1],i[1]=i[1]/o[1])}return[i[0]+"px",i[1]+"px"]}(),title:!1,shade:.9,shadeClose:!0,closeBtn:!1,move:".layui-layer-phimg img",moveType:1,scrollbar:!1,moveOut:!0,anim:5*Math.random()|0,skin:"layui-layer-photos"+c("photos"),content:'<div class="layui-layer-phimg"><img src="'+f[d].src+'" alt="'+(f[d].alt||"")+'" layer-pid="'+f[d].pid+'"><div class="layui-layer-imgsee">'+(f.length>1?'<span class="layui-layer-imguide"><a href="javascript:;" class="layui-layer-iconext layui-layer-imgprev"></a><a href="javascript:;" class="layui-layer-iconext layui-layer-imgnext"></a></span>':"")+'<div class="layui-layer-imgbar" style="display:'+(i?"block":"")+'"><span class="layui-layer-imgtit"><a href="javascript:;">'+(f[d].alt||"")+"</a><em>"+o.imgIndex+"/"+f.length+"</em></span></div></div></div>",success:function(t){o.bigimg=t.find(".layui-layer-phimg"),o.imgsee=t.find(".layui-layer-imguide,.layui-layer-imgbar"),o.event(t),e.tab&&e.tab(f[d],t)},end:function(){o.end=!0,n(document).off("keyup",o.keyup)}},e))},function(){r.close(o.loadi),r.msg("&#x5F53;&#x524D;&#x56FE;&#x7247;&#x5730;&#x5740;&#x5F02;&#x5E38;<br>&#x662F;&#x5426;&#x7EE7;&#x7EED;&#x67E5;&#x770B;&#x4E0B;&#x4E00;&#x5F20;&#xFF1F;",{time:3e4,btn:["&#x4E0B;&#x4E00;&#x5F20;","&#x4E0D;&#x770B;&#x4E86;"],yes:function(){f.length>1&&o.imgnext(!0,!0)}})})}},r.open=function(e){var t=new l(e);return t.index},i.exports=r});