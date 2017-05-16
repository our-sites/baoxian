var dialog = require('common/artdialog:dialog'),
    $ = require('jquery');
var Placeholder = require('common/placeholder:placeholder');
require('./vendor/fileupload');
require('./vendor/iframe-transport');

// @require ./style.css
// @require ./venderflie.css
module.exports = {
    init: function($node, ins) {

        var load_flag=null;

        $('.main-container').scroll(function(e){

            if (load_flag){
                return;
            }


            if(tabPage.getHref() !== tabPage.getIns().getHref($node)) {
                return;
            }
            var manHeight=$(this).height();
            var itemHeight=$(this).find('.man-item').outerHeight();
            var lasttime=$(".man-item>li:last-child").attr('data-time');
            if(lasttime==0){return;}
            if((itemHeight-manHeight)<=($(this).scrollTop()+30)){
                if($(".loadding").length>=1)return;
                $(this).find('.man-item').append("<div class='loadding'>加载中...<img src='images/loadding.gif' /></div>");
                $(this).animate({"scrollTop":$(this).find('.man-item').outerHeight()-$(this).height()+'px'},500);
                $.ajax({
                    url:"//work.supsite.net/resource/index/fileajax?addtime=" + lasttime,
                    type:'post',
                    dataType:"json",
                    data:{addtime:lasttime},
                    success:function(data){
                        if(data.data==null){
                            load_flag=1;
                            $(".man-filelist li:last-child").attr('data-time','0');
                        }else{
                            $(".man-filelist .loadding").before(DataSorting(data.data));
                        }

                        $(".loadding").remove();
                    },
                    error:function(e){

                    }

                })
            }
        })
        // 滚动加载li
        // alert($node.find(".man-filelist").length);
        // $node.find(".man-filelist").scroll(function(e){
        //     var manHeight=$(this).height();
        //     var itemHeight=$(this).find('.man-item').outerHeight();
        //     var lasttime=$("#resexe li:last-child").attr('data-time');
        //     if(lasttime==0){return;}
        //     if((itemHeight-manHeight)<=($(this).scrollTop()+30)){
        //         if($(".loadding").length>=1)return;
        //         $(this).find('.man-item').append("<div class='loadding'>加载中...<img src='images/loadding.gif' /></div>");
        //         $(this).animate({"scrollTop":$(this).find('.man-item').outerHeight()-$(this).height()+'px'},500);
        //         $.ajax({
        //             url:"//work.supsite.net/resource/index/fileajax?addtime" + lasttime,
        //             type:'post',
        //             dataType:"json",
        //             data:{addtime:lasttime},
        //             success:function(data){
        //                 console.log(data);
        //                 if(data.data==null){
        //                     $("#resexe li:last-child").attr('data-time','0');
        //                 }else{
        //                     $("#resexe .loadding").before(DataSorting(data.data));
        //                 }
        //
        //                 $(".loadding").remove();
        //             },
        //             error:function(e){
        //
        //             }
        //
        //         })
        //     }
        // })


        //选中
        $node.find(".man-filelist").delegate('li i', 'click', function() {
            $(this).parent().toggleClass('selected');
            selectState();

        })

        //全选
        $node.find(".man-breadcrumb label").click(function() {
            $(this).find('i').toggleClass('all');
            if($(this).find('i').hasClass('all')) {
                $(".man-filelist li").not($('.dir')).addClass('selected');
                $(".dir").removeClass('selected');
            } else {
                $(".man-filelist li").not($('.dir')).removeClass('selected');
            }
            selectState();

        })

        //新建分组
        $node.find("#createGroup").bind('click', function() {

            var createjust = $('#createGroup').attr('data-href');

            //新建分组
            var cate = dialog({
                title: '新建分组',
                content: '<textarea id="cateDir"  placeholder="一行标示新建一个分组，已添加过的分组将自动忽略" ></textarea>',
                skin: 'myalert rename create',
                okValue: '保存',
                ok: function() {
                    var dir = $.trim($("#cateDir").val());
                    var dirArr = dir.split("\n");
                    if(!dir){return false;}
                    console.log(dirArr)
                    $.ajax({
                        url: createjust, //新件文件夹接口地址
                        type: 'post',
                        dataType: "json",
                        data: {
                            cateArr: dirArr
                        },
                        success: function(data) {
                            cate.close().remove();
                            console.log(data);
                            if(data.errorcode == 0) {
                                for(var i = 0; i < data.data.length; i++) {
                                    $node.find(".man-filelist #direxe").prepend("<li class='dir' data-id='" + data.data[i]['_id'] + "'><em>松开移动文件</em><i></i><p><a href='javascript:;'>" + data.data[i]['catename'] + "</a></p></li>");
                                }
                                var d = dialog({
                                    skin: "mymessage",
                                    content: '√ 新建成功'
                                });
                                d.show();
                                setTimeout(function() {
                                    d.close().remove();
                                }, 2000);

                            } else {
                                myalert("新建失败！");
                            }
                        },
                        error: function(e) {

                        }

                    })

                    return false;
                },
                cancelValue: '取消',
                cancel: function() {}
            }).showModal();

        })

        function get_selected_type(){
            //获取到被选中的这些项的类型
            var selected = $(".man-item .selected");
            if(selected.length==0){
                return null;
            }
            else {
                var result=[];
                selected.map(function(_i,_) {
                    result=result.concat(jQuery(_).parent().attr("id"))
                })
                return result;
            }

        }

        //重命名
        $node.find("#rename").bind('click', function() {
            var newnameys = $('#rename').attr('data-href');   //  获取重命名url
            if(!$(this).hasClass('on')) return;
            var _id = $(".man-filelist li.selected").attr("data-id");
            var oldName = $(".man-filelist li.selected p").text();
            //重命名
            var d = dialog({
                title: '重命名',
                content: '<span>分组名：</span><input id="re_name" type="type" value="'+oldName+'" />',
                skin: 'myalert rename',
                okValue: '保存',
                ok: function() {
                    var newname = $.trim($("#re_name").val());
                    if(newname == oldName) {
                        d.close();
                        return;
                    };
                    //修改的文件名称
                    $(".man-filelist li.selected p").text(newname);
                    $.ajax({
                        url: newnameys + '?id=' + _id,
                        type: 'post',
                        dataType: "json",
                        data: get_selected_type()[0]=="direxe" ? {rename: newname,} : {filename:newname} ,
                        success: function(data) {
                            d.close().remove();
                            if(data.errorcode > 0) {
                                myalert("修改失败！");
                            }
                        },
                        error: function(e) {

                        }

                    })
                    return false;
                },
                cancelValue: '取消',
                cancel: function() {}
            }).showModal();

        })

        function getGroup(){
            var groupData;
            $.ajax({
                url:"http://work.supsite.net/resource/cate/fileajax",//接口地址
                type:'post',
                dataType:"json",
                async:false,//同步请求
                success:function(data){
                    groupData=data.data;
                },
                error:function(e){

                }

            })
            return  groupData;
        }


        //移动文件
        $node.find("#move").bind("click", function() {
            if(!$(this).hasClass('on')) return;
            var selected = $(".man-filelist li.selected");
            var ids = [];
            for(var b = 0; b < selected.length; b++) {
                ids[b] = selected.eq(b).attr("data-id");
            }
            var $groupData=getGroup();//获取现有分组

            var groupLi = '';
            for(var p = 0; p < $groupData.length; p++) {
                groupLi += '<li data-id="' + $groupData[p]['_id'] + '">' + $groupData[p]['catename'] + '</li>';
            }

            var d = dialog({
                title: '移动分组',
                content: '<div id="group-list" class="move-list"><div class="title">全部分组</div><div class="content"><ul id="titlefile">' + groupLi + '</ul></div></div>',
                skin: 'myalert rename create move',
                okValue: '保存',
                ok: function() {

                    var targetId = $('#group-list li.on').attr('data-id');
                    if(!targetId) {
                        return false;
                    };
                    var res = moveFile(targetId, ids);

                    d.close();
                    if(res.errorcode == 0) {
                        $(".man-breadcrumb label i").removeClass('all');
                        var c = dialog({
                            skin: "mymessage",
                            content: '√ 移动成功'
                        });
                        c.show();
                        setTimeout(function() {
                            c.close().remove();
                        }, 2000);
                        selected.remove();
                        selectState();
                    }
                    return false;
                },
                cancelValue: '取消',
                cancel: function() {}
            }).showModal();
        })

        //删除文件或文件夹
        $node.find("#delete").bind("click", function() {
            var deltclose = $('#delete').attr('data-href');
            if(!$(this).hasClass('on')) return;
            var selected = $(".man-filelist li.selected");
            var ids = [];
            var file_type=null;
            for(var b = 0; b < selected.length; b++) {
                ids[b] = selected.eq(b).attr("data-id");
            }
            console.log(ids);
            //确认框
            var d = dialog({
                title: '删除提示',
                content: '将删除当前所选分组，是否继续。<br>当前所选分类中的文档将   变为无分组状态',
                okValue: '确定',
                skin: 'myalert',
                ok: function() {
                    $.ajax({
                        url: deltclose, //接口地址
                        type: 'post',
                        dataType: "json",
                        data:
                            get_selected_type()[0]=="direxe" ? { catearr: ids,} : {ids:ids},
                        success: function(data) {
                            d.close().remove();
                            if(data.errorcode == 0) {
                                $(".man-breadcrumb label i").removeClass('all');
                                var c = dialog({
                                    skin: "mymessage",
                                    content: '√ 删除成功'
                                });
                                c.show();
                                setTimeout(function() {
                                    c.close().remove();
                                }, 2000);
                                selected.remove();
                                selectState();

                            }
                        },
                        error: function(e) {

                        }

                    })
                    return false;
                },
                cancelValue: '取消',
                cancel: function() {}
            }).showModal();
        })

        //编辑图片
        $node.find("#edit").bind('click', function() {
            if(!$(this).hasClass('on')) {
                return
            };
            var imgUrl = $('.img.selected').find('img').attr('src');
            //新建分组
            var b = dialog({
                title: '编辑图片',
                content: '<div id="meitu"></div>',
                skin: 'myalert rename create meitu',
                okValue: false,
                cancelValue: false,
            });
            b.showModal();
            //美图秀秀
            var meitu = new meituxiuxiu(); //实例化美图秀秀
            meitu.Initialization('meitu', 1, '100%', '100%', imgUrl) //初始化美图秀秀
            meitu.setUploadURL(meituUploadUrl, 2, 'upload_file'); //上传参数设置
            meitu.setUploadArgs({
                name: '隔壁老王'
            }); //附加上传参数
            meitu.uploadResponse(function(data) { //上传回调
                console.log(data);
            })

        })

        /**绑定拖放事件   开始*****/
        var filelist = $('man-filelist')[0];
        var li = $('.man-filelist li');
        for(var i = 0; i < li.length; i++) {
            if(li[i].getAttribute('class').indexOf('dir') != -1) {
                li[i].addEventListener('dragover', dragmouse, false);
                li[i].addEventListener('dragleave', dragmouse, false);
                li[i].addEventListener('drop', drop, false);
                continue;
            }
            li[i].addEventListener('dragstart', bindDrag, false);
            li[i].addEventListener('dragend', bindDrag, false);

        }
        /**绑定拖放事件   结束*****/

        var dragObj; //当前拖动对象
        var targetObj; //目标对象

        /**动态添加的元素使用此种方式绑定   开始*****/
        //开始拖动
        //	$('.man-filelist').delegate('.css,.html,.img,.doc,.js,.pdf,.php,.ppt,.xls','dragstart',function(event){
        //		bindDrag(event);
        //	})
        //	//拖动放开
        //	$('.man-filelist').delegate('.css,.html,.img,.doc,.js,.pdf,.php,.ppt,.xls','dragend',function(event){
        //		bindDrag(event);
        //	})
        //	//绑定拖放对象dragover移上
        //	$('.man-filelist').delegate('.dir','dragover',function(event){
        //		dragmouse(event);
        //	})
        //	//绑定拖放对象dragleave移开
        //	$('.man-filelist').delegate('.dir','dragleave',function(event){
        //		dragmouse(event);
        //	})
        //
        //	//松开
        //	$('.man-filelist').delegate('.dir','drop',function(event){
        //		dragend(event);
        //	})
        //
        /**动态添加的元素使用此种方式绑定   结束*****/

        //绑定移动分组li点击事件
        $('body').delegate('#group-list li', 'click', function() {
            $(this).addClass('on').siblings().removeClass('on');
        })

        //绑定复制
        /* var clipboard = new Clipboard('.copy');
         //复制成功
         clipboard.on('success', function(e) {
         var d = dialog({
         skin:"mymessage",
         content: '√ 复制成功'
         });
         d.show();
         setTimeout(function() {
         d.close().remove();
         }, 2000);
         });
         //复制失败
         clipboard.on('error', function(e) {
         var d = dialog({
         skin:'mymessage err',
         content: '× 浏览器不支持'
         });
         d.show();
         setTimeout(function() {
         d.close().remove();
         }, 2000);
         });   */

        //开始拖放，取消拖放
        function bindDrag(event) {
            dragObj = $(event.target);
            //开始拖放
            if(event.type == 'dragstart') {
                event.dataTransfer.effectAllowed = "copy";
                event.dataTransfer.setData("text", $(event.target).attr('data-id'));
                dragObj = $(event.target);
                $(event.target).addClass('dragstart');
            }
            //松开拖放
            else {
                dragObj = null;
                $(event.target).removeClass('dragstart');
            };
            return false;
        }
        //移动到目标和离开目标
        function dragmouse(event) {
            //移动到目标
            if(event.type == 'dragover') {
                event.preventDefault();
                var targetId = $(event.target).attr('data-id'); //目标ID
                $(event.target).addClass('dragover');
            }
            //离开目标
            else {
                $(event.target).removeClass('dragover');
            };
        }

        //拖放松开
        function drop(event) {
            var dragID = event.dataTransfer.getData("text"); //文件ID
            var targetID = $(event.target).attr('data-id'); //目标文件夹ID
            if(targetID == undefined || targetID == undefined) return;
            var targetText = $(event.target).find('p').text(); //目标文件夹名称
            $(event.target).removeClass('dragover');
            $res = moveFile(targetID, [dragID]);
            //移动成功
            if($res) {
                //提示
                var d = dialog({
                    skin: "mymessage",
                    content: '已成功移动文件到‘' + targetText + '’',
                });
                d.show();
                setTimeout(function() {
                    d.close().remove();
                }, 2000);
                dragObj.remove();
                selectState();
            }
            //失败
            else {

            }

        }

        /**
         * 移动文件到文件夹
         * @param {Object} targetID  文件夹ID
         * @param {Object} dragID  文件ID 数组形式[1,2,3]
         */
        function moveFile(targetID,dragID){
            var data={
                "cateid": targetID,//目标ID
                "ids":dragID//移动的文件
            }
            var result;
            $.ajax({
                url:$('#move').attr('data-href'),//接口地址
                type:'post',
                dataType:"json",
                async:false,//同步请求
                data:{
                    "cateid": targetID,//目标ID
                    "ids":dragID//移动的文件
                },
                success:function(data){
                    result=data;
                },
                error:function(e){

                }

            })
            return result;

        }

        //操作按钮状态规则
        function selectState() {
            var selectEDlen = $(".man-filelist li.selected").length; //选择中文件/文件夹的个数
            $('.selectCount').text(selectEDlen); //复制已选择数量
            var dirLen = $(".man-filelist li.dir.selected").length;
            var imgLen = $(".man-filelist li.img.selected").length;
            if(selectEDlen > 0) {
                $('#rename,#delete,#move').addClass('on');
            } else {
                $('#rename,#delete,#move').removeClass('on');
            }
            if(dirLen > 0) {
                $('#move').removeClass('on')
            }
            if(selectEDlen > 1) {
                $('#rename').removeClass('on')
            }
            if(imgLen == 1) {
                $('#edit').addClass('on')
            } else {
                $('#edit').removeClass('on')
            }

        }

        /**
         * 美臀秀秀图片处理
         * @param {Object} $id  绑定的domID
         * @param {Object} $imgUrl 处理图片的URL
         * @param {Object} $uploadServe 上传服务地址
         */
        function meituxiuxiu() {
            //初始化美图，id编辑器容器，imgURl要编辑的图片路径，绝对路径包括http://
            //$id 		参数是加载编辑器div容器，
            //$type 	参数是编辑器类型，
            //$width	参数是div容器宽，
            //$height	参数是div容器高,
            //$imgUrl	要编辑的图片
            this.Initialization = function($id, $type, $width, $height, $imgUrl) {
                xiuxiu.embedSWF($id, $type, $width, $height);
                xiuxiu.onInit = function() {
                    xiuxiu.loadPhoto($imgUrl);
                }
                this.close();
            }
            //设置上传图片接口
            /**
             * $uploadUrl   上传图片的URL
             * $type		上传方式类型，1、流式上传，2、标准表单上传，3、为编码成Base64传给JS
             * $formName	表单文件域的名称
             */
            this.setUploadURL = function($uploadUrl, $type, $formName) {
                xiuxiu.setUploadURL($uploadUrl);
                xiuxiu.setUploadType($type);
                xiuxiu.setUploadDataFieldName($formName);
            }

            //设置上传参数
            //$Args	对象形式{name:'隔壁老王'}
            this.setUploadArgs = function($Args) {
                xiuxiu.setUploadArgs($Args);
            }
            //上传回调
            this.uploadResponse = function($callback) {
                xiuxiu.onUploadResponse = function(data) {
                    $callback(data);
                }
            }
            //关闭美图秀秀
            this.close = function() {
                xiuxiu.onClose = function() {
                    //确认框
                    var c = dialog({
                        title: '温馨提示！',
                        content: '您需要取消本次图片编辑吗？',
                        okValue: '确定',
                        skin: 'myalert',
                        ok: function() {
                            b.remove();
                        },
                        cancelValue: '取消',
                        cancel: function() {}
                    });
                    c.showModal();
                }
            }
        }

        //   以下为文件上传

        var uploadUrl = 'http://v0.api.upyun.com/fivestarweb'; //又拍云API-URL
        var autographUrl = 'http://www.supsite.net/upload/set?'; //获取签名URl
        var fieupurl = $('.js-fileup').attr('data-href');  // 获取上传url
        var fikeves = $('.js-fileup').attr('data-siteid');  //获取上传秘钥siteid
        $(function() {
            //自适应居中
            autoPosition();
            $(window).resize(function() {
                autoPosition();
            })
        })

        /**
         * 自适应居中
         */
        function autoPosition() {
            //自适应居中
            var windowWidth = $(window).width();
            var windowHeight = $(window).height();
            var left = windowWidth / 2 - ($('.upload-content').width() / 2);
            var top = windowHeight / 2 - ($('.upload-content').height() / 2) - 100;
            $('.upload-content').css({
                left: left + 'px',
                top: top + 'px'
            });
        }

        /**
         * 打开上传界面
         * @param string   mime 上传文件类型  "jpg,png,gif"
         * @param function sucCallback  成功信息回调函数
         * @param function errCallback  失败信息回调函数
         */
        function openFileUpload(mime, sucCallback, errCallback) {
            if(!mime) {
                myalert('请声明上传文件类型');
                return;
            }
            var typeHtml = '';
            if(mime.indexOf('jpg') != -1 || mime.indexOf('png') != -1 || mime.indexOf('bmp') != -1 || mime.indexOf('gif') != -1) {
                typeHtml = '<p>将图片拖拽到该区域或<span>点击上传</span></p><p>支持单张20M以内的图片上传</p>';
            } else if(mime.indexOf('pdf') != -1 || mime.indexOf('xlsx') != -1 || mime.indexOf('xls') != -1 || mime.indexOf('ppt') != -1 || mime.indexOf('doc') != -1 || mime.indexOf('docx') != -1) {
                typeHtml = '<p>将文档拖拽到该区域或<span>点击上传</span></p><p>支持单个20M以内的文档上传</p>';
            } else {
                typeHtml = '<p>将文件拖拽到该区域或<span>点击上传</span></p><p>支持单个20M以内的文件上传</p>';
            }

            var fileUploadHtml = '<div id="upload-file"><div class="upload-mask"></div><div class="upload-content"><div class="head">上传<span class="progressBox"><i class="progressCount">0</i>/<i class="fileCount">0</i></span><div title="关闭" class="close"></div></div><div class="file-list scrollbar"><div class="filedomain">' + typeHtml + '<input type="file" name="file" id="file" value="" multiple /></div></div></div></div>';
            $('body').append(fileUploadHtml);
            autoPosition();
            coreUpload(mime, sucCallback, errCallback);
        }

        /**
         * 验证文件大小和文件个数
         * @param {Object} that upload当前对象
         * @param {Object} data files
         * @param {Object} mime 允许上传的文件类型
         */
        var oldFileList = [];//文件原名数组
        function initcheck(that, data, mime) {

            //引入
            //定义限制参数
            var maxFilesize = 20 * 1024 * 1024; //单个文件最大数
            var maxFilesCount = 20; //允许上传最大文件数

            //定义全局化参数
            that['Authorization'] = []; //鉴权认证数组
            that['isSubmit'] = true; //是否发送上传
            that['listItems'] = []; //上传集合
            that['listItemIndex'] = 0; //当前上传索引
            that['listItemFailCount'] = 0; //失败总数
            that['itemCount'] = data.files.length; //选择的文件总数

            //判断文件最大限制
            if(data.files.length > maxFilesCount) {
                myalert('单次上传只允许20个,请重新选择!');
                that['isSubmit'] = false;
                return;
            }


            //单个判断文件大小 or 类型
            var fileTypeGroup = "";
            for(var i = 0; i < data.files.length; i++) {
                var type = data.files[i].name.substr(data.files[i].name.lastIndexOf('.') + 1);
                fileTypeGroup += type + "|";
                oldFileList.push({filename:data.files[i].name});
                if(mime.indexOf(type) == -1) {
                    myalert('选择文件类型有误,请重新选择!<br>仅支持 ' + mime + ' 格式');
                    that['isSubmit'] = false;
                    return;
                }
                if(data.files[i].size > maxFilesize) {
                    myalert('单个文件最大限制20M,请重新选择!');
                    that['isSubmit'] = false;
                    return;
                };

            }
            fileTypeGroup = fileTypeGroup.substr(0, fileTypeGroup.length - 1);

            //上传总文件数
            $('#upload-file .fileCount').text(that['itemCount']);
            console.log(fileTypeGroup);
            //判断全部上传文件是否符合上传要求，再向服务器发起生成签名请求
            if(that['isSubmit']) {
                //获取鉴权签名
                getAutograph(fileTypeGroup);
            }

        }

        /**
         * 核心上传函数
         * @param {Object} mime 允许上传的文件类型
         * @param function sucCallback 返回成功的资源
         * @param function errCallback 返回失败信息
         * include 'jquery.min.js'
         * include 'jquery.ui.widget.js'
         * include 'jquery.iframe-transport.js'
         * include 'jquery.fileupload.js'
         * 必须引入这四个文件
         */
        var $dataArr = [];
        var $Authorization = [];

        function coreUpload(mime, sucCallback, errCallback) {
            $dataArr = [];
            $Authorization = [];
            $AuthorizationIndex = 0; //
            var resources = []; //服务器返回成功数据 array
            var errInfo = []; //返回失败信息 array
            //判断浏览器是否是10以下
            if(navigator.appName == "Microsoft Internet Explorer" && navigator.appVersion.match(/MSIE\s(\d+\.?\d+)/i)[1] < 10) {
                $('#upload-file .filedomain p:first').html('<span>点击上传</span>');
            }

            //初始化化上传控件
            $('#file').fileupload({
                url: uploadUrl,
                type: 'POST',
                dataType: 'json',
                dropZone: $('.filedomain'),
                autoUpload: true,
                sequentialUploads: true,
                real_file_name: null,
                //提交的POST数据
                submit: function(e, data) {
                    console.log("sumbit~~~");
                    console.log(data);
                    if(data.files.length == 1)
                        this.real_file_name = data.files[0].name;

                    data.formData = $Authorization['data'][$AuthorizationIndex];
                    $AuthorizationIndex++;
                    if($Authorization['data'].length <= 0) {
                        return false;
                    }
                },
                //单文件执行完成
                done: function(e, data) {
                    console.log("single upload success!");
                    console.log(e);
                    console.log(data);
                    var item = this.listItems[this.listItemIndex];
                    //上传失败
                    //if(data.result.code==200){
                    //console.log(data.result);
                    data.result.real_file_name = this.real_file_name;
                    resources.push(data.result);
                    item.find('.progressBar').css('width', '100%');
                    item.find('.progressNumber').addClass('success').text('成功');
                    setTimeout(function() {
                        item.fadeOut(1000, function() {
                            item.remove();
                        });
                    }, 2000);

                    //};
                    this.listItemIndex++;
                    $('#upload-file .progressCount').text(this.listItemIndex);
                },

                //单文件上传失败
                fail: function(e, data) {
                    var res = JSON.parse(data.jqXHR.responseText);
                    var item = this.listItems[this.listItemIndex];
                    errInfo.push(res);
                    this.listItemFailCount++; //记录错误条数
                    item.find('.progressNumber,.progressBar').addClass('fail');
                    item.find('.progressNumber').text('失败');
                    this.listItemIndex++;
                    $('#upload-file .progressCount').text(this.listItemIndex);
                },
                //添加文件队列，添加一个执行一次
                add: function(e, data) {
                    //是否执行上传
                    if(!this.isSubmit) {
                        return false;
                    }
                    var file = data.files[0];
                    $dataArr.push(data);
                    var fileName = data.files[0].name;
                    var fileSize = data.files[0].size;
                    var fileType = data.files[0].name.substr(data.files[0].name.lastIndexOf('.') + 1);
                    var imgUrl = '';
                    var item = $('<div class="item"><i class="thumbnail"><img src="' + imgUrl + '" alt=""></i><div class="title">' + fileName + '<span class="progressBar"></span></div><span class="progressNumber">等待</span></div>');
                    $('#upload-file .file-list').append(item);

                    //获取缩略图
                    var ImgtypeArr = 'jpg,png,gif,bmp';
                    if(window.FileReader && ImgtypeArr.indexOf(fileType) != -1) {
                        var reader = new FileReader();
                        reader.readAsDataURL(file);
                        reader.onloadend = function(e) {
                            imgUrl = e.target.result;
                            item.find('.thumbnail img').attr('src', imgUrl)
                        }
                    }
                    //类型
                    switch(fileType) {
                        case 'pdf':
                            imgUrl = '//static.gcimg.net/i/201704/n64JJGu3zy.png';
                            break;
                        case 'docx':
                            imgUrl = '//static.gcimg.net/i/201704/dgfWrNy5zS.png';
                            break;
                        case 'ppts':
                            imgUrl = '//static.gcimg.net/i/201704/nQ01clXhTJ.png';
                            break;
                        case 'pptx':
                            imgUrl = '//static.gcimg.net/i/201704/nQ01clXhTJ.png';
                            break;
                        case 'xlsx':
                            imgUrl = '//static.gcimg.net/i/201704/vcYgqrMu7c.png';
                            break;
                        case 'xls':
                            imgUrl = '//static.gcimg.net/i/201704/vcYgqrMu7c.png';
                            break;
                        case 'ppt':
                            imgUrl = '//static.gcimg.net/i/201704/nQ01clXhTJ.png';
                            break;
                        case 'doc':
                            imgUrl = '//static.gcimg.net/i/201704/dgfWrNy5zS.png';
                            break;
                        case 'rar':
                            imgUrl = '//static.gcimg.net/i/201704/QdfiS0h9Iz.png';
                            break;
                        case 'css':
                            imgUrl = '//static.gcimg.net/i/201704/k409lOo5NJ.png';
                            break;
                        case 'js':
                            imgUrl = '//static.gcimg.net/i/201704/nvKK8QZBdA.png';
                            break;
                        default:
                            imgUrl = 'images/picture.png';
                    }
                    item.find('.thumbnail img').attr('src', imgUrl);
                    this.listItems.push(item);
                    $("#upload-file .filedomain").hide();
                    $('#upload-file .head .progressBox').show();
                },

                //change触发
                change: function(e, data) {
                    initcheck(this, data, mime);
                },

                //拖放触发
                drop: function(e, data) {
                    initcheck(this, data, mime);
                },
                dragover: function(e) {
                    e.preventDefault();
                },

                //开始上传执行
                start: function(e) {
                    $(this).attr("disabled", "disabled");
                },

                //队列完成执行
                always: function(e, data) {
                    $(this).removeAttr("disabled");
                },

                //队形完成停止，全部完成2秒后关闭上传窗口
                stop: function(e, data) {
                    sucCallback(resources);
                    if(errCallback) {
                        errCallback(errInfo);
                    }
                    if(this.listItemFailCount == 0) {
                        setTimeout(function() {
                            $('#upload-file').remove();
                        }, 2000)
                    };
                },

                //进度条
                progress: function(e, data) {
                    var progress = parseInt(data.loaded / data.total * 100, 10);
                    var item = this.listItems[this.listItemIndex];
                    item.find('.progressNumber').text(progress + '%');
                    item.find('.progressBar').css({
                        width: progress + '%'
                    });
                }
            });

            //关闭组件
            $('#upload-file').delegate('.close', 'click', function() {
                $('#upload-file').remove();
            })

        }

        ///**
        // * 获取签名信息
        // * @param {string} $data //签名必须参数
        // */
        //function getAutograph($fileTypeGroup){
        //	$res=[];
        //	$.ajaxSettings.async=false;//同步请求
        //	$.getJSON(autographUrl+'?callback=?',{data:$fileTypeGroup},function(data){$res=data;
        //	console.log(res);})
        //	return $res;
        //}

        /**
         * 获取签名信息
         * @param {string} $data //签名必须参数
         */
        function getAutograph($fileTypeGroup) {
            $.ajax({
                url: autographUrl,
                type: 'GET',
                dataType: 'jsonp',
                jsonp: 'callback',
                data: {
                    types: $fileTypeGroup,
                    siteid: 'dsakfjlkasdjfnhrgbaksjdfk'
                },
                async: false, //同步请求
                jsonpCallback: "successCallback",
                success: function(res) {
                    $Authorization = res;
                    if(res.errorcode > 0) {
                        $('#upload-file').remove();
                        myalert('鉴权错误！');
                        return;
                    }
                    for($i = 0; $i < $dataArr.length; $i++) {
                        $dataArr[$i].submit();
                    }
                },
                error: function(err) {
                    $('#upload-file').remove();
                    myalert('获取签名失败！');
                }
            });
        }

        /**
         * 把数据推回服务器
         * @saveServerUrl $saveServerUrl
         * @param {Object} $data
         * @callback       $callback
         */
        function saveServer($saveServerUrl, $data, $callback) {
            var juteid = $("#supperts").attr('data-cateid');
            $fileArr = [];
            for(var c = 0; c < $data.length; c++) {
                $name = $data[c]['url'].substr($data[c]['url'].lastIndexOf('/') + 1);
                $url = $data[c]['url'];
                $size = $data[c]["file_size"];
                $fileArr.push({
                    filename: oldFileList[c].filename,
                    url: $url,
                    size: $size
                });
            }
            if($data.length < 1) {
                return;
            }
            $.ajax({
                url: $saveServerUrl,
                type: 'POST',
                dataType: 'json',
                //  jsonp:'callback',
                //  jsonpCallback:"successCallback",
                data: {
                    data: $fileArr,
                    cateid: juteid
                },
                //async:false,//同步请求
                success: function(res) {
                    $callback(res);
                },
                error: function(err) {
                    myalert('推送到服务器失败！');
                }
            })
        }

        //  调用上传窗口

        myAlertAutoPosition();

        //上传图片
        //异步获取列表,如果要不同uri获取不同页面的数据，可以把此方法放在每个页面的页脚
        /*getListData('localhost',{uid:222},function(data){
         $(".man-filelist").append(DataSorting(data.data));
         });*/

        $node.find('#uploadImg').bind('click', function() {
            var imgfileurl = $('#uploadImg').attr('data-href');
            var accImgType = 'jpg,png,bmp,gif'; //图片类型
            openFileUpload(accImgType,function(data){
                //传回服务器
                saveServer(imgfileurl,data,function(res){
                    $(".man-filelist").append(DataSorting(res.data));
                });

            },function(errInfo){
                //上传失败的文件错误信息
                console.log(errInfo);
            })
        })

        // 文档上传
        $node.find('#supperts').click(function() {
            var accWordType = 'pdf,xlsx,xls,ppt,doc,docx,ppts,zip,pptx'; //文档类型
            openFileUpload(accWordType, function(data) {
                //传回服务器
                saveServer(fieupurl, data, function(res) {
                    // $("#resexe li").remove();
                    $("#resexe").prepend(DataSorting(res.data));
                });

            }, function(errInfo) {
                //上传失败的文件错误信息
                console.log(errInfo);
            });
        })

        /**
         * 异步获取列表数据
         * @param {Object} Url 服务器连接
         * @param {Object} obj 附加参数
         */
        function getListData(Url, obj, callback) {
            $.ajax({
                url: 'work.supsite.net/resource/index/addgetlist',
                type: 'post',
                dataType: 'json',
                data: {
                    data: obj
                },
                success: function(res) {
                    callback(res);
                },
                error: function(err) {
                    alert('获取数据失败！');
                }
            })

        }

        /**解析数组转义html**/
        /**解析数组转义html**/
        function DataSorting($arr){
            if($arr.length<=0){return;}
            var Html="";
            for(var i=0; i<$arr.length; i++){
                var type=$arr[i].filename.substr($arr[i].filename.lastIndexOf('.')+1);
                var img='';
                var cls="dir";
                var title=$arr[i].filename;
                var cateid=$arr[i].cateid;
                var imgUrl=$arr[i]['url'];
                var addtime=$arr[i]['addtime']
                //类型
                switch(type){
                    case 'pdf' :
                        cls="pdf";
                        break;
                    case 'xlsx' :
                        cls="xls";
                        break;
                    case 'xls' :
                        cls="xls";
                        break;
                    case 'ppt' :
                        cls="ppt";
                        break;
                    case 'pptx' :
                        cls="pptx";
                        break;
                    case 'doc' :
                        cls="doc";
                        break;
                    case 'docx' :
                        cls="doc";
                        break;
                    case 'js' :
                        cls="js";
                        break;
                    case 'css' :
                        cls="css";
                        break;
                    case 'html' :
                        cls="html";
                        break;
                    case 'php' :
                        cls="php";
                        break;
                    default:
                        cls="img";
                }
                if($arr[i]['uptype']==1){
                    img='< img draggable="false" src="'+imgUrl+'" alt="" />';
                }
                var tmp='<li data-time="'+addtime+'" class="'+cls+'" draggable="true" data-id="'+cateid+'"><i></i>'+img+'<p>'+title+'</p ></li>';
                Html+=tmp;
            }


            return $(Html);

        }
        //文档CSS
        $node.find('#').bind('click', function() {
            openFileUpload(accCssType,
                function(data) {
                    console.log(data);
                },
                function(errInfo) {
                    console.log(errInfo);
                }
            );
        })

        //文档js
        $('#').bind('click', function() {
            openFileUpload(accJsType,
                function(data) {
                    console.log(data);
                },
                function(errInfo) {
                    console.log(errInfo);
                }
            );
        })

        //myalert
        function myalert(content) {
            myAlertAutoPosition();
            var myalert = '<div id="myalert"><div class="mask"></div><div class="content"><div class="head">错误信息！<i class="close">X</i></div><p>' + content + '</p></div></div>';
            $('body').append(myalert);
            myAlertAutoPosition();
            $(window).resize(function() {
                autoPosition();
            })
            $('#myalert').delegate('.close,.mask', 'click', function() {
                $('#myalert').remove();
            })

        }
        /**
         * mylaert自适应居中
         */
        function myAlertAutoPosition() {
            //自适应居中
            var windowWidth = $(window).width();
            var windowHeight = $(window).height();
            var left = windowWidth / 2 - ($('#myalert .content').width() / 2);
            var top = windowHeight / 2 - ($('#myalert .content').height() / 2) - 100;
            $('#myalert .content').css({
                left: left + 'px',
                top: top + 'px'
            });
        }

    }
}