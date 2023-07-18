var g_move_element = null
var g_move_mouse_x_offset = 0
var g_move_mouse_y_offset = 0
var g_active_gui_element = null
var g_last_gui_element_mousedown_event = 0

const pause = (time) => new Promise(resolve => setTimeout(resolve, time))

function addListeners() {

    window.addEventListener('mouseup', gui_element_mouseup_event, false);

    gui_elements.addEventListener('mousedown', gui_elements_mousedown_event, false)

    const t_elements = document.getElementsByClassName('gui-element')
    for (i = 0; i < t_elements.length; i++) {
        t_elements[i].addEventListener('mousedown', gui_element_mousedown_event, false);
    }

    window.menubar_element_btn = document.getElementById("menubar-element-btn");
    menubar_element_btn.addEventListener('mousedown', menubar_element_btn_mousedown_event, false);
}

async function gui_elements_mousedown_event(e) {
    await pause(50)
    if (new Date().getTime() - g_last_gui_element_mousedown_event > 70)
        reset_active_gui_element()
}

function gui_element_mousedown_event(e) {
    g_last_gui_element_mousedown_event = new Date().getTime()
    if (g_active_gui_element == null)
        set_active_gui_element(e.target)
    else
        start_move_element(e.target, e.clientX, e.clientY)
}

function gui_element_mouseup_event() {
    if (g_move_element != null)
        end_move_element(g_move_element)
}

function gui_element_mousemove_event(e) {
    set_gui_element_translation(g_move_element, e.clientX, e.clientY)
}

async function menubar_element_btn_mousedown_event(e) {
    const id = await eel.create_btn()()
    create_element(e.target, e.clientX, e.clientY, id)
}



function start_move_element(p_element, p_mouseX, p_mouseY, p_offset_element_override = p_element) {
    window.addEventListener('mousemove', gui_element_mousemove_event, true);
    window.g_move_mouse_x_offset = p_mouseX - p_offset_element_override.getBoundingClientRect().left
    window.g_move_mouse_y_offset = p_mouseY - p_offset_element_override.getBoundingClientRect().top
    window.g_move_element = p_element
    p_element.classList.add("element-moving")
    document.body.style.cursor = "grabbing"
}

function end_move_element(p_element) {
    window.removeEventListener('mousemove', gui_element_mousemove_event, true);
    window.g_move_mouse_x_offset = 0
    window.g_move_mouse_y_offset = 0
    window.g_move_element = null
    p_element.classList.remove("element-moving")
    document.body.style.cursor = ""
}

function set_gui_element_translation(p_element, p_x, p_y) {
    var t_leftTranslation = p_x - gui_elements.getBoundingClientRect().left - window.g_move_mouse_x_offset;
    var t_topTranslation = p_y - gui_elements.getBoundingClientRect().top - window.g_move_mouse_y_offset;

    if (t_leftTranslation < 0)
        t_leftTranslation = 0
    if (t_topTranslation < 0)
        t_topTranslation = 0

    p_element.style.transform = "translate(" + t_leftTranslation + "px, " + t_topTranslation + "px)"
}

function create_element(p_element, p_x, p_y, id) {
    t_neu_element = p_element.cloneNode(true);

    t_neu_element.id = "menubar-element-"+id;
    t_neu_element.classList.remove("menubar-element")
    t_neu_element.classList.add("gui-element")
    t_neu_element.style.position = "absolute";
    t_neu_element.style.top = "";
    t_neu_element.style.left = "";
    t_neu_element.style.transform = "translate(0px, 0px)";

    t_neu_element.data = {"id": id}

    start_move_element(t_neu_element, p_x, p_y, p_element)

    set_gui_element_translation(t_neu_element, p_x, p_y)

    t_neu_element.addEventListener('mousedown', gui_element_mousedown_event, false);

    gui_elements.append(t_neu_element);
}



function set_active_gui_element(p_element) {
    if (g_active_gui_element != null)
        g_active_gui_element.classList.remove("active-gui-element")
    g_active_gui_element = p_element
    g_active_gui_element.classList.add("active-gui-element")

    const t_titel = document.getElementById("element-attributes-titel")
    t_titel.value = g_active_gui_element.textContent

    document.getElementById("element-attributes-inner").style.visibility = ""
}

function reset_active_gui_element() {
    if (g_active_gui_element != null)
        g_active_gui_element.classList.remove("active-gui-element")
    document.getElementById("element-attributes-inner").style.visibility = "hidden"
    g_active_gui_element = null
}

function attribut_setname() {
    const input = document.getElementById("element-attributes-name")
}

function attribut_settitel() {
    const input = document.getElementById("element-attributes-titel")
    if (input.value == "")
        g_active_gui_element.textContent = "undefined"
    else
        g_active_gui_element.textContent = input.value
}



async function load_gui_elements() {
    const t_gui_elements = await eel.load_gui_elements()();
}



window.onload = function () {
    window.gui_elements = document.getElementById('gui-elements');

    addListeners();
}
