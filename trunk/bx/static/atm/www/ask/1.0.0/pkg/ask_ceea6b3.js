;/*!www/ask/1.0.0:common*/
define("www/ask/1.0.0:common",["www/common/1.0.0:common","com/global/1.0.0:validator"],function(n){n("www/common/1.0.0:common");var o=n("com/global/1.0.0:validator"),e=$("form#ask");if(e.length){var t=$("#content"),m=$(".current-length"),a=new o({element:e});a.addItem({element:"#content",required:!0,display:"提问内容"}),e.on("keyup","#content",function(){var n=t.val().length;m.html(n)})}});
;/*!www/ask/1.0.0:list*/
define("www/ask/1.0.0:list",["www/ask/1.0.0:common"],function(w){w("www/ask/1.0.0:common")});