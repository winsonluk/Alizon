//wait for popup.js event, then signal content.js for action
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.type == "status") sendResponse({status: localStorage.status});
});