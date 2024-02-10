from django.shortcuts import render
from django.http import HttpResponse
from . import util
import markdown2
import numpy as np
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse



def index(request):
    param = request.GET.get('q', None)

    if(param in util.list_entries()):
        
        ##return HttpResponse(f"{name}!")
        return render(request, "encyclopedia/article.html", {
        "article": markdown2.markdown(util.get_entry(param)),
        "name": param
    })    
    if param:
        matching_entries = [entry for entry in util.list_entries() if param.lower() in entry.lower()]
        
        if matching_entries:
            # Display a list of entries that have param as substring
            return render(request, "encyclopedia/index.html", {
                "entries": matching_entries,
                "param": param
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def article(request, name):
    if(name in util.list_entries()):
        
        ##return HttpResponse(f"{name}!")
        return render(request, "encyclopedia/article.html", {
        "article": markdown2.markdown(util.get_entry(name)),
        "name": name
    })
    else:
        return HttpResponse("404")

def random(request):
    random_article =  np.random.choice(util.list_entries())

    return render(request, "encyclopedia/article.html", {
        "article": markdown2.markdown(util.get_entry(random_article)),
        "name": random_article
    })


def new(request):
    class NewArticleForm(forms.Form):
        title = forms.CharField(label="Title")
        content = forms.CharField(label="Content", widget=forms.Textarea)
    if request.method == "POST":
        form = NewArticleForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

    return render(request, "encyclopedia/new.html", {
        "form" : NewArticleForm()
    })


def edit(request, name):
    class NewArticleForm(forms.Form):
        content = forms.CharField(label="Content", widget=forms.Textarea)

    if name.capitalize() in util.list_entries() or name.lower() in util.list_entries() or name.upper() in util.list_entries():
        if request.method == "POST":
            form = NewArticleForm(request.POST)

            if form.is_valid():
                content = form.cleaned_data["content"]

                util.save_entry(name, content)

                # Redirect to the edited entry using reverse
                return HttpResponseRedirect(reverse(f'index'))
        else:
            return render(request, "encyclopedia/edit.html", {
                "article": util.get_entry(name),
                "name": name,
                "form": NewArticleForm(initial={'content': util.get_entry(name)})  # Include an empty form for GET requests
            })
    else:
        return HttpResponse(name)
