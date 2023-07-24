var g_move_element = null // enthält das Element, welches aktuell vom User verschoben wird
var g_move_mouse_x_offset = 0 // enthält mouse_offset der aktuellen Element-verschiebungs-Aktion.
var g_move_mouse_y_offset = 0 // enthält mouse_offset der aktuellen Element-verschiebungs-Aktion.
var g_active_gui_element = null // enthält das Element, welches aktuell ausgewält ist und im Attributeditor angezeigt wird.
var g_last_gui_element_mousedown_event = 0 // Timestamp des letzten gui_element_mousedown_events
var g_prog_language = null // enthält die ausgewählte Programmiersprache

// Dictionary mit HTML-Elementen für vereinfachten Zugriff.
var gui_elements_main = null
var copy_elements = null
var menubar_elements = null
var element_attributes = null
var window_attributes = null


// UTILITY:

const pause = (time) => new Promise(resolve => setTimeout(resolve, time))

// shortcut to get ElementsById
function getElement(id) {
    return document.getElementById(id)
}

// called by Collapsables to expand or hide content
function toggleCollapsable(p_collapsable) {
    p_collapsable.classList.toggle("collapsible-active");
    var t_content = p_collapsable.nextElementSibling;
    if (t_content.style.display) {
        t_content.style.display = null;
    } else {
        t_content.style.display = "block";
    }
}



// Wird vor dem Schließen der Seite ausgeführt
window.onbeforeunload = function (e) {
    return 'Unsaved changes!';
};

// Wird beim Laden der Seite ausgeführt
window.onload = async function () {
    init_element_variables()

    set_language()

    t_w_attr = await eel.gui_init()()
    load_window(t_w_attr)

    addListeners()
}



// setzt alle element_variablen
function init_element_variables() {
    window.gui_elements_main = getElement('gui-elements')
    window.copy_elements = { main: getElement("copy-elements"), btn: getElement("copy-element-btn"), label: getElement("copy-element-label"), edit: getElement("copy-element-edit"), checkbox: getElement("copy-element-checkbox"), canvas: getElement("copy-element-canvas"), timer: getElement("copy-element-timer") }
    window.menubar_elements = { main: getElement("menubar-elements"), btn: getElement("menubar-element-btn"), label: getElement("menubar-element-label"), edit: getElement("menubar-element-edit"), checkbox: getElement("menubar-element-checkbox"), canvas: getElement("menubar-element-canvas"), timer: getElement("menubar-element-timer"), select_language: getElement("menubar-element-select-language") }
    window.element_attributes = { main: getElement("element-attributes"), inner: getElement("element-attributes-inner"), id: getElement("element-attribut-id"), name: getElement("element-attribut-name"), text_section: getElement("element-attribut-text-section"), text: getElement("element-attribut-text"), pos_x: getElement("element-attribut-position-x"), pos_y: getElement("element-attribut-position-y"), size_x: getElement("element-attribut-size-x"), size_y: getElement("element-attribut-size-y"), text_color_section: getElement("element-attribut-text-color-section"), text_color: getElement("element-attribut-text-color"), background_color_section: getElement("element-attribut-background-color-section"), background_color: getElement("element-attribut-background-color"), interval_section: getElement("element-attribut-interval-section"), interval: getElement("element-attribut-interval"), multiple_lines_section: getElement("element-attribut-multiple-lines-section"), checked_section: getElement("element-attribut-checked-section"), checked: getElement("element-attribut-checked"), enabled_section: getElement("element-attribut-enabled-section"), enabled: getElement("element-attribut-enabled"), multiple_lines: getElement("element-attribut-multiple-lines"), event_section: getElement("element-attribut-section"), event_pressed_section: getElement("element-attribut-event-pressed-section"), event_pressed: getElement("element-attribut-event-pressed"), event_double_pressed_section: getElement("element-attribut-event-double-pressed-section"), event_double_pressed: getElement("element-attribut-event-double-pressed"), event_hovered_section: getElement("element-attribut-event-hovered-section"), event_hovered: getElement("element-attribut-event-hovered"), event_changed_section: getElement("element-attribut-event-changed-section"), event_changed: getElement("element-attribut-event-changed") }
    window.window_attributes = { main: getElement("window-attributes"), id: getElement("window-attribut-id"), name: getElement("window-attribut-name"), text: getElement("window-attribut-text"), size_x: getElement("window-attribut-size-x"), size_y: getElement("window-attribut-size-y"), text_color: getElement("window-attribut-text-color"), background_color: getElement("window-attribut-background-color"), event_create: getElement("window-attribut-event-create"), event_destroy: getElement("window-attribut-event-destroy"), event_paint: getElement("window-attribut-event-paint"), event_resize: getElement("window-attribut-event-resize"), event_mouse_click: getElement("window-attribut-event-mouse-click"), event_mouse_move: getElement("window-attribut-event-mouse-move") }
}


// Set Programming Language
function set_language() {
    g_prog_language = menubar_elements.select_language.value

    if (g_prog_language == "C++") {
        element_attributes.text_color.disabled = true;
        element_attributes.background_color.disabled = true;
        element_attributes.event_hovered.disabled = true;
        window_attributes.text_color.disabled = true;
        window_attributes.background_color.disabled = true;
    }
    else {
        element_attributes.text_color.disabled = false;
        element_attributes.background_color.disabled = false;
        element_attributes.event_hovered.disabled = false;
        window_attributes.text_color.disabled = false;
        window_attributes.background_color.disabled = false;
    }
}


//EVENT-LISTENERS:

function addListeners() {

    window.addEventListener('mouseup', gui_element_mouseup_event, false)
    gui_elements_main.addEventListener('mousedown', gui_elements_mousedown_event, false)

    // Fügt allen GUI-Elementen den Eventhandler hinzu.
    const t_elements = document.getElementsByClassName('gui-element')
    for (i = 0; i < t_elements.length; i++) {
        t_elements[i].addEventListener('mousedown', gui_element_mousedown_event, false)
    }
    
    // fügt alles Menubar-create-Elementen den Eventhandler hinzu.
    menubar_elements.btn.addEventListener('mousedown', menubar_element_btn_mousedown_event, false)
    menubar_elements.label.addEventListener('mousedown', menubar_element_label_mousedown_event, false)
    menubar_elements.edit.addEventListener('mousedown', menubar_element_edit_mousedown_event, false)
    menubar_elements.checkbox.addEventListener('mousedown', menubar_element_checkbox_mousedown_event, false)
    menubar_elements.canvas.addEventListener('mousedown', menubar_element_canvas_mousedown_event, false)
    menubar_elements.timer.addEventListener('mousedown', menubar_element_timer_mousedown_event, false)
}

async function gui_elements_mousedown_event(e) {
    // prüft, ob auf gui_elements_main geklickt wurde oder auf ein GUI_ELEMENT, da in diesem Fall beide funktionen aufgerufen werden.
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
    set_gui_element_translation_from_abs_coords(g_move_element, e.clientX, e.clientY)
}

async function menubar_element_btn_mousedown_event(e) {
    const t_attributes = await eel.create_btn()()
    const t_neu_element = create_new_element(copy_elements.btn, t_attributes, e.clientX, e.clientY, e.target)
}

async function menubar_element_label_mousedown_event(e) {
    const t_attributes = await eel.create_label()()
    const t_neu_element = create_new_element(copy_elements.label, t_attributes, e.clientX, e.clientY, e.target)
}

async function menubar_element_edit_mousedown_event(e) {
    const t_attributes = await eel.create_edit()()
    const t_neu_element = create_new_element(copy_elements.edit, t_attributes, e.clientX, e.clientY, e.target)
}

async function menubar_element_checkbox_mousedown_event(e) {
    const t_attributes = await eel.create_checkbox()()
    const t_neu_element = create_new_element(copy_elements.checkbox, t_attributes, e.clientX, e.clientY, e.target)
}

async function menubar_element_canvas_mousedown_event(e) {
    const t_attributes = await eel.create_canvas()()
    const t_neu_element = create_new_element(copy_elements.canvas, t_attributes, e.clientX, e.clientY, e.target)
}

async function menubar_element_timer_mousedown_event(e) {
    const t_attributes = await eel.create_timer()()
    const t_neu_element = create_new_element(copy_elements.timer, t_attributes, e.clientX, e.clientY, e.target)
}


// calculate and set GUI-Element Pos

function set_gui_element_translation_from_abs_coords(p_element, p_x, p_y) {
    // Berechnet relative GUI-Position aus absoluten Mouse-Koordinaten
    var t_x = p_x - gui_elements_main.getBoundingClientRect().left - window.g_move_mouse_x_offset
    var t_y = p_y - gui_elements_main.getBoundingClientRect().top - window.g_move_mouse_y_offset

    set_gui_element_translation(p_element, t_x, t_y)
}

function set_gui_element_translation(p_element, p_x, p_y) {
    // Prüft, ob Mouse außerhalb des GUI-Bereiches
    if (p_x < 0)
    p_x = 0
    else if (p_x > (gui_elements_main.data.size_x - p_element.data.size_x))
    p_x = gui_elements_main.data.size_x - p_element.data.size_x
    if (p_y < 0)
    p_y = 0
    else if (p_y > (gui_elements_main.data.size_y - p_element.data.size_y))
    p_y = gui_elements_main.data.size_y - p_element.data.size_y

    // Rundet auf ganze Zahlen
    p_x = Math.round(p_x)
    p_y = Math.round(p_y)

    p_element.data.pos_x = p_x;
    p_element.data.pos_y = p_y;

    // Aktuallisiert die Positionsanzeige im Element-Attribut-Editor, falls das verschobene Element auch das dort angezeigte ist.
    if (g_active_gui_element == p_element) {
        element_attributes.pos_x.value = g_active_gui_element.data.pos_x
        element_attributes.pos_y.value = g_active_gui_element.data.pos_y
    }

    // setzt schlussendlich die Position
    p_element.style.transform = "translate(" + p_x + "px, " + p_y + "px)"
}

function reprocess_element_translation(p_element) {
    set_gui_element_translation(p_element, p_element.data.pos_x, p_element.data.pos_y);
}

function reprocess_all_elements_translation() {
    t_gui_elements = document.getElementsByClassName("gui-element")
    for (i=0; i<t_gui_elements.length; i++)
    reprocess_element_translation(t_gui_elements[i])
}



// load or store Element to database
async function load_gui_elements_from_database() {
    const t_gui_elements = await eel.load_gui_elements()()
    for (i = 0; i < t_gui_elements.length; i++) {
        const t_akt = t_gui_elements[i]
        switch (t_akt.type) {
            case "window":
                load_window(t_akt)
                break

            case "button":
                load_gui_element(copy_elements.btn, t_akt)
                break

            case "label":
                load_gui_element(copy_elements.label, t_akt)
                break

            case "edit":
                load_gui_element(copy_elements.edit, t_akt)
                break

            case "checkbox":
                load_gui_element(copy_elements.checkbox, t_akt)
                break

            case "canvas":
                load_gui_element(copy_elements.canvas, t_akt)
                break

            case "timer":
                load_gui_element(copy_elements.timer, t_akt)
                break

            default:
                break
        }
    }
}

async function save_gui_elements_to_database() {
    const t_gui_elements = document.getElementsByClassName("gui-element")
    await eel.save_gui_element(gui_elements_main.data)()
    for (i = 0; i < t_gui_elements.length; i++) {
        const akt = t_gui_elements[i]
        await eel.save_gui_element(akt.data)()
    }
    await eel.save()()
}

async function export_gui_elements() {
    await eel.export_to_cpp()()
}


// load or create GUI-Elements

function load_window(p_attributes) {
    gui_elements_main.data = p_attributes

    // wendet die window_attribute an
    gui_elements_main.style.width = gui_elements_main.data.size_x + "px"
    gui_elements_main.style.height = gui_elements_main.data.size_y + "px"
    gui_elements_main.style.backgroundColor = "#" + gui_elements_main.data.background_color

    // schreibt die Window_attribute in den window-attribut-editor
    window_attributes.id.textContent = gui_elements_main.data.id
    window_attributes.name.value = gui_elements_main.data.name
    window_attributes.text.value = gui_elements_main.data.text
    window_attributes.size_x.value = gui_elements_main.data.size_x
    window_attributes.size_y.value = gui_elements_main.data.size_y
    window_attributes.text_color.value = gui_elements_main.data.text_color
    window_attributes.background_color.value = gui_elements_main.data.background_color
    window_attributes.event_create.checked = gui_elements_main.data.event_create
    window_attributes.event_destroy.checked = gui_elements_main.data.event_destroy
    window_attributes.event_paint.checked = gui_elements_main.data.event_paint
    window_attributes.event_resize.checked = gui_elements_main.data.event_resize
    window_attributes.event_mouse_click.checked = gui_elements_main.data.event_mouse_click
    window_attributes.event_mouse_move.checked = gui_elements_main.data.event_mouse_move
}

function load_gui_element(p_origin_element, p_attributes) {
    // clont das origin-Element
    t_neu_element = p_origin_element.cloneNode(true)

    t_neu_element.classList.add("gui-element")

    t_neu_element.id = "gui-element-" + p_attributes.id

    t_neu_element.data = p_attributes

    // Wendet die Attribute an
    if (p_attributes.type == "checkbox") {
        t_neu_element.children[1].textContent = p_attributes.text
        t_neu_element.children[0].checked = p_attributes.checked
    }
    else if (p_attributes.type == "canvas" || p_attributes.type == "timer")
        ;
    else
        t_neu_element.textContent = p_attributes.text
    t_neu_element.style.transform = "translate(" + p_attributes.pos_x + "px, " + p_attributes.pos_y + "px)"
    t_neu_element.style.width = p_attributes.size_x + "px"
    t_neu_element.style.height = p_attributes.size_y + "px"
    t_neu_element.style.color = "#" + p_attributes.text_color
    t_neu_element.style.backgroundColor = "#" + p_attributes.background_color

    gui_elements_main.append(t_neu_element)

    // added den Event-Listener
    t_neu_element.addEventListener('mousedown', gui_element_mousedown_event, false)

    return t_neu_element
}

function create_new_element(p_origin_element, p_attributes, p_x, p_y, p_menubar_element) {
    const t_neu_element = load_gui_element(p_origin_element, p_attributes)

    start_move_element(t_neu_element, p_x, p_y, p_menubar_element)

    set_gui_element_translation_from_abs_coords(t_neu_element, p_x, p_y)

    set_active_gui_element(t_neu_element)

    return t_neu_element
}


// GUI-MOVE-Methods

function start_move_element(p_element, p_mouseX, p_mouseY, p_offset_element_override = null) {
    if (p_offset_element_override == null)
        p_offset_element_override = p_element
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


// Active-Element-Attribut-Editor-Element

function set_active_gui_element(p_element) {
    if (g_active_gui_element != null)
        g_active_gui_element.classList.remove("active-gui-element")
    g_active_gui_element = p_element
    g_active_gui_element.classList.add("active-gui-element")

    // setzt aktuelle data Werte in den Element-Attribut-Editor
    element_attributes.id.textContent = g_active_gui_element.data.id
    element_attributes.name.value = g_active_gui_element.data.name
    element_attributes.text.value = g_active_gui_element.data.text
    element_attributes.pos_x.value = g_active_gui_element.data.pos_x
    element_attributes.pos_y.value = g_active_gui_element.data.pos_y
    element_attributes.size_x.value = g_active_gui_element.data.size_x
    element_attributes.size_y.value = g_active_gui_element.data.size_y
    element_attributes.text_color.value = g_active_gui_element.data.text_color
    element_attributes.background_color.value = g_active_gui_element.data.background_color
    element_attributes.interval.value = g_active_gui_element.data.interval
    element_attributes.checked.checked = g_active_gui_element.data.checked
    element_attributes.enabled.checked = g_active_gui_element.data.enabled
    element_attributes.multiple_lines.checked = g_active_gui_element.data.multiple_lines
    element_attributes.event_pressed.checked = g_active_gui_element.data.event_pressed
    element_attributes.event_double_pressed.checked = g_active_gui_element.data.event_double_pressed
    element_attributes.event_hovered.checked = g_active_gui_element.data.event_hovered
    element_attributes.event_changed.checked = g_active_gui_element.data.event_changed

    // Blendet die Teile des Attribut-Editors aus, welche nicht für das aktuelle Element unterstützt wird.
    
    if (!(p_element.data.type == "timer")) {
        element_attributes.event_section.style.display = ""
        element_attributes.background_color_section.style.display = ""
    }
    else {
        element_attributes.event_section.style.display = "none"
        element_attributes.background_color_section.style.display = "none"
    }

    if (p_element.data.type == "button" || p_element.data.type == "label" || p_element.data.type == "edit" || p_element.data.type == "checkbox") {
        element_attributes.text_section.style.display = ""
        element_attributes.text_color_section.style.display = ""
    }
    else {
        element_attributes.text_section.style.display = "none"
        element_attributes.text_color_section.style.display = "none"
    }

    if (p_element.data.type == "button" || p_element.data.type == "label" || p_element.data.type == "edit" || p_element.data.type == "checkbox" || p_element.data.type == "canvas")
        element_attributes.event_hovered_section.style.display = ""
    else
        element_attributes.event_hovered_section.style.display = "none"

    if (p_element.data.type == "button")
    {
        element_attributes.event_pressed_section.style.display = ""
        element_attributes.event_double_pressed_section.style.display = ""
    }
    else
    {
        element_attributes.event_pressed_section.style.display = "none"
        element_attributes.event_double_pressed_section.style.display = "none"
    }

    if (p_element.data.type == "edit" || p_element.data.type == "checkbox")
        element_attributes.event_changed_section.style.display = ""
    else
        element_attributes.event_changed_section.style.display = "none"

    if (p_element.data.type == "edit")
        element_attributes.multiple_lines_section.style.display = ""
    else
        element_attributes.multiple_lines_section.style.display = "none"

    if (p_element.data.type == "checkbox")
        element_attributes.checked_section.style.display = ""
    else
        element_attributes.checked_section.style.display = "none"

    if (p_element.data.type == "timer") {
        element_attributes.enabled_section.style.display = ""
        element_attributes.interval_section.style.display = ""
    }
    else {
        element_attributes.enabled_section.style.display = "none"
        element_attributes.interval_section.style.display = "none"
    }

    element_attributes.inner.style.visibility = "visible"
}

function reset_active_gui_element() {
    if (g_active_gui_element != null)
        g_active_gui_element.classList.remove("active-gui-element")
    element_attributes.inner.style.visibility = ""
    g_active_gui_element = null
}


// Element-Attribut-Change-Events. Wird ausgeführt, wenn ein Wert im Element-Attribut-Editor geändert wird.

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
        if (g_active_gui_element.data.type == "checkbox")
            g_active_gui_element.children[1].textContent = "undefined"
        else
            g_active_gui_element.textContent = "undefined"
    else {
        if (g_active_gui_element.data.type == "checkbox")
            g_active_gui_element.children[1].textContent = element_attributes.text.value
        else
            g_active_gui_element.textContent = element_attributes.text.value
    }
}

function attribut_set_pos_x() {
    if (isNaN(element_attributes.pos_x.value)) {
        element_attributes.pos_x.value = g_active_gui_element.data.pos_x
        return;
    }
    g_active_gui_element.data.pos_x = Math.round(Number(element_attributes.pos_x.value))
    set_gui_element_translation(g_active_gui_element, g_active_gui_element.data.pos_x, g_active_gui_element.data.pos_y)
}

function attribut_set_pos_y() {
    if (isNaN(element_attributes.pos_y.value)) {
        element_attributes.pos_y.value = g_active_gui_element.data.pos_y
        return;
    }
    g_active_gui_element.data.pos_y = Math.round(Number(element_attributes.pos_y.value))
    set_gui_element_translation(g_active_gui_element, g_active_gui_element.data.pos_x, g_active_gui_element.data.pos_y)
}

function attribut_set_size_x() {
    if (isNaN(element_attributes.size_x.value)) {
        element_attributes.size_x.value = g_active_gui_element.data.size_x
        return;
    }
    g_active_gui_element.data.size_x = Math.round(Number(element_attributes.size_x.value))
    g_active_gui_element.style.width = g_active_gui_element.data.size_x + "px"
    reprocess_element_translation(g_active_gui_element)
}

function attribut_set_size_y() {
    if (isNaN(element_attributes.size_y.value)) {
        element_attributes.size_y.value = g_active_gui_element.data.size_y
        return;
    }
    g_active_gui_element.data.size_y = Math.round(Number(element_attributes.size_y.value))
    g_active_gui_element.style.height = g_active_gui_element.data.size_y + "px"
    reprocess_element_translation(g_active_gui_element)
}

function attribut_set_text_color() {
    g_active_gui_element.data.text_color = element_attributes.text_color.value
    g_active_gui_element.style.color = "#" + g_active_gui_element.data.text_color
}

function attribut_set_background_color() {
    g_active_gui_element.data.background_color = element_attributes.background_color.value
    g_active_gui_element.style.backgroundColor = "#" + g_active_gui_element.data.background_color
}

function attribut_set_interval() {
    g_active_gui_element.data.interval = element_attributes.interval.value
}

function attribut_set_multiple_lines() {
    g_active_gui_element.data.multiple_lines = element_attributes.multiple_lines.checked
}

function attribut_set_checked() {
    g_active_gui_element.data.checked = element_attributes.checked.checked
    g_active_gui_element.children[0].checked = g_active_gui_element.data.checked
}

function attribut_set_enabled() {
    g_active_gui_element.data.enabled = element_attributes.enabled.checked
    g_active_gui_element.children[0].enabled = g_active_gui_element.data.enabled
}

function attribut_set_event_pressed() {
    g_active_gui_element.data.event_pressed = element_attributes.event_pressed.checked
}

function attribut_set_event_double_pressed() {
    g_active_gui_element.data.event_double_pressed = element_attributes.event_double_pressed.checked
}

function attribut_set_event_hovered() {
    g_active_gui_element.data.event_hovered = element_attributes.event_hovered.checked
}

function attribut_set_event_changed() {
    g_active_gui_element.data.event_changed = element_attributes.event_changed.checked
}


// Window-Attribut-Change-Events. Wird ausgeführt, wenn ein Wert im Window-Attribut-Editor geändert wird.

function window_set_name() {
    gui_elements_main.data.name = window_attributes.name.value
}

function window_set_text() {
    gui_elements_main.data.name = window_attributes.text.value
}

function window_set_size_x() {
    if (isNaN(window_attributes.size_x.value)) {
        window_attributes.size_x.value = gui_elements_main.data.size_x
        return;
    }
    gui_elements_main.data.size_x = Math.round(Number(window_attributes.size_x.value))
    gui_elements_main.style.width = gui_elements_main.data.size_x + "px"
    reprocess_all_elements_translation();
}

function window_set_size_y() {
    if (isNaN(window_attributes.size_y.value)) {
        window_attributes.size_y.value = gui_elements_main.data.size_y
        return;
    }
    gui_elements_main.data.size_y = Math.round(Number(window_attributes.size_y.value))
    gui_elements_main.style.height = gui_elements_main.data.size_y + "px"
    reprocess_all_elements_translation();
}

function window_set_text_color() {
    gui_elements_main.data.text_color = window_attributes.text_color.value
}

function window_set_background_color() {
    gui_elements_main.data.background_color = window_attributes.background_color.value
    gui_elements_main.style.backgroundColor = "#" + gui_elements_main.data.background_color
}

function window_set_event_create() {
    gui_elements_main.data.event_create = window_attributes.event_create.checked
}

function window_set_event_destroy() {
    gui_elements_main.data.event_destroy = window_attributes.event_destroy.checked
}

function window_set_event_paint() {
    gui_elements_main.data.event_paint = window_attributes.event_paint.checked
}

function window_set_event_resize() {
    gui_elements_main.data.event_resize = window_attributes.event_resize.checked
}

function window_set_event_mouse_click() {
    gui_elements_main.data.event_mouse_click = window_attributes.event_mouse_click.checked
}

function window_set_event_mouse_move() {
    gui_elements_main.data.event_mouse_move = window_attributes.event_mouse_move.checked
}



// Blendet das license_window ein.
function show_license_window() {
    getElement("license-window-main-outer").style.display = "flex"
    getElement("license-window-shadow").style.display = "block"
}

// Blendet das license_window aus.
function hide_license_window() {
    getElement("license-window-main-outer").style.display = ""
    getElement("license-window-shadow").style.display = ""
}