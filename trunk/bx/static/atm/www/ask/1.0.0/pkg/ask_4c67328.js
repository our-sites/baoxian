;/*!www/ask/1.0.0:common*/
define("www/ask/1.0.0:common",["www/common/1.0.0:common","com/global/1.0.0:dollar","com/global/1.0.0:validator"],function(o){o("www/common/1.0.0:common");var n=o("com/global/1.0.0:dollar"),l=o("com/global/1.0.0:validator"),e=n("form#ask");if(e.length){var m=n("#content"),a=n(".current-length"),t=new l({element:e});t.addItem({element:"#content",required:!0,display:"提问内容"}),e.on("keyup","#content",function(){var o=m.val().length;a.html(o)})}});
;/*!www/ask/1.0.0:list*/
define("www/ask/1.0.0:list",["www/ask/1.0.0:common"],function(w){w("www/ask/1.0.0:common")});