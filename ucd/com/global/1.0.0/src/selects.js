var $ = require('./dollar');
var Widget = require('com/arale:widget');
var Selects = Widget.extend({
    attrs: {
        defaults: [],
        selectName: 'select',
        selectNames: ['province', 'city']
    },
    events: {
        'change .atm-select': function (e) {
            var $select = $(e.target);
            var level = $select.data('level');
            this.initLevel(level);
        }
    },

    // 获取子数据的url
    // @param level: 当前所处的等级,获取一级分类数据时level为0,获取二级分类数据时level为1
    // @param value: 当前选中的
    getUrl: $.noop,

    getName: function (level) {
        var selectNames = this.get('selectNames') || [];
        var selectName = selectNames[level-1];
        if (typeof selectName === 'undefined') {
            selectName = this.get('selectName') + (level);
        }
        return selectName;
    },

    // 设置select的name
    addName: function (level) {
        var name = this.getName(level);
        this.getSelect(level).attr('name', name);
    },
    getAjaxUrl: function (level) {
        var that = this;
        var selectValue = that.getSelectValue(level);
        var url = that.getUrl(level, selectValue);
        if (!url) {
            return null;
        } else {
            return url;
        }
    },

    // 获取select的jQuery对象
    getSelect: function (level) {
        return this.element.find('.atm-select[data-level="' + level + '"]');
    },

    // 获取选中项的值
    getSelectValue: function (level) {
        var that = this;
        if (level === 0) {
            return '';
        } else {
            return this.getSelect(level).val();
        }
    },

    setValue: function (level, value) {
        this.element.find('.atm-select[data-level="' + level + '"]').val(value);
    },

    // 删除level以后的select
    removeAfter: function (level) {
        var that = this;
        // 删除后面的select
        that.element.find('.atm-select').each(function () {
            if ($(this).data('level') > level) {
                $(this).remove();
            }
        });
        return this;
    },

    getDefaultValue: function (level) {
        var defaults = this.get('defaults') || [];
        if (typeof(defaults[level]) === 'undefined') {
            return null;
        } else {
            // 删除默认值
            var defaultValue = defaults[level];
            delete defaults[level];
            return defaultValue;
        }
    },

    // 异步数据返回后的回调
    ajaxCallback: function (level, res) {
        var that = this;
        that.removeAfter(level - 1).createSelect(res, level);

        // 获取当前级的默认值
        var defaultValue = that.getDefaultValue(level - 1);

        // 如果该级有默认值
        if (defaultValue !== null) {

            // 设置默认值
            that.setValue(level, defaultValue);

            // 初始化下一级
            that.initLevel(level);
        }
    },

    // 对后台返回的数据进行处理
    convertData: function (level, data) {
        return data;
    },

    // 创建select标签
    createSelect: function (data, level) {
        var optionHtml = this.getOptionHtml(level, data);
        var html = '<select class="atm-select" data-level="' + level + '">' + optionHtml + '</select>';
        if (level === 1) {
            $(html).prependTo(this.element);
        } else {
            $(html).insertAfter('select[data-level="' + (level - 1)+ '"]')
        }
        this.addName(level);
    },

    // 获取option标签
    getOptionHtml: function (level, data) {
        data = this.convertData(level, data);
        var arr = [];
        for(var i = 0,len = data.length; i < len; i++) {
            var obj = data[i];
            arr.push('<option value="' + obj[0] + '">' + obj[1] + "</div>");
        }
        return arr.join('');
    },

    // 初始化
    initLevel: function (level) {
        var that = this;
        var ajaxUrl = that.getAjaxUrl(level);
        if (ajaxUrl !== null) {
            // 获取ajax数据
            $.getJSON(ajaxUrl, function (res) {
                that.ajaxCallback(level + 1, res);
            });
        } else {
            that.removeAfter(level);
        }
    },

    setup: function () {
        this.initLevel(0);
    }
});

module.exports = Selects;