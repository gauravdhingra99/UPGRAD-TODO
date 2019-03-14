from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from rest_framework import generics
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required


def sendmail(request):
	email = EmailMessage('Subject', 'Body', to=['def@domain.com'])
	email.send()

def index(request):
    return render(request, 'tasks/signup.html', {})

@login_required(login_url='/welcome')
def profile(request):
	from datetime import datetime, timedelta
	d = datetime.today() - timedelta(days=1)
	duetodo=TodoList.objects.filter(created_by=request.user,due_date=d)
	print(duetodo)
	print(request.user.email)
	for i in duetodo:
		email = EmailMessage('Schedule Reminder', 'Your '+i.title+' need to be completed its due_date is '+i.due_date.strftime('%m/%d/%Y'), to=[request.user.email])
		email.send()

	cat=Category.objects.all().values()
	todos=TodoList.objects.filter(created_by=request.user).values()
	return render(request, 'tasks/profile1.html', {"cat":cat,"todos":todos})


@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


def complete_view(request):
	return render(request, 'tasks/emailconfirm.html', {})
    # return Response("Email account is activated")


class TodoCreateView(generics.CreateAPIView):
		queryset=TodoList.objects.all()
		serializer_class = TodoSerializer

		def perform_create(self, serializer):
			print(self.request.data.get('category'))

			serializer.save(created_by=self.request.user)

class TodoRetrieveView(APIView):
	def get(self,request):
		print(request.query_params)
		title=request.query_params.get("title")
		if title:
			qs=TodoList.objects.filter(title__iexact=title,created_by=request.user)
			if qs.exists():
				return Response({"data":qs.values('id','title','completed','created_by__username','created','due_date','category__name',)})
			else:
				return Response({"data":"NO TODOS WIHT THAT TITLE"})
		return Response({"data":TodoList.objects.filter(created_by=request.user).values('id','title','completed','created_by__username','created','due_date','category__name',)})

class TodoUpdateView(APIView):
	def get_queryset(self, pk):
		return TodoList.objects.filter(pk=pk,created_by=self.request.user)
	def put(self, request,pk):
		todo = self.get_queryset(pk)
		print('dwdw',todo)
		if not todo.exists():
			return Response({"error":"no pk corresponsding"}, status=status.HTTP_400_BAD_REQUEST)

		serializer = TodoSerializer(todo[0], data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDeleteView(APIView):
	def get_queryset(self, pk):
		return TodoList.objects.filter(pk=pk,created_by=self.request.user)
	
	def delete(self, request,pk):
		todo = self.get_queryset(pk)
		print('dwdw',todo)
		if not todo.exists():
			return Response({"error":"no pk corresponsding"}, status=status.HTTP_400_BAD_REQUEST)
		todo[0].delete()
		return Response("deleted successfully", status=200)

    






