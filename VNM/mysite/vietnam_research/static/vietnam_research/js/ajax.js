function likes(event, user_id, article_id) {

    // toggle
    var pressed = (event.target.getAttribute("aria-pressed") === "true");
    event.target.setAttribute("aria-pressed", !pressed);

    // ajax: using pure javascript
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/vietnam_research/likes/' + user_id + '/' + article_id);
    xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
    xhr.send(); 
}