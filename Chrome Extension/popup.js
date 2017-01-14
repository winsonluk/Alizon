var port = chrome.extension.connect({
	name: "Sample Communication"
});

port.onMessage.addListener(function(msg) {
	console.log("message recieved" + msg);
});

function loadAll(){
 
  var state = document.getElementById("toggle").innerText;

  if(state == "Turn On"){
    document.getElementById("toggle").innerHTML = "Turn Off";
	port.postMessage("Off");
  } else if(state == "Turn Off"){
    document.getElementById("toggle").innerHTML = "Turn On";
    port.postMessage("On");
  } else{
    throw "Unexpected toggle error";
  }
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("toggle").addEventListener("click", loadAll)
});

