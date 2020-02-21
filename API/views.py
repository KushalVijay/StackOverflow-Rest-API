from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status
from .models import Question
from .serializer import QuestionSerializer
import requests
import json
from bs4 import BeautifulSoup
# Create your views here.
def index(request):
    return HttpResponse("Success")

class List(APIView):
    def get(self,request):
        queryset = Question.objects.all()
        serializer = QuestionSerializer(queryset,many=True)
        return Response(serializer.data)

    def post(self,request):
        pass

class QuestionAPI(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


def latest(request):
    try:
        res = requests.get("https://stackoverflow.com/questions")

        soup = BeautifulSoup(res.text, "html.parser")
        questions = soup.select(".question-summary")

        for que in questions:
            q = que.select_one('.question-hyperlink').getText()
            print(q)
            vote_count = que.select_one('.vote-count-post').getText()
            views = que.select_one('.views').attrs['title']
            tags = [i.getText() for i in (que.select('.post-tag'))]

            question = Question()
            question.question = q
            question.vote_count = vote_count
            question.views = views
            question.tags = tags

            question.save()
        return HttpResponse("Fetching Questions from StackOverFlow")
    except e as Exception:
        return HttpResponse(f"Failed {e}")



