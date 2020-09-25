$(function(){
    $('.nav li a').each(function(){
		var href = $(this).attr('href');
        if(location.href.match(href)) {
    	    $(this).addClass('active');
        } else {
    	    $(this).removeClass('active');
        }
    	var conf = $('#navbar-configuration')
    	if (location.href.match('/configuration')){
    		conf.addClass('active')
    	}
    	else{
    		conf.removeClass('active')
    	}
    });
});
