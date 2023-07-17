function addListeners() {
    elements = document.getElementsByClassName('gui-element')
    for (i = 0; i < elements.length; i++)
    {
        elements[i].addEventListener('mousedown', gui_element_mousedown_event, false);
    }
    window.addEventListener('mouseup', gui_element_mouseup_event, false);

    window.menubar_element_btn = document.getElementById("menubar-element-btn");
    menubar_element_btn.addEventListener('mousedown', createBTN, false);
}

function gui_element_mouseup_event() {
    window.removeEventListener('mousemove', gui_element_mousemove_event, true);
}

function gui_element_mousedown_event(e) {
    window.addEventListener('mousemove', gui_element_mousemove_event, true);
    const element = e.target;
    window.t_move_mouse_x_offset = e.clientX - element.getBoundingClientRect().left
    window.t_move_mouse_y_offset = e.clientY - element.getBoundingClientRect().top
    window.t_move_element = element
}

function gui_element_mousemove_event(e) {
    const left = (e.clientX - gui_elements.getBoundingClientRect().left - window.t_move_mouse_x_offset) + 'px';
    const top = (e.clientY - gui_elements.getBoundingClientRect().top - window.t_move_mouse_y_offset) + 'px';
    window.t_move_element.style.transform = "translate(" + left + ", " + top + ")"
    //console.log("translate(" + left + ", " + top + ")")
}

function createBTN(e) {
    t_neu = e.target.cloneNode(true);
    t_neu.id = "";
    t_neu.style.position = "absolute";
    t_neu.style.top = "";
    t_neu.style.left = "";
    t_neu.style.transform = "translate(0px, 0px)";
    t_neu.style.class = "gui-element";
    const left = (e.target.getBoundingClientRect().left - gui_elements.getBoundingClientRect().left) + 'px';
    const top = (e.target.getBoundingClientRect().left - gui_elements.getBoundingClientRect().top) + 'px';
    t_neu.style.transform = "translate(" + left + ", " + top + ")"
    t_neu.addEventListener('mousedown', gui_element_mousedown_event, false);
    window.addEventListener('mousemove', gui_element_mousemove_event, true);
    const element = e.target;
    window.t_move_mouse_x_offset = e.clientX - element.getBoundingClientRect().left
    window.t_move_mouse_y_offset = e.clientY - element.getBoundingClientRect().top
    window.t_move_element = t_neu
    gui_elements.append(t_neu);
}

window.onload = function () {
    addListeners();
    window.gui_elements = document.getElementById('gui-elements');
}