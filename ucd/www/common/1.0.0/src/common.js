require('global');
var $ = require('$');
require('com/tabs:tabs');
require('region').initAll();
$('.warmheart-advisers').tabs({
    type: 'click',
    menuNode: '.rank-title-tab a',
    contNode: '.rank-type',
    className: 'active'
});
// @require './common.css';
