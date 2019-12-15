function likes(event) {

    // toggle
    var pressed = (event.target.getAttribute("aria-pressed") === "true");
    event.target.setAttribute("aria-pressed", !pressed);

    // ajax: using pure javascript
    var xhr = new XMLHttpRequest();
    xhr.open('POST', "/vietnam_research/likes/1/2");
    xhr.onload = function() {
        if (xhr.status === 200) {
            alert('ajax ok')
        }
        else {
            alert('Request failed.  Returned status of ' + status)
        }
        function callback(result){
            alert(result + ' is done!')
        }
    };
    xhr.send(); 
}