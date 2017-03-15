/**
 * Created by Administrator on 2016/10/25.
 */
function setPosition(x,y){
    //设置元素的位置
}
function setNum(x){
    //关闭按钮倒计时
}
//假设元素目前的位置是 0， 0
//元素位置过度到0,400 即完成展开
//元素位置回复到0,0 即完成折叠
function  main(){

        //用1秒时间完成展开
        for(var i=1;i<=5;i++){
            setTimeout(function (){
                setPosition(0,400/5*i)
                },1000/5*i)
        }
        setNum(5);//初始化倒计时为5
        //用5秒时间完成倒计时
        for(var j=2;j<=6;j++){
         setTimeout(function(){
             setNum(6-j)
         },1000*j)
        }
        //用一秒时间完成折叠
        for(var k=1;k<=5;k++){
            setTimeout(function (){
                setPosition(0,400-400/5*k)
                },1000/5*k+6000)
        }

}
function getCookie(name)
{
var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
if(arr=document.cookie.match(reg))
return unescape(arr[2]);
else
return null;
}

//注：投保人登陆模态框 和 代理人登陆模态框区别就是name=user_type的一个隐藏input
//投保人：<div style="display:none"><input type="hidden" name="user_type" value="1"></div>
//代理人: <div style="display:none"><input type="hidden" name="user_type" value="2"></div>
///////////////////////////
//模态框中的表单验证及提交方式还用以前那种就行


function isBuyLogin(){  //是否已以投保人身份登陆
    var user_type=getCookie("user_type");
    return user_type==1;
}
function isProxyLogin(){ //是否已以代理人身份登陆
    var user_info=getCookie("user_type");
    return user_info==2
}

function buy_login_window_show(){ //投保人登陆模态框显示

}
function proxy_login_window_show(){//代理人登陆模态框显示

}
document.click=function(event){
    var target_element=event.target;
    var target_element_j=jQuery(target_element);
    if(target_element_j.hasClass("buy_login_required")){
        if (!isBuyLogin){   //未登陆
            buy_login_window_show();
            return false;
        }
    }
    else if(target_element_j.hasClass("proxy_login_required")){
        if(!isProxyLogin()){ //未登陆
            proxy_login_window_show();
            return false;
        }
    }
};