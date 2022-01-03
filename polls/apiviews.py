# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers

from .models import Poll, Choice
from .serializers import ChoiceSerializer, PollSerializer


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
