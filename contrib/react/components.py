from django.http import HttpRequest
from reactpy import component, html, use_state, event

from .views import form_view, csrf


@component
def Tab(display_text: str, selected: str, set_selected):
    def handle_click(event):
        set_selected(display_text)

    attributes = {"on_click": handle_click, "class_name": "tab tab-bordered"}

    if selected == display_text:
        attributes["class_name"] += " tab-active"

    return html.a(attributes, display_text)


@component
def Tabs(selected: str, set_selected):
    return html.div(
        {
            "class_name": "tabs",
        },
        Tab("Alvos", selected, set_selected),
        Tab("Email", selected, set_selected),
        Tab("Envio", selected, set_selected),
        Tab("Agradecimento", selected, set_selected),
        Tab("Pós-ação", selected, set_selected),
    )


@component
def Panels(selected: str):
    data, set_data = use_state({})

    @event(prevent_default=True)
    async def handle_submit(event):
        new_data = data.copy()
        new_data[selected] = {}
        for x in event["target"]["elements"]:
            # TODO: Muito especifico, entender como melhorar captura do evento
            if x['name'] == "sharing":
                values = new_data[selected].get(x['name'], [])
                values.append(x['value'])
                
                new_data[selected][x['name']] = values
            else:
                new_data[selected][x['name']] = x['value']

        print("new_data", new_data)
        set_data(new_data)

    request = HttpRequest()

    return html.div(
        {"class_name": "py-8"},
        html.form(
            {"on_submit": handle_submit, "method": "POST", "novalidate": True},
            csrf(),
            form_view(request, selected, data.get(selected, None)),
            html.button({"type": "submit"}, "Salvar"),
        ),
    )


@component
def SettingsPage():
    selected, set_selected = use_state("Alvos")

    return html.div(Tabs(selected, set_selected), Panels(selected))
