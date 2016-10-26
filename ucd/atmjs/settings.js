var settings = {
    name: 'bx',                 // 站点名称(字母+数字+下划线组成,必须以字母开头)
    libName: 'lib',               // 开放项目的名称
    styleTimeout: 0,                        // 样式延迟多少毫秒后返回,主要用于调试
    targets: {                              // 目标配置
        dev: {                              // dev目标的配置
            color: 'green',                 // GUI中目标操作按钮的颜色,参考semantic-ui中的按钮颜色的class
            operates: {                     // dev目标可用的操作,指定项必须在settings.operates中存在
                build: 1
            },
            compress: {
                js: false,                  // js文件不压缩
                css: false,                 // css文件不压缩
                png: false                  // png文件不压缩
            }
        },
        product: {                             // test目标的配置
            // 构建后的文件的根路径,可用占位符{{site}}(站点目录)和{{homedir}}(用户目录)
            assets: '{{site}}/../trunk/bx/static/atm',

            // 产出的清单文件的根路径,可用占位符{{site}}(开发目录,即站点目录)和{{target}}(构建目标)
            manifests: '{{site}}/../trunk/bx/manifests',

            // 产出的地图文件的根路径,可用占位符{{site}}(开发目录,即站点目录)和{{homedir}}(用户目录)和{{target}}(构建目标)
            maps: '{{site}}/../trunk/bx/maps',

            // 静态文件根目录对应的http[s]路径
            domain: '/static/atm',

            color: 'red',                 // GUI中目标操作按钮的颜色,参考semantic-ui中的按钮颜色的class
            operates: {                     // test目标可用的操作,指定项必须在settings.operates中存在
                build: 1,                   // 构建
                map: 1,                     // 地图
                build_map: 1
            },
            hash: true,                     // 构建后的文件名是否带7位的md5后缀
            compress: {
                js: true,                   // 构建后的js文件是否进行压缩
                css: true,                  // 构建后的css文件是否进行压缩
                png: true                   // png文件是否进行压缩
            }

        }
    }
};
module.exports = settings;
