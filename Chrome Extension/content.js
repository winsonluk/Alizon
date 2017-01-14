function active(){
	//check if dp is in the current url
	if (/amazon/.test(window.location.href) && /dp/.test(window.location.href)){

		var link_ref = {link: window.location.href};

		//run script at the url, with data as argument, and json expected return type
	    $.ajax({
	        url: 'https://alizon.pythonanywhere.com/getInfo',
			data: JSON.stringify(link_ref),
			dataType: "json",          
			type: 'POST',
			//actions after a successful return from script
	        success: function(response) {

	        	if(response['price'] > 0){

	                //use the web accessible resources to inject a modal dialog bar
					var css = chrome.extension.getURL("style.css");
					$('<link rel="stylesheet" type="text/css" href="' + css + '" >').appendTo("head");

					var js = chrome.extension.getURL("modal-script.js");
					$('<script type="text/javascript" src="' + js + '"></script>').appendTo("head");

	                $.get(chrome.extension.getURL('modal.html'), function(data) {
					    $($.parseHTML(data)).appendTo('body');

					    var head = "<h2> A better deal was found at AliExpress! </h2>";
					    var body = "<h2><a href='" + response["link"] + "'>" +
					    			"Get the same or similar thing for only $"+ 
					    			response['price']  + "!</a> You " +
					    			"save $" + response['diff'].toFixed(2) + "</h2>";
					   	var foot = "(click out of the box to return to the screen)";

		                document.getElementById("modal-header").innerHTML = head;
		                document.getElementById("modal-body").innerHTML = body;
		                document.getElementById("modal-footer").innerHTML = foot;
					});
	            }

	            console.log(response);

	        },
	        error: function(error) {
	            console.log(error);
	        }
	    });

	}
}

//wait til the document fully loads
document.addEventListener('DOMContentLoaded', function() {

	//sends a message to the background.js
	//awaits for the response, if the status is "On", run the script
	chrome.runtime.sendMessage({type: "status"}, function(response) {
	    if(response.status == "On") active();
	    return;
	});

});