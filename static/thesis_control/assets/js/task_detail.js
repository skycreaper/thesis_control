var clicked = false;

var panel_header = $('#panel-heading');
var panel_body = $('#panel-body');

panel_header.click(function() {
    if (clicked) {
        panel_body.slideDown();
    } else {
        panel_body.slideUp();
    }
    clicked = !clicked;
});