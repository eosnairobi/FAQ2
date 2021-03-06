/*
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3 & 4
Version: 4.1.0
Author: Sean Ngu
Website: https://www.seantheme.com/color-admin-v4.1/admin/
*/

var handleRenderHighlight = function() { 
	$('.hljs-wrapper pre code').each(function(i, block) {
		hljs.highlightBlock(block);
	});
};

var Highlight = function () {
	"use strict";
    return {
        //main function
        init: function () {
            handleRenderHighlight();
        }
    };
}();