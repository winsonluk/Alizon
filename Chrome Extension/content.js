chrome.extension.onMessage.addListener(function(msg, sender, sendResponse) {
   if (msg.action == 'SendIt') {
      alert("Message recieved!");
   }
});

var on = true;

//check if dp is in the current url
if (on && /dp/.test(window.location.href)){

//wait til the document fully loads
document.addEventListener('DOMContentLoaded', function() {

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
					    var body = "<h2><a href='" + response["link"] + "'> Get the same or similar thing " + 
					    			"for only $" + response['price']  + "!</a></h2>";
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

/*        console.log("HI");
		var post = {link: 'https://www.amazon.com/Apple-Factory-Unlocked-Internal-Smartphone/dp/B00NQGP42Y/ref=s9_simh_gw_g107_i4_r?_encoding=UTF8&fpl=fresh&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=&pf_rd_r=RFGFD532PFF47QF1YTPV&pf_rd_t=36701&pf_rd_p=a6aaf593-1ba4-4f4e-bdcc-0febe090b8ed&pf_rd_i=desktop'};

        $.ajax({
            url: 'https://alizon.pythonanywhere.com/getInfo',
			data: JSON.stringify(post),
			dataType: "json",          
			type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });*/

});
}