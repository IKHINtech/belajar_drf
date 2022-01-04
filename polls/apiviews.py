# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers, status, viewsets
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from .models import Poll, Choice
from .serializers import ChoiceSerializer, PollSerializer, VoteSerializer, UserSerializer


# apiview using ApiView
# class PollList(APIView):
#     def get(self, request):
#         polls = Poll.objects.all()[:20]
#         data = PollSerializer(polls, many=True).data
#         return Response(data=data)

# class PollDetail(APIView):
#     def get(self, req, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         data = PollSerializer(poll).data
#         return Response(data=data)

# class ChoiceList(APIView):
#     def get(self, req):
#         choice = Choice.objects.all()[:20]
#         data = ChoiceSerializer(choice, many=True).data
#         return Response(data)

# Apiview using generic

class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollDetail(generics.RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id= self.kwargs["pk"])
        return queryset
    serializer_class = ChoiceSerializer
    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("you can not create choice for this poll")
        return super().post(request, *args, **kwargs)

class CreateVote(generics.CreateAPIView):
    serializer_class = VoteSerializer

    def post(self, req, pk, choice_pk):
        voted_by = req.data.get("voted_by")
        data = {'choice':choice_pk, 'poll':pk, 'voted_by':voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    def destroy(self, req, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not req.user == poll.created_by:
            raise PermissionDenied("you can not delete this poll")
        return super().destroy(req, *args, **kwargs)

class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = ()
    def post(self, req,):
        username = req.data.get('username')
        password = req.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response({'error':"wrong credentials"}, status=status.HTTP_400_BAD_REQUEST)