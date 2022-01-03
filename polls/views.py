from django.http.response import JsonResponse
from django.shortcuts import get_list_or_404, render
from django.urls.conf import re_path

from polls.models import Poll

def polls_list(request):
    MAX_OBJECTS = 20
    polls = Poll.objects.all()[:MAX_OBJECTS]
    data = {"results":list(polls.values("question", "create_by__username", "pub_date"))}
    return JsonResponse(data)

def polls_detail(request, pk):
    poll = get_list_or_404(Poll, pk=pk)
    data = {"results":{
        "questions":poll.question,
        "created_by": poll.created_by.username,
        "pub_date": poll.pub_date
    }}
    return JsonResponse(data)


# Create your views here.
