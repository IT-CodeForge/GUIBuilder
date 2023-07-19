var g_move_element = null
var g_move_mouse_x_offset = 0
var g_move_mouse_y_offset = 0
var g_active_gui_element = null
var g_last_gui_element_mousedown_event = 0

const pause = (time) => new Promise(resolve => setTimeout(resolve, time))

function addListeners() {

    window.addEventListener('mouseup', gui_element_mouseup_event, false)

    gui_elements.addEventListener('mousedown', gui_elements_mousedown_event, false)

    const t_elements = document.getElementsByClassName('gui-element')
    for (i = 0; i < t_elements.length; i++) {
        t_elements[i].addEventListener('mousedown', gui_element_mousedown_event, false)
    }
    menubar_elements.btn.addEventListener('mousedown', menubar_element_btn_mousedown_event, false)
}

async function gui_elements_mousedown_event(e) {
    await pause(50)
    if (new Date().getTime() - g_last_gui_element_mousedown_event > 70)
        reset_active_gui_element()
}

function gui_element_mousedown_event(e) {
    g_last_gui_element_mousedown_event = new Date().getTime()
    if (g_active_gui_element == null || g_active_gui_element != e.target)
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
    const t_attributes = await eel.create_btn()()
    create_new_element(copy_elements.btn, t_attributes, e.clientX, e.clientY, 70, 25)
}



function start_move_element(p_element, p_mouseX, p_mouseY, p_offset_element_override = p_element) {
    window.addEventListener('mousemove', gui_element_mousemove_event, true)
    window.g_move_mouse_x_offset = p_mouseX - p_offset_element_override.getBoundingClientRect().left
    window.g_move_mouse_y_offset = p_mouseY - p_offset_element_override.getBoundingClientRect().top
    window.g_move_element = p_element
    p_element.classList.add("element-moving")
    document.body.style.cursor = "grabbing"
}

function end_move_element(p_element) {
    window.removeEventListener('mousemove', gui_element_mousemove_event, true)
    window.g_move_mouse_x_offset = 0
    window.g_move_mouse_y_offset = 0
    window.g_move_element = null
    p_element.classList.remove("element-moving")
    document.body.style.cursor = ""
}

function set_gui_element_translation(p_element, p_x, p_y) {
    var t_leftTranslation = p_x - gui_elements.getBoundingClientRect().left - window.g_move_mouse_x_offset
    var t_topTranslation = p_y - gui_elements.getBoundingClientRect().top - window.g_move_mouse_y_offset

    if (t_leftTranslation < 0)
        t_leftTranslation = 0
    if (t_topTranslation < 0)
        t_topTranslation = 0

    p_element.data.pos_x = t_leftTranslation;
    p_element.data.pos_y = t_topTranslation;

    if (g_active_gui_element == p_element) {
        element_attributes.pos_x.value = g_active_gui_element.data.pos_x
        element_attributes.pos_y.value = g_active_gui_element.data.pos_y
    }

    p_element.style.transform = "translate(" + t_leftTranslation + "px, " + t_topTranslation + "px)"
}

function create_gui_element(p_origin_element, p_attributes) {
    t_neu_element = p_origin_element.cloneNode(true)

    t_neu_element.classList.add("gui-element")

    t_neu_element.data = p_attributes

    t_neu_element.id = "menubar-element-" + p_attributes.id

    gui_elements.append(t_neu_element)

    t_neu_element.addEventListener('mousedown', gui_element_mousedown_event, false)

    return t_neu_element
}

function create_new_element(p_origin_element, p_attributes, p_x, p_y, p_width, p_height) {
    const t_neu_element = create_gui_element(p_origin_element, p_attributes)

    t_neu_element.style.width = p_width + "px"
    t_neu_element.style.height = p_height + "px"
    t_neu_element.data.size_x = p_width
    t_neu_element.data.size_y = p_height

    start_move_element(t_neu_element, p_x, p_y, p_origin_element)

    set_gui_element_translation(t_neu_element, p_x, p_y)

    set_active_gui_element(t_neu_element)
}

function load_gui_element(p_origin_element, p_attributes) {
    const t_neu_element = create_gui_element(p_origin_element, p_attributes)

    t_neu_element.textContent = element_attributes.text.value
    set_gui_element_translation(t_neu_element, p_attributes.postition[0], p_attributes.postition[1])
    //NOTE: SIZE
    t_neu_element.style.color = p_attributes.textColor
    t_neu_element.style.backgroundColor = p_attributes.backgroundColor
}



function set_active_gui_element(p_element) {
    if (g_active_gui_element != null)
        g_active_gui_element.classList.remove("active-gui-element")
    g_active_gui_element = p_element
    g_active_gui_element.classList.add("active-gui-element")

    element_attributes.id.textContent = g_active_gui_element.data.id
    element_attributes.name.value = g_active_gui_element.data.name
    element_attributes.text.value = g_active_gui_element.data.text
    element_attributes.pos_x.value = g_active_gui_element.data.pos_x
    element_attributes.pos_y.value = g_active_gui_element.data.pos_y
    element_attributes.size_x.value = g_active_gui_element.data.size_x
    element_attributes.size_y.value = g_active_gui_element.data.size_y

    element_attributes.inner.style.visibility = ""
}

function reset_active_gui_element() {
    if (g_active_gui_element != null)
        g_active_gui_element.classList.remove("active-gui-element")
    element_attributes.inner.style.visibility = "hidden"
    g_active_gui_element = null
}

function attribut_setname() {
}

function attribut_settext() {
    if (element_attributes.text.value == "")
        g_active_gui_element.textContent = "undefined"
    else
        g_active_gui_element.textContent = element_attributes.text.value
}

function attribut_setpos_x() {
    if (isNaN(element_attributes.pos_x.value))
    {
        element_attributes.pos_x.value = g_active_gui_element.data.pos_x
        return;
    }
    g_active_gui_element.data.pos_x = Number(element_attributes.pos_x.value)
    g_active_gui_element.style.transform = "translate(" + g_active_gui_element.data.pos_x + "px, " + g_active_gui_element.data.pos_y + "px)"
}

function attribut_setpos_y() {
    if (isNaN(element_attributes.pos_y.value))
    {
        element_attributes.pos_y.value = g_active_gui_element.data.pos_y
        return;
    }
    g_active_gui_element.data.pos_y = Number(element_attributes.pos_y.value)
    g_active_gui_element.style.transform = "translate(" + g_active_gui_element.data.pos_x + "px, " + g_active_gui_element.data.pos_y + "px)"
}

function attribut_setsize_x() {
    if (isNaN(element_attributes.size_x.value))
    {
        element_attributes.size_x.value = g_active_gui_element.data.size_x
        return;
    }
    g_active_gui_element.data.size_x = Number(element_attributes.size_x.value)
    g_active_gui_element.style.width = g_active_gui_element.data.size_x + "px"
}

function attribut_setsize_y() {
    if (isNaN(element_attributes.size_y.value))
    {
        element_attributes.size_y.value = g_active_gui_element.data.size_y
        return;
    }
    g_active_gui_element.data.size_y = Number(element_attributes.size_y.value)
    g_active_gui_element.style.height = g_active_gui_element.data.size_y + "px"
}



async function load_gui_elements() {
    const t_gui_elements = await eel.load_gui_elements()()
    window.temptest = t_gui_elements
    for (i = 0; i < t_gui_elements.length; i++) {
        const t_akt = t_gui_elements[i]
        switch (t_akt.type) {
            case "button":
                create_new_element(copy_elements.btn, 0, 0, t_akt)
                break

            default:
                break
        }
    }
    console.log("test")
}



function getElement(id) {
    return document.getElementById(id)
}

function init_element_variables() {
    window.gui_elements = getElement('gui-elements')
    window.copy_elements = { main: getElement("copy-elements"), btn: getElement("copy-element-btn") }
    window.menubar_elements = { main: getElement("menubar-elements"), btn: getElement("menubar-element-btn") }
    window.element_attributes = { main: getElement("element-attributes"), inner: getElement("element-attributes-inner"), id: getElement("element-attribut-id"), name: getElement("element-attribut-name"), text: getElement("element-attribut-text"), pos_x: getElement("element-attribut-position-x"), pos_y: getElement("element-attribut-position-y"), size_x: getElement("element-attribut-size-x"), size_y: getElement("element-attribut-size-y") }
}

window.onload = function () {
    init_element_variables()
    addListeners()
}
