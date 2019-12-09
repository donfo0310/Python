function handleBtnClick(event) {
    var pressed = (event.target.getAttribute("aria-pressed") === "true");
    event.target.setAttribute("aria-pressed", !pressed);
}