var define = null;
var atmjs;
(function (util, win, undefined) {
    var args = {};
    var initialized;
    var defines = {};
    var modules = {};
    var process = {};
    atmjs = {
        loadCss: util.loadCss,
        loadJs: util.loadJs,
        addCss: util.addCss,
        _loadJs: util._loadJs,
        _loadCss: util._loadCss,
        init: function (cfg) {
            if (initialized) {
                return atmjs;
            }
            initialized = true;
            args = util.transformArgs(cfg);
        },
        use: function (ids, callback){
            ids = util.getIds(ids);
            ids = (function () {
                var arr = [];
                for (var i in ids) {
                    arr.push(util.completeId(ids[i], args));
                }
                return arr;
            })();

            require.async(ids, callback);
        }
    };

    define = function (id, deps, factory) {
        defines[id] = {
            id: id,
            deps: deps,
            factory: factory
        };

        for(var key in process) {
            // 如果该id在待处理列表里面
            if (process[key].has[id]) {
                // 如果该模块的依赖都准备完毕
                setStatus(id, key);
                tryApplyProcess(key);

            }
        }
    };
    function require (id) {
        if (modules[id]) {
            return modules[id].exports;
        }
        var module = {
            exports: {}
        };
        modules[id] = module;

        var factory = defines[id].factory || function() {};
        var ret = factory.apply(win, [require, module.exports, module]);
        if (ret !== undefined) {
            module.exports = ret;
        }
        return module.exports;
    }

    require.async = function(ids, callback) {
        if (typeof callback !== 'function') {
            callback = function () {};
        }

        // 把ids转换成数组
        ids = util.getIds(ids);
        var key = ids.join(',');

        // 判断依赖的模块是否全部都defines过
        if (!process[key]) {
            process[key] = {
                ids: ids,
                has: {},
                callbacks: [callback]
            };
        } else {
            process[key].callbacks.push(callback);
        }

        for(var i in ids) {
            setStatus(ids[i], key);
        }
        tryApplyProcess(key);
        // 如果模块都准备完毕,则执行process


    };

    function tryApplyProcess(key) {
        if (getStatus(key)) {
            var data = process[key];
            var ids = data.ids;
            var arr = [];
            for(var i in ids) {
                arr.push(require(ids[i]));
            }
            var callbacks = data.callbacks;
            for(var j in callbacks) {
                callbacks[j].apply(win, arr);
            }
            delete process[key];
        }


    }

    function getStatus(key) {

        var has = process[key].has;
        var status = true;
        for(var i in has) {
            if (has[i] < 20) {
                status = false;
                break;
            }
        }
        return status;
    }

    // 获取模块及模块的依赖及依赖的依赖是否加载完成
    function setStatus(id, key) {
        var data = process[key];
        var has = data.has;

        if (defines[id]) {
            // 如果已经被执行过,则直接返回true
            if (modules[id]) {
                has[id] = 40;
            } else {
                has[id] = 20;
                var deps = defines[id].deps;
                for(var i in deps) {
                    var depId = deps[i];
                    if (!has[depId]) {
                        setStatus(depId, key);
                    }
                }
            }
        } else {

            has[id] = 10;
            util.loadModule(id, 1, args);
        }


    }

    define.atm = {};

})((function() {
    var caches = {
        style: {},                  // 加载过样式的模块id
        js: {},                     // 加载过的js
        css: {}                     // 加载过的css
    };

    var RE_NON_WORD = /\W/g;
    var doc = document;
    var head = document.getElementsByTagName("head")[0] || document.documentElement;
    var styleNode;
    // 获取第一个script标签
    var util = {
        // 加载css文件
        loadCss: function (href) {
            var link = document.createElement('link');
            link.href = href;
            link.rel = 'stylesheet';
            link.type = 'text/css';

            head.appendChild(link);
            return this;
        },

        // 加载js文件
        loadJs: function (url) {
            var script = document.createElement('script');
            script.type = 'text/javascript';
            script.src = url;
            head.appendChild(script);
            return this;
        },

        // 插入style标签样式
        addCss: function (styleText, id) {
            if (id) {
                // Convert id to valid string
                id = id.replace(RE_NON_WORD, "-");
                // Don't add multiple times
                if (doc.getElementById(id)) {
                    return;
                }
            }

            var element;
            // Don't share styleNode when id is spectied
            if (!styleNode || id) {
                element = doc.createElement("style");
                id && (element.id = id);
                // Adds to DOM first to avoid the css hack invalid
                head.appendChild(element);
            } else {
                element = styleNode;
            }
            // IE
            if (element.styleSheet) {
                // http://support.microsoft.com/kb/262161
                if (doc.getElementsByTagName("style").length > 31) {
                    throw new Error("Exceed the maximal count of style tags in IE");
                }
                element.styleSheet.cssText += styleText;
            } else {
                element.appendChild(doc.createTextNode(styleText));
            }
            if (!id) {
                styleNode = element;
            }
        },
        // 把页面里面atmjs.use里面的参数进行转换
        transformArgs: function (args) {
            args = args || {};
            var async = args.async || {};
            var idArr = async.id || [];
            var uriArr = async.uri || [];
            var typeArr = async.type || [];
            var uris = async.uris || {};
            var deps = async.deps || {};

            var newUris = {};
            var newDeps = {};

            var debugDomain = args.debugDomain;
            if (debugDomain === undefined) {
                var domain = args.domain;
                for(var id in uris) {
                    var uri = uriArr[uris[id]];
                    if (uri.indexOf(domain) === 0) {
                        newUris[idArr[id]] = uri;
                    } else {
                        newUris[idArr[id]] = domain + uri;
                    }
                }
            } else {
                var domain = args.domain;
                for(var id in uris) {
                    var uri = uriArr[uris[id]];
                    if (uri.indexOf(domain) === 0) {
                        uri = uri.replace(domain, debugDomain);
                        newUris[idArr[id]] = uri;
                    } else{
                        newUris[idArr[id]] = debugDomain + uri;
                    }

                }
            }


            for(var i in deps) {
                var arr = [];
                var obj = deps[i];
                for(var j in obj) {
                    var index = obj[j];
                    var id = idArr[index];
                    var type = typeArr[index];
                    var url = newUris[id];
                    arr.push({
                        id: id,
                        type: type,
                        uri: url
                    });
                }
                newDeps[idArr[i]] = arr;
            }
            var newArgs = args;
            newArgs.async = {
                uris: newUris,
                deps: newDeps
            };
            return newArgs;
        },

        // 如果传入的是字符串,则转换成数组
        getIds:function (ids) {
            return typeof ids === 'string'? [ids]: ids;
        },

        // 如果是空对象或对象的所有键的键值都为空类型,则返回true;其他都返回false
        isEmpty: function (obj) {
            var status = true;
            for(var i in obj) {
                if (obj[i]) {
                    status = false;
                }
            }
            return status;
        },

        // 补全id
        completeId: function (id, args) {
            if (id.indexOf(':') > -1) {
                var arr = id.split(':');
                var namespace = arr[0];
                var idpath = arr[1];
                arr = namespace.split('/');
                if (arr.length === 2) {
                    return [arr[0], arr[1], args.version || ''].join('/') + ':' + idpath;
                } else {
                    return id;
                }
            } else {
                var alias = args.alias || {};
                var aliasId = alias[id];
                return aliasId ? aliasId : id;
            }
        },
        _loadJs: function (url, debugDomain) {
            if (!url || caches.js[url]) {
                return;
            }
            caches.js[url] = true;
            if (debugDomain !== undefined) {
                url = url + '?debugDomain=' + debugDomain;
            }
            util.loadJs(url);
        },
        _loadCss: function (href, debugDomain) {
            if (!href || caches.css[href]) {
                return;
            }
            caches.css[href] = true;
            if (debugDomain !== undefined) {
                href = href + '?debugDomain=' + debugDomain
            }
            util.loadCss(href);
        },

        // 加载模块依赖的css文件
        loadCssDeps: function (id, args) {
            var cssDeps = args.async.css;
            var uriArr = cssDeps[id];
            if (uriArr) {
                for (var i in uriArr) {
                    var uri = uriArr[i];
                    util._loadCss(uri, args.debugDomain);
                }
            }
        },
        loadModule: function (id, type, args) {         // 加载js或css模块及依赖的模块
            var style = caches.style;
            if (style[id]) {
                return;
            }
            style[id] = true;
            var async = args.async;
            var arr = async.deps[id];
            var uri = async.uris[id];
            if (arr) {
                for(var i in arr) {
                    var obj = arr[i];
                    var depId = obj.id;
                    if (obj.uri) {
                        util.loadModule(depId, obj.type, args);
                    }
                }
            }
            if (uri) {
                if (type) {
                    util._loadJs(uri, args.debugDomain);
                } else {
                    util._loadCss(uri, args.debugDomain);
                }
            }

        }

    };
    return util;
})(), window);