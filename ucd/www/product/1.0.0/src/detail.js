require('./common.js');
var $ = require('$');
$('.product-information').tabs({
    type: 'click',
    menuNode: '.product-information-tabs li',
    contNode: '.product-info-detail,.product-info-example,.product-info-process',
    className: 'active'
});
// @require './detail.css';
