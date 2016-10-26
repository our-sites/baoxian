define("com/arale/1.2.0:widget",["lib/jquery/1.11.3:jquery","com/arale/1.2.0:base","com/arale/1.2.0:daparser","com/arale/1.2.0:auto-render"],function(e,t,n){function i(){return"widget-"+b++}function r(e){return"[object String]"===w.call(e)}function s(e){return"[object Function]"===w.call(e)}function l(e){return x(document.documentElement,e)}function a(e){return e.charAt(0).toUpperCase()+e.substring(1)}function o(e){return s(e.events)&&(e.events=e.events()),e.events}function u(e,t){var n=e.match(C),i=n[1]+g+t.cid,r=n[2]||void 0;return r&&r.indexOf("{{")>-1&&(r=h(r,t)),{type:i,selector:r}}function h(e,t){return e.replace(R,function(e,n){for(var i,s=n.split("."),l=t;i=s.shift();)l=l===t.attrs?t.get(i):l[i];return r(l)?l:j})}function c(e){return null==e||void 0===e}function d(e){for(var t=e.length-1;t>=0&&void 0===e[t];t--)e.pop();return e}var m=e("lib/jquery/1.11.3:jquery"),f=e("com/arale/1.2.0:base"),p=e("com/arale/1.2.0:daparser"),v=e("com/arale/1.2.0:auto-render"),g=".delegate-events-",E="_onRender",y="data-widget-cid",_={},A=f.extend({propsInAttrs:["initElement","element","events"],element:null,events:null,attrs:{id:null,className:null,style:null,template:"<div></div>",model:null,parentNode:document.body},initialize:function(e){this.cid=i();var t=this._parseDataAttrsConfig(e);A.superclass.initialize.call(this,e?m.extend(t,e):t),this.parseElement(),this.initProps(),this.delegateEvents(),this.setup(),this._stamp(),this._isTemplate=!(e&&e.element)},_parseDataAttrsConfig:function(e){var t,n;return e&&(t=m(e.initElement?e.initElement:e.element)),t&&t[0]&&!v.isDataApiOff(t)&&(n=p.parseElement(t)),n},parseElement:function(){var e=this.element;if(e?this.element=m(e):this.get("template")&&this.parseElementFromTemplate(),!this.element||!this.element[0])throw new Error("element is invalid")},parseElementFromTemplate:function(){this.element=m(this.get("template"))},initProps:function(){},delegateEvents:function(e,t,n){var i=d(Array.prototype.slice.call(arguments));if(0===i.length?(t=o(this),e=this.element):1===i.length?(t=e,e=this.element):2===i.length?(n=t,t=e,e=this.element):(e||(e=this.element),this._delegateElements||(this._delegateElements=[]),this._delegateElements.push(m(e))),r(t)&&s(n)){var l={};l[t]=n,t=l}for(var a in t)if(t.hasOwnProperty(a)){var h=u(a,this),c=h.type,f=h.selector;!function(t,n){var i=function(e){s(t)?t.call(n,e):n[t](e)};f?m(e).on(c,f,i):m(e).on(c,i)}(t[a],this)}return this},undelegateEvents:function(e,t){var n=d(Array.prototype.slice.call(arguments));if(t||(t=e,e=null),0===n.length){var i=g+this.cid;if(this.element&&this.element.off(i),this._delegateElements)for(var r in this._delegateElements)this._delegateElements.hasOwnProperty(r)&&this._delegateElements[r].off(i)}else{var s=u(t,this);e?m(e).off(s.type,s.selector):this.element&&this.element.off(s.type,s.selector)}return this},setup:function(){},render:function(){this.rendered||(this._renderAndBindAttrs(),this.rendered=!0);var e=this.get("parentNode");if(e&&!l(this.element[0])){var t=this.constructor.outerBoxClass;if(t){var n=this._outerBox=m("<div></div>").addClass(t);n.append(this.element).appendTo(e)}else this.element.appendTo(e)}return this},_renderAndBindAttrs:function(){var e=this,t=e.attrs;for(var n in t)if(t.hasOwnProperty(n)){var i=E+a(n);if(this[i]){var r=this.get(n);c(r)||this[i](r,void 0,n),function(t){e.on("change:"+n,function(n,i,r){e[t](n,i,r)})}(i)}}},_onRenderId:function(e){this.element.attr("id",e)},_onRenderClassName:function(e){this.element.addClass(e)},_onRenderStyle:function(e){this.element.css(e)},_stamp:function(){var e=this.cid;(this.initElement||this.element).attr(y,e),_[e]=this},$:function(e){return this.element.find(e)},destroy:function(){this.undelegateEvents(),delete _[this.cid],this.element&&this._isTemplate&&(this.element.off(),this._outerBox?this._outerBox.remove():this.element.remove()),this.element=null,A.superclass.destroy.call(this)}});m(window).unload(function(){for(var e in _)_[e].destroy()}),A.query=function(e){var t,n=m(e).eq(0);return n&&(t=n.attr(y)),_[t]},A.autoRender=v.autoRender,A.StaticsWhiteList=["autoRender"],n.exports=A;var w=Object.prototype.toString,b=0,x=m.contains||function(e,t){return!!(16&e.compareDocumentPosition(t))},C=/^(\S+)\s*(.*)$/,R=/{{([^}]+)}}/g,j="INVALID_SELECTOR"});