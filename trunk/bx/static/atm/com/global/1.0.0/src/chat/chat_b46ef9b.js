define("com/global/1.0.0:chat/chat",["com/global/1.0.0:dollar","lib/art-dialog/6.0.5:art-dialog","com/global/1.0.0:validator"],function(a){var t=a("com/global/1.0.0:dollar"),o=a("lib/art-dialog/6.0.5:art-dialog"),l=a("com/global/1.0.0:validator"),e=1,i=999999999;t(document).on("click",".rank-item-consult",function(a){a.preventDefault();var n,c=t(this).data("chat-id");if(c)n=o.get(c),n&&n.showModal();else{c="chat-"+e,t(this).data("chat-id",c),e++;var d=t(this).find(".chat-box-wrap").html();n=o({id:c,content:d}),n.showModal();var r=t(n.node);r.find(".chat-online-close").data("chat-id",c);var h=r.find("form");if(h.data("chat",n),h.length){var f=new l({element:h});f.before("formSuccessHandle",function(a){var t=a.data.html;r.find(".chat-online-body").append(t).scrollTop(i)}),f.addItem({element:".chat-text-field",required:!0,display:"咨询内容"})}}r.find(".chat-online-body").scrollTop(i)}).on("click",".chat-online-close",function(a){a.preventDefault();var l=t(this).data("chat-id"),e=o.get(l);e&&e.close()}).on("click",".chat-box .send-btn",function(a){a.preventDefault(),t(this).closest("form").trigger("submit")})});