define("com/chat/1.0.0:chat",["com/global/1.0.0:dollar","lib/art-dialog/6.0.5:art-dialog","com/global/1.0.0:validator"],function(a){var t=a("com/global/1.0.0:dollar"),e=a("lib/art-dialog/6.0.5:art-dialog"),l=a("com/global/1.0.0:validator"),o=1;t(document).on("click",".rank-item-consult,.i-want-to-ask",function(a){a.preventDefault();var i,d=t(this).data("chat-id");if(d)i=e.get(d),i&&i.showModal();else{d="chat-"+o,t(this).data("chat-id",d),o++;var n=t(this).find(".chat-box-wrap").html();i=e({fixed:!0,id:d,content:n}),i.showModal();var c=t(i.node);c.find(".chat-online-close").data("chat-id",d);var r=c.find("form");if(r.data("chat",i),r.length){var h=new l({element:r});h.addItem({element:".cellphone",required:!0,display:"手机号码"}),h.addItem({element:".ask-text",required:!0,display:"咨询内容"})}}}).on("click",".chat-online-close",function(a){a.preventDefault();var l=t(this).data("chat-id"),o=e.get(l);o&&o.close()})});