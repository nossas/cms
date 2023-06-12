from django.shortcuts import render
from reactpy_django.components import view_to_component

from .forms import TargetsForm, EmailForm, SendForm, ThankForm, PostActionForm


@view_to_component
def csrf(request):
    return render(request, "react/views/csrf.html")


form_dict = {
    "Alvos": TargetsForm,
    "Email": EmailForm,
    "Envio": SendForm,
    "Agradecimento": ThankForm,
    "Pós-ação": PostActionForm,
}


@view_to_component
def form_view(request, selected: str, data=None):
    FormClass = form_dict.get(selected, TargetsForm)

    if data:
        form = FormClass(data)
        # print("data", data)
        # tuple_fields = [
        #     (field_name, data.get(field_name, None))
        #     for field_name in FormClass.Meta.fields
        # ]

        # tuple_fields = list(filter(lambda x: x[1], tuple_fields))

        # form = FormClass(dict(tuple_fields))

        obj = form.save(commit=False)
        # import ipdb;ipdb.set_trace()
    else:
        form = FormClass()

    return render(request, "react/views/form.html", {"form": form})
