function likes(event, user_id, article_id) {

    // button-state
    var is_pressed = (event.target.getAttribute("aria-pressed") === "true");
    var span = event.currentTarget.getElementsByTagName('span')[0];
    var cnt = parseInt(span.innerHTML.slice(1).split(')')[0]);
    if(is_pressed) {
        event.target.setAttribute("aria-pressed", false);
        span.innerHTML = '(' + (cnt - 1) + ')';
    } else {
        event.target.setAttribute("aria-pressed", true);
        span.innerHTML = '(' + (cnt + 1) + ')';
    }

    // ajax: using pure javascript
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/vietnam_research/likes/' + user_id + '/' + article_id);
    xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
    xhr.send(); 
}