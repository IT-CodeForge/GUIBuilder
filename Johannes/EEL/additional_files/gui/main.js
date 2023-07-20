var g_move_element = null
var g_move_mouse_x_offset = 0
var g_move_mouse_y_offset = 0
var g_active_gui_element = null
var g_last_gui_element_mousedown_event = 0
var gui_element_window = null
var gui_elements_main = null
var copy_elements = null
var menubar_elements = null
var element_attributes = null
var window_attributes = null


//UTILITY:

const pause = (time) => new Promise(resolve => setTimeout(resolve, time))

function getElement(id) {
    return document.getElementById(id)
}



window.onload = async function () {
    init_element_variables()
    t_w_id = await eel.gui_init()()
    addListeners()

    gui_element_window.data = {}
    gui_element_window.data.id = t_w_id
    gui_element_window.data.name = "window"
    gui_element_window.data.text = "Fenster"
    gui_element_window.data.size_x = 500
    gui_element_window.data.size_y = 500
    gui_element_window.data.background_color = "FFFFFF"
    gui_element_window.data.text_color = "000000"
    gui_element_window.data.event_create = false
    gui_element_window.data.event_paint = false
    gui_element_window.data.event_resize = false
    gui_element_window.data.event_mouse_click = false
    gui_element_window.data.event_mouse_move = false

    gui_elements_main.style.width = gui_element_window.data.size_x + "px"
    gui_elements_main.style.height = gui_element_window.data.size_y + "px"
    gui_elements_main.style.backgroundColor = "#" + gui_element_window.data.background_color

    window_attributes.id.textContent = gui_element_window.data.id
    window_attributes.name.value = gui_element_window.data.name
    window_attributes.text.value = gui_element_window.data.text
    window_attributes.size_x.value = gui_element_window.data.size_x
    window_attributes.size_y.value = gui_element_window.data.size_y
    window_attributes.text_color.value = gui_element_window.data.text_color
    window_attributes.background_color.value = gui_element_window.data.background_color
    window_attributes.event_create = gui_element_window.data.event_create
    window_attributes.event_paint = gui_element_window.data.event_paint
    window_attributes.event_resize = gui_element_window.data.event_resize
    window_attributes.event_mouse_click = gui_element_window.data.event_mouse_click
    window_attributes.event_mouse_move = gui_element_window.data.event_mouse_move
}



function init_element_variables() {
    window.gui_element_window = getElement("gui-element-0")
    window.gui_elements_main = getElement('gui-elements')
    window.copy_elements = { main: getElement("copy-elements"), btn: getElement("copy-element-btn") }
    window.menubar_elements = { main: getElement("menubar-elements"), btn: getElement("menubar-element-btn") }
    window.element_attributes = { main: getElement("element-attributes"), inner: getElement("element-attributes-inner"), id: getElement("element-attribut-id"), name: getElement("element-attribut-name"), text: getElement("element-attribut-text"), pos_x: getElement("element-attribut-position-x"), pos_y: getElement("element-attribut-position-y"), size_x: getElement("element-attribut-size-x"), size_y: getElement("element-attribut-size-y"), text_color: getElement("element-attribut-text-color"), background_color: getElement("element-attribut-background-color"), event_pressed: getElement("element-attribut-event-pressed"), event_hovered: getElement("element-attribut-event-hovered"), event_changed: getElement("element-attribut-event-changed") }
    window.window_attributes = { main: getElement("window-attributes"), id: getElement("window-attribut-id"), name: getElement("window-attribut-name"), text: getElement("window-attribut-text"), size_x: getElement("window-attribut-size-x"), size_y: getElement("window-attribut-size-y"), text_color: getElement("window-attribut-text-color"), background_color: getElement("window-attribut-background-color"), event_create: getElement("window-attribut-event-create"), event_paint: getElement("window-attribut-event-paint"), event_resize: getElement("window-attribut-event-resize"), event_mouse_click: getElement("window-attribut-event-mouse-click"), event_mouse_move: getElement("window-attribut-event-mouse-move") }
}


//EVENT-LISTENERS:

function addListeners() {

    window.addEventListener('mouseup', gui_element_mouseup_event, false)

    gui_elements_main.addEventListener('mousedown', gui_elements_mousedown_event, false)

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


// calculate and set GUI-Element Pos

function set_gui_element_translation(p_element, p_x, p_y) {
    var t_leftTranslation = p_x - gui_elements_main.getBoundingClientRect().left - window.g_move_mouse_x_offset
    var t_topTranslation = p_y - gui_elements_main.getBoundingClientRect().top - window.g_move_mouse_y_offset

    if (t_leftTranslation < 0)
        t_leftTranslation = 0
    else if (t_leftTranslation > (gui_element_window.data.size_x - p_element.data.size_x))
        t_leftTranslation = gui_element_window.data.size_x - p_element.data.size_x
    if (t_topTranslation < 0)
        t_topTranslation = 0
    else if (t_topTranslation > (gui_element_window.data.size_y - p_element.data.size_y))
        t_topTranslation = gui_element_window.data.size_y - p_element.data.size_y

    p_element.data.pos_x = t_leftTranslation;
    p_element.data.pos_y = t_topTranslation;

    if (g_active_gui_element == p_element) {
        element_attributes.pos_x.value = g_active_gui_element.data.pos_x
        element_attributes.pos_y.value = g_active_gui_element.data.pos_y
    }

    p_element.style.transform = "translate(" + t_leftTranslation + "px, " + t_topTranslation + "px)"
}


// GUI-MOVE-Methods

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


// load or create Elements

function load_window(p_attributes) {
    gui_element_window.data = p_attributes

    gui_elements_main.style.width = gui_element_window.data.size_x + "px"
    gui_elements_main.style.height = gui_element_window.data.size_y + "px"
    gui_elements_main.style.backgroundColor = "#" + gui_element_window.data.background_color

    window_attributes.id.textContent = gui_element_window.data.id
    window_attributes.name.value = gui_element_window.data.name
    window_attributes.text.value = gui_element_window.data.text
    window_attributes.size_x.value = gui_element_window.data.size_x
    window_attributes.size_y.value = gui_element_window.data.size_y
    window_attributes.text_color.value = gui_element_window.data.text_color
    window_attributes.background_color.value = gui_element_window.data.background_color
    window_attributes.event_create = gui_element_window.data.event_create
    window_attributes.event_paint = gui_element_window.data.event_paint
    window_attributes.event_resize = gui_element_window.data.event_resize
    window_attributes.event_mouse_click = gui_element_window.data.event_mouse_click
    window_attributes.event_mouse_move = gui_element_window.data.event_mouse_move
}

function create_gui_element(p_origin_element, p_attributes) {
    t_neu_element = p_origin_element.cloneNode(true)

    t_neu_element.classList.add("gui-element")

    t_neu_element.data = p_attributes

    t_neu_element.id = "gui-element-" + p_attributes.id

    gui_elements_main.append(t_neu_element)

    t_neu_element.addEventListener('mousedown', gui_element_mousedown_event, false)

    return t_neu_element
}

function create_new_element(p_origin_element, p_attributes, p_x, p_y, p_width, p_height) {
    const t_neu_element = create_gui_element(p_origin_element, p_attributes)

    t_neu_element.style.width = p_width + "px"
    t_neu_element.style.height = p_height + "px"
    t_neu_element.data.size_x = p_width
    t_neu_element.data.size_y = p_height

    t_neu_element.style.color = "#000000"
    t_neu_element.style.backgroundColor = "#FFFFFF"
    t_neu_element.data.text_color = "000000"
    t_neu_element.data.background_color = "FFFFFF"
    t_neu_element.data.event_pressed = true;
    t_neu_element.data.event_hovered = false;
    t_neu_element.data.event_changed = false;

    start_move_element(t_neu_element, p_x, p_y, p_origin_element)

    set_gui_element_translation(t_neu_element, p_x, p_y)

    set_active_gui_element(t_neu_element)
}

function load_gui_element(p_origin_element, p_attributes) {
    const t_neu_element = create_gui_element(p_origin_element, p_attributes)

    t_neu_element.textContent = p_attributes.text
    t_neu_element.style.transform = "translate(" + p_attributes.pos_x + "px, " + p_attributes.pos_y + "px)"
    t_neu_element.style.width = p_attributes.size_x + "px"
    t_neu_element.style.height = p_attributes.size_y + "px"
    t_neu_element.style.color = "#" + p_attributes.text_color
    t_neu_element.style.backgroundColor = "#" + p_attributes.background_color
}


// Active-Element-Attribut-Editor-Element

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
    element_attributes.text_color.value = g_active_gui_element.data.text_color
    element_attributes.background_color.value = g_active_gui_element.data.background_color
    element_attributes.event_pressed.checked = g_active_gui_element.data.event_pressed
    element_attributes.event_hovered.checked = g_active_gui_element.data.event_hovered
    element_attributes.event_changed.checked = g_active_gui_element.data.event_changed

    if (p_element.data.type == "button")
        element_attributes.event_changed.disabled = true
    else
        element_attributes.event_changed.disabled = false

    element_attributes.inner.style.visibility = ""
}

function reset_active_gui_element() {
    if (g_active_gui_element != null)
        g_active_gui_element.classList.remove("active-gui-element")
    element_attributes.inner.style.visibility = "hidden"
    g_active_gui_element = null
}


// Element-Attribut-Change-Events

function attribut_delete_element() {
    eel.delete_element(g_active_gui_element.data.id)
    g_active_gui_element.remove()
    g_active_gui_element = null
    reset_active_gui_element()
}

function attribut_set_name() {
    g_active_gui_element.data.name = element_attributes.name.value
}

function attribut_set_text() {
    g_active_gui_element.data.text = element_attributes.text.value
    if (element_attributes.text.value == "")
        g_active_gui_element.textContent = "undefined"
    else {
        g_active_gui_element.textContent = element_attributes.text.value
    }
}

function attribut_set_pos_x() {
    if (isNaN(element_attributes.pos_x.value)) {
        element_attributes.pos_x.value = g_active_gui_element.data.pos_x
        return;
    }
    g_active_gui_element.data.pos_x = Number(element_attributes.pos_x.value)
    g_active_gui_element.style.transform = "translate(" + g_active_gui_element.data.pos_x + "px, " + g_active_gui_element.data.pos_y + "px)"
}

function attribut_set_pos_y() {
    if (isNaN(element_attributes.pos_y.value)) {
        element_attributes.pos_y.value = g_active_gui_element.data.pos_y
        return;
    }
    g_active_gui_element.data.pos_y = Number(element_attributes.pos_y.value)
    g_active_gui_element.style.transform = "translate(" + g_active_gui_element.data.pos_x + "px, " + g_active_gui_element.data.pos_y + "px)"
}

function attribut_set_size_x() {
    if (isNaN(element_attributes.size_x.value)) {
        element_attributes.size_x.value = g_active_gui_element.data.size_x
        return;
    }
    g_active_gui_element.data.size_x = Number(element_attributes.size_x.value)
    g_active_gui_element.style.width = g_active_gui_element.data.size_x + "px"
}

function attribut_set_size_y() {
    if (isNaN(element_attributes.size_y.value)) {
        element_attributes.size_y.value = g_active_gui_element.data.size_y
        return;
    }
    g_active_gui_element.data.size_y = Number(element_attributes.size_y.value)
    g_active_gui_element.style.height = g_active_gui_element.data.size_y + "px"
}

function attribut_set_text_color() {
    g_active_gui_element.data.text_color = element_attributes.text_color.value
    g_active_gui_element.style.color = "#" + g_active_gui_element.data.text_color
}

function attribut_set_background_color() {
    g_active_gui_element.data.background_color = element_attributes.background_color.value
    g_active_gui_element.style.backgroundColor = "#" + g_active_gui_element.data.background_color
}

function attribut_set_event_pressed() {
    g_active_gui_element.data.event_pressed = element_attributes.event_pressed.checked
}

function attribut_set_event_hovered() {
    g_active_gui_element.data.event_hovered = element_attributes.event_hovered.checked
}

function attribut_set_event_changed() {
    g_active_gui_element.data.event_changed = element_attributes.event_changed.checked
}


// Window-Attribut-Change-Events

function window_set_name() {
    gui_element_window.data.name = window_attributes.name.value
}

function window_set_text() {
    gui_element_window.text.name = window_attributes.text.value
}

function window_set_size_x() {
    if (isNaN(window_attributes.size_x.value)) {
        window_attributes.size_x.value = gui_element_window.data.size_x
        return;
    }
    gui_element_window.data.size_x = Number(window_attributes.size_x.value)
    gui_elements_main.style.width = gui_element_window.data.size_x + "px"
}

function window_set_size_y() {
    if (isNaN(window_attributes.size_y.value)) {
        window_attributes.size_y.value = gui_element_window.data.size_y
        return;
    }
    gui_element_window.data.size_y = Number(window_attributes.size_y.value)
    gui_elements_main.style.height = gui_element_window.data.size_y + "px"
}

function window_set_text_color() {
    gui_element_window.data.text_color = window_attributes.text_color.value
}

function window_set_background_color() {
    gui_element_window.data.background_color = window_attributes.background_color.value
    gui_elements_main.style.backgroundColor = "#" + gui_element_window.data.background_color
}

function window_set_event_create() {
    gui_element_window.data.event_create = window_attributes.event_create.checked
}

function window_set_event_paint() {
    gui_element_window.data.event_paint = window_attributes.event_paint.checked
}

function window_set_event_resize() {
    gui_element_window.data.event_resize = window_attributes.event_resize.checked
}

function window_set_event_mouse_click() {
    gui_element_window.data.event_mouse_click = window_attributes.event_mouse_click.checked
}

function window_set_event_mouse_move() {
    gui_element_window.data.event_mouse_move = window_attributes.event_mouse_move.checked
}



async function load_gui_elements_from_database() {
    const t_gui_elements = await eel.load_gui_elements()()
    window.temptest = t_gui_elements
    for (i = 0; i < t_gui_elements.length; i++) {
        const t_akt = t_gui_elements[i]
        const attribut = { id: t_akt.id, name: t_akt.name, text: t_akt.text, pos_x: t_akt.position[0], pos_y: t_akt.position[1], size_x: t_akt.size[0], size_y: t_akt.size[1], text_color: t_akt.textColor[0].toString(16) + t_akt.textColor[1].toString(16) + t_akt.textColor[2].toString(16), background_color: t_akt.backgroundColor[0].toString(16) + t_akt.backgroundColor[1].toString(16) + t_akt.backgroundColor[2].toString(16), event_pressed: t_akt.eventPressed, event_hovered: t_akt.eventHovered, event_changed: t_akt.eventChanged, event_create: t_akt.eventCreate, event_paint: t_akt.eventPaint, event_resize: t_akt.eventResize, event_mouse_click: t_akt.eventMouseClick, event_mouse_move: t_akt.eventMouseMove };
        console.log(attribut)
        switch (t_akt.type) {
            case "window":
                load_window(attribut)
                break

            case "button":
                load_gui_element(copy_elements.btn, attribut)
                break

            default:
                break
        }
    }
    console.log("test")
}

async function save_gui_elements_to_database() {
    const t_gui_elements = document.getElementsByClassName("gui-element")
    for (i = 0; i < t_gui_elements.length; i++) {
        const akt = t_gui_elements[i]
        const t_text_color = [Number("0x" + akt.data.text_color.substring(0, 2)), Number("0x" + akt.data.text_color.substring(2, 4)), Number("0x" + akt.data.text_color.substring(4, 6))]
        const t_bg_col = [Number("0x" + akt.data.background_color.substring(0, 2)), Number("0x" + akt.data.background_color.substring(2, 4)), Number("0x" + akt.data.background_color.substring(4, 6))]
        if (akt.type == "submit")
            await eel.save_gui_element(akt.data.id, akt.data.name, akt.data.text, [akt.data.pos_x, akt.data.pos_y], [akt.data.size_x, akt.data.size_y], t_bg_col, t_text_color, akt.data.event_pressed, akt.data.event_hovered, akt.data.event_changed)()
    }
    await eel.save()()
}
