//toggles the state of status in localstorage
//communicates to content.js with background.js as proxy
function toggle(){
 
  var state = document.getElementById("toggle").innerText;
  console.log(state);
  if(state == "Turn On"){

    document.getElementById("toggle").innerHTML = "Turn Off";

	localStorage.status = "On";

    chrome.browserAction.setIcon({path: "active38.png"});

  } else if(state == "Turn Off"){

    document.getElementById("toggle").innerHTML = "Turn On";

    localStorage.status = "Off";

    chrome.browserAction.setIcon({path: "inactive38.png"});

  } else{

    throw "Unexpected toggle error";

  }

}

//waits until the page is fully loaded, then awaits click to toggle
document.addEventListener('DOMContentLoaded', function() {

	if(!localStorage.status) localStorage.status = "On";

	//popup.html resets per window open/close
	//save state in localStore, then load the proper
	//attributes and image for the browserAction and popup

	var state = localStorage.status;
	var buttonState;

	if(state == "On"){
		buttonState = "Off";
		chrome.browserAction.setIcon({path: "active38.png"});
	} else{
		buttonState = "On";
		chrome.browserAction.setIcon({path: "inactive38.png"});
	}
	
    document.getElementById("toggle").innerHTML = "Turn " + buttonState;

    //wait for user click to toggle the button
	document.getElementById("toggle").addEventListener("click", toggle)

});

