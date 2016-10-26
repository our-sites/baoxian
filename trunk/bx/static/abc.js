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