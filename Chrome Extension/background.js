chrome.extension.onConnect.addListener(function(port) {
	console.log("Connected .....");
	port.onMessage.addListener(function(msg) {
		console.log("message recieved" + msg);

		if(msg == "On"){
			toggleExtension(true);
		} else {
			toggleExtension(false);
		}
		port.postMessage("Hi Popup.js");
	});
})

chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
    chrome.tabs.sendMessage(tabs[0].id, {action: "SendIt"}, function(response) {});  
});

function toggleExtension(disabled)
{

    chrome.windows.getAll({populate : true}, function (window_list)
    {
        for (var i = 0; i < window_list.length; ++i)
        {
            var window = window_list[i];
            for (var j = 0; j < window.tabs.length; ++j)
            {
                var tab = window.tabs[j];
                if (checkContentScriptExists(tab))
                {
                    chrome.tabs.executeScript(tab.id, {code : "disabled = " + disabled + ";"}, allTabs: true) 
                }
            }
        }
        // No matching url found. Open it in the new tab
        chrome.tabs.create({ url : url, selected: true });
    });
}