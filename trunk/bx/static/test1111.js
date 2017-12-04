/**
 * Created by zhou on 2017/9/26.
server端一共会返回三种数据格式:

 第一种:(正常返回)
 例如:
 a.一般接口
 {"errorCode": 0, "formError": {}, "message": "success", "data": 123}
 b.表单提交接口,username验证失败
 {"errorCode": 0, "formError": {"username":"user is not exist!"}, "message": "", "data": null}

 第二种:(用户无权限)
 例如:
 a.用户未登录,无权限访问此api
 {"errorCode": 403, "formError": {}, "message": "you have no permission to this api", "data": null}

 第三种:(服务端error)
 例如:
 a.服务端的mysql无法访问
 {"errorCode":500,"formError":{},"message":"mysql database is gone away!","data":null}
 */


function ServerApi(errorback_403,errorback_500){
    if(!errorback_403){
        errorback_403=function(data){
            mui.toast(data.message);
        }
    }
    if(!errorback_500){
        errorback_500=function(data){
            mui.toast("服务器开小差了,请稍后重试..");
        }
    }
    function ajax(method,params,callback){
        function _(){
            mui.ajax('https://www.bao361.cn/app/api_gateway/?method='+method,{
                data:params,
                dataType:'json',//服务器返回json格式数据
                type:'post',//HTTP请求类型
                timeout:10000,//超时时间设置为10秒；
                headers:{'Session':window.localStorage.session},
                success:function(data){
                    //服务器返回响应，根据响应结果，分析是否登录成功
                    var errorCode=data.errorCode;
                    if (errorCode==0)
                        callback(data);
                    if(errorCode==500)
                        errorback_500(data);
                    if(errorCode==403)
                        errorback_403(data);


                },
                error:function(xhr,type,errorThrown){
                    //异常处理；
                    console.log(type);
                }
            });
        }
        if (window.localStorage.session){
            mui.ajax('https://www.bao361.cn/app/get_session_key',{
                //data:{
                //    username:'username',
                //    password:'password'
                //},
                dataType:'json',//服务器返回json格式数据
                type:'get',//HTTP请求类型
                timeout:10000,//超时时间设置为10秒；
                headers:{'Content-Type':'application/json'},
                success:function(data){
                    window.localStorage.session=data.data;
                    _();
                },
                error:function(xhr,type,errorThrown){
                    //异常处理；
                    console.log(type);
                }
            });
        }
        else
            _();
    }
    return {"ajax":ajax}
}

//exmaple
//var api=ServerApi(function(x){},function(x){});
//api.ajax("bx.app.views.login.login",{"username":"13523136191","password":"gc7232275"},function(x){});
