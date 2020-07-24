from django.shortcuts import render
from .forms import *
from django.core import serializers
from django.http import JsonResponse


# Create your views here.
from django.http import HttpResponse
def home(request):
    form = searchForm()
    
    return render(request,'index.html', {'form': form})


def answerPOST(request):
    if request.is_ajax() and request.method=="POST":
            form = searchForm(request.POST)
            if form.is_valid():
                instance = form.cleaned_data
                question = instance.get("question")
                answer = {'question': instance.get("question"),'answer':'younes'}
                # serialize in new friend object in json
               # ser_instance = serializers.serialize('json',answer)
                # send to client side.
                return JsonResponse({"instance": answer}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error":""},status=400)