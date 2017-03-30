var django = django || {};
django.jQuery = jQuery.noConflict(true);

(function($) {
    'use strict';
    $(function() {
        $('.comment_id').click(function() {
        		var cNum = $(this).text();
        		if(!cNum)
        			return;
        		var inputElm = $('#comment-form input[type=text]');
        		var orgVal = inputElm.val();
        		var newVal = orgVal == '' ? cNum : orgVal + ',' + cNum
        		inputElm.val(newVal);
        });
    });
})(django.jQuery);
