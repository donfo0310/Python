function likes(event, user_id, article_id) {

    // toggle
    var pressed = (event.target.getAttribute("aria-pressed") === "true");
    event.target.setAttribute("aria-pressed", !pressed);

    // likes count up/down
    console.log(event.currentTarget.getElementsByTagName('span')[0].innerHTML.slice(1).split(')')[0]);

    // ajax: using pure javascript
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/vietnam_research/likes/' + user_id + '/' + article_id);
    xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
    xhr.send(); 
}