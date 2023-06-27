from django.shortcuts import render

from .forms import ChatGPTForm
from .openai_client import answer_me


def chatgpt_view(request):
    form = ChatGPTForm()
    result = None

    if request.method == "POST":
        form = ChatGPTForm(data=request.POST)

        if form.is_valid():
            input_text = form.cleaned_data['input_text']
            result = answer_me(input_text)

    return render(request, "chatgpt/view.html", {"form": form, "result": result})