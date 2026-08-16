
jQuery(document).ready(function(event) {
	"use strict";
	
	jQuery('.ekit-mailChimpForm').submit(ajaxMailSubmit);
 
	function ajaxMailSubmit(e) {
		e.preventDefault();
		var mailForm = jQuery(this).serialize();
		
		jQuery.ajax({           
            data : mailForm,
            type : 'get',
            url : ekit_site_url.siteurl+'/wp-json/elementskit/v1/widget/mailchimp/sendmail/',
			success : function( response ) {
				//var messageBox =  jQuery(this).find('.ekit-mail-message');
				var messageBox =  jQuery('.ekit-mail-message');
                if(response.error.length > 0){
					messageBox.html( 'Found error' + response.error );
					return;
				}
				var obj = JSON.parse(response.success.body);
				if(obj.status == 'subscribed'){
					messageBox.html('Successfully listed this email');
					return;
				}
				messageBox.html(obj.title);
            }
        });
		
	}
});
