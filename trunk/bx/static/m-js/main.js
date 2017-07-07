/**
 * Created by zhou on 17/5/31.
 */
function bar_menu_tab(){
    if(jQuery("#bar-menu").is(":visible")){
        jQuery("#bar-menu").hide();
    }
    else {
        jQuery("#bar-menu").show();
    }

}

$(document).ready(function () {
    //initialize swiper when document ready
  var mySwiper = new Swiper('.swiper-container',{
    //pagination: '.swiper-pagination',
    loop:true,
    grabCursor: true,
    paginationClickable: true
  })
  });