define("com/global/1.0.0:global",["lib/jquery/1.11.3:jquery","com/global/1.0.0:validator","com/chat/1.0.0:chat"],function(e){var a=e("lib/jquery/1.11.3:jquery"),r=e("com/global/1.0.0:validator"),l=a(".bx-header form.ui-form");if(e("com/chat/1.0.0:chat"),l.length){l.on("click",".bx-header-search-box a",function(e){e.preventDefault(),l.trigger("submit")});var o=new r({element:l});o.addItem({element:"#search-kw",required:!0,display:"搜索内容"})}});