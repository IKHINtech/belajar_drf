from os import name
from django.urls import path
from rest_framework import views
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from polls.models import Choice
from rest_framework.authtoken import views
# Using Native Django
from .views import polls_list, polls_detail

# Using APIViews
from .apiviews import PollList, PollDetail, ChoiceList, CreateVote, PollViewSet, UserCreate, LoginView

router = DefaultRouter()
router.register('polls', PollViewSet, basename='polls' )

urlpatterns = [

    path("polls/", PollList.as_view(), name="polls_list"),
    path("polls/<int:pk>", PollDetail.as_view(), name="polls_detail"),
    path("choices/", ChoiceList.as_view(), name="chioce_list"),
    path("vote/", CreateVote.as_view(), name="create_vote"),
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),
    path("users/", UserCreate.as_view(), name='user_create'),
    path("login/", views.obtain_auth_token, name='login')
    
]
# urlpatterns+= router.urls