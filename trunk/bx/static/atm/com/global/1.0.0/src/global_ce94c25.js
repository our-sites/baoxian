define("com/global/1.0.0:global",["lib/jquery/1.11.3:jquery","com/global/1.0.0:validator"],function(e){var r=e("lib/jquery/1.11.3:jquery"),a=e("com/global/1.0.0:validator"),l=r(".bx-header form.ui-form");if(l.length){l.on("click",".bx-header-search-box a",function(e){e.preventDefault(),l.trigger("submit")});var o=new a({element:l});o.addItem({element:"#search-kw",required:!0,display:"搜索内容"})}});