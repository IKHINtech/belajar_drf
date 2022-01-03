from django.urls import path

# Using Native Django
from .views import polls_list, polls_detail

# Using APIViews
from .apiviews import PollList, PollDetail

urlpatterns = [
    path("polls/", PollList.as_view(), name="polls_list"),
    path("polls/<int:pk>", PollDetail.as_view(), name="polls_detail"),
    
]