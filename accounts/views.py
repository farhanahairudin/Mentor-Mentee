from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.generic.list import ListView

from django.core.files.storage import FileSystemStorage

import os
from io import BytesIO
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from django.views import View 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .serializers import QuizSerializer, RandomQuestionSerializer, AnswerSerializer

# Create your views here.
#OrderForm, CreateUserForm, CustomerForm, MentorForm, MenteeForm, MatchForm, UpdateGoal, SetupSession
from .models import *
from .forms import *
from .filters import *
from .decorators import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
def registerPage(request):
	context = {}
	return render(request, 'accounts/register.html', context) 


@unauthenticated_user
def registerMentor(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			
			group = Group.objects.get(name='mentor')
			user.groups.add(group)
			Mentor.objects.create(
				user=user,
				name=user.username,
				email=user.email,
				)


			messages.success(request, 'Account was created for Mentor ' + username)
				
			return redirect('login')

	context = {'form': form}
	return render(request, 'accounts/register_mentor.html', context)


@unauthenticated_user
def registerMentee(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			
			group = Group.objects.get(name='mentee')
			user.groups.add(group)
			Mentee.objects.create(
				user=user,
				name=user.username,
				email=user.email,
				)


			messages.success(request, 'Account was created for Mentee ' + username)
				
			return redirect('login')

	context = {'form':form}
	return render(request, 'accounts/register_mentee.html', context)


@unauthenticated_user
def loginPage(request):
			
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username or Password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders': orders, 'customers': customers, 'total_orders': total_orders, 
	'delivered': delivered, 'pending': pending}	

	return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def mentorPage(request):
	matchs = request.user.mentor.match_set.all()
	# print('MATCHS:', matchs)

	context = {'matchs': matchs}
	return render(request, 'accounts/mentor.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentee'])
def menteePage(request):
	matchs = request.user.mentee.match_set.all()
	# print('MATCHS:', matchs)

	context = {'matchs': matchs}
	return render(request, 'accounts/mentee.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def accountSettingsMentor(request):
	mentor = request.user.mentor
	form = MentorForm(instance=mentor)

	if request.method == 'POST':
		form = MentorForm(request.POST, request.FILES, instance=mentor)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings_mentor.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentee'])
def accountSettingsMentee(request):
	mentee = request.user.mentee
	form = MenteeForm(instance=mentee)
	results = mentee.result_set.all() 

	myFilter = ResultFilter(request.GET, queryset=results)
	results = myFilter.qs

	if request.method == 'POST':
		form = MenteeForm(request.POST, request.FILES, instance=mentee)
		if form.is_valid():
			form.save()


	context = {'form':form, 'results':results, 'myFilter':myFilter, 'mentee':mentee}
	return render(request, 'accounts/account_settings_mentee.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentee'])
def matchMentor(request):
	# mentee = request.user.mentee
	# form = MatchForm(instance=mentee)
	mentee = request.user.mentee
	form = MatchForm(initial={'mentee':mentee}) #set customer name as initial

	mentors = Mentor.objects.all()
	if request.method == 'POST':
		# print('Printing POST:', request.POST)
		# form = OrderForm(request.POST)
		form = MatchForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/') #after submit, redirect to the dashboard

	myFilter = MentorFilter(request.GET, queryset=mentors)
	mentors = myFilter.qs

	context = {'mentors' : mentors, 'myFilter':myFilter, 'form':form, 'mentee':mentee}
	return render(request, 'accounts/matching.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentee','mentor'])
def deleteMatch(request, pk):
	match = Match.objects.get(id=pk)
	if request.method == 'POST':
		match.delete()
		return redirect('/')

	context = {'item':match}
	return render(request, 'accounts/delete_match.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def mentee(request, pk):
	match = Match.objects.get(id=pk)

	goals = match.goal_set.all() #order_set ni tgk balik relationship parent child tu
	goal_count = goals.count() #ejaan orders based on atas 
	completed = goals.filter(status='Completed').count()
	active = goals.filter(status='Active').count()
	perc = round(1)

	if goal_count == 0:
		perc = round(0)
	elif goal_count > 0:
		perc = round(completed * 100 / goal_count)
	# perc = round(completed * 100)
	# round_perc = round(perc)

	myFilter = GoalFilter(request.GET, queryset=goals)
	goals = myFilter.qs

	context = {'match':match, 'goals': goals, 'goal_count': goal_count, 'myFilter': myFilter, 'completed': completed, 'active': active, 'perc': perc}
	return render(request, 'accounts/mentee_goal.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['mentee'])
def menteeModules(request):
	matchs = request.user.mentee.match_set.all()
	# print('MATCHS:', matchs)

	context = {'matchs': matchs}
	return render(request, 'accounts/modules.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def mentorModules(request):
	matchs = request.user.mentor.match_set.all()
	# print('MATCHS:', matchs)

	context = {'matchs': matchs}
	return render(request, 'accounts/mentor_modules.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def createGoal(request, pk): 
	match = Match.objects.get(id=pk)
	form = UpdateGoal(initial={'match':match}) 

	if request.method == 'POST':
		form = UpdateGoal(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form, 'item':match}
	return render(request, 'accounts/create_goal.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def updateGoal(request, pk):

	goal = Goal.objects.get(id=pk)
	form = UpdateGoal(instance=goal) #pre-filled the form
	
	if request.method == 'POST':
		form = UpdateGoal(request.POST, instance=goal)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/create_goal.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def deleteGoal(request, pk):
	goal = Goal.objects.get(id=pk)
	if request.method == 'POST':
		goal.delete()
		return redirect('/')

	context = {'item':goal}
	return render(request, 'accounts/delete_goal.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentee'])
def viewGoal(request, pk):
	match = Match.objects.get(id=pk)

	goals = match.goal_set.all() #order_set ni tgk balik relationship parent child tu
	goal_count = goals.count() #ejaan orders based on atas
	completed = goals.filter(status='Completed').count()
	active = goals.filter(status='Active').count()
	perc = completed * 100 / goal_count
	round_perc = round(perc)

	myFilter = GoalFilter(request.GET, queryset=goals)
	goals = myFilter.qs
	
	context = {'match':match, 'goals': goals, 'goal_count': goal_count, 'myFilter':myFilter, 'completed':completed, 'active':active, 'perc': perc, 'round_perc': round_perc}
	return render(request, 'accounts/view_goal.html', context)



#sama dengan create goal
@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def setupSession(request, pk):
	match = Match.objects.get(id=pk)
	form = SetupSession(initial={'match':match})

	if request.method == 'POST':
		form = SetupSession(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'item': match, 'form': form}
	return render(request, 'accounts/create_sessions.html', context)



#sama dengan mentee
@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def mentorSession(request, pk):
	match = Match.objects.get(id=pk)

	sessions = match.session_set.all() #order_set ni tgk balik relationship parent child tu
	session_count = sessions.count() #ejaan orders based on atas 

	myFilter = SessionFilter(request.GET, queryset=sessions)
	sessions = myFilter.qs

	context = {'match':match, 'sessions': sessions, 'session_count': session_count,'myFilter': myFilter}
	return render(request, 'accounts/mentor_session.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentee'])
def updateSession(request, pk):

	session = Session.objects.get(id=pk)
	form = UpdateSession(instance=session) #pre-filled the form
	
	if request.method == 'POST':
		form = UpdateSession(request.POST, instance=session)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/create_sessions.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def deleteSession(request, pk):
	session = Session.objects.get(id=pk)
	if request.method == 'POST':
		session.delete()
		return redirect('/')

	context = {'item':session}
	return render(request, 'accounts/delete_session.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentee'])
def bookSession(request, pk):
	match = Match.objects.get(id=pk)

	sessions = match.session_set.all() #order_set ni tgk balik relationship parent child tu
	session_count = sessions.count() #ejaan orders based on atas 

	myFilter = SessionFilter(request.GET, queryset=sessions)
	sessions = myFilter.qs

	context = {'match':match, 'sessions': sessions, 'session_count': session_count, 'myFilter':myFilter}
	return render(request, 'accounts/book_session.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentee'])
def menteeSchedule(request, pk):
	match = Match.objects.get(id=pk)

	sessions = match.session_set.all() #order_set ni tgk balik relationship parent child tu
	accepted_sess = sessions.filter(status='Accepted')
	accepted = sessions.filter(status='Accepted').count()

	context = {'match':match, 'sessions': sessions, 'accepted_sess': accepted_sess, 'accepted': accepted}
	return render(request, 'accounts/mentee_schedule.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def mentorSchedule(request, pk):
	match = Match.objects.get(id=pk)

	sessions = match.session_set.all() #order_set ni tgk balik relationship parent child tu
	accepted_sess = sessions.filter(status='Accepted')
	accepted = sessions.filter(status='Accepted').count()

	context = {'match':match, 'sessions': sessions, 'accepted_sess': accepted_sess, 'accepted': accepted}
	return render(request, 'accounts/mentor_schedule.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def mentorTask(request, pk):
	match = Match.objects.get(id=pk)

	tasks = match.task_set.all() #order_set ni tgk balik relationship parent child tu
	task_count = tasks.count() #ejaan orders based on atas 
	completed = tasks.filter(status='Completed').count()
	pending = tasks.filter(status='Pending').count()
	# perc = round(completed * 100)

	# if task_count == 0:
	# 	perc = 0.0
	# else:
	# 	perc = round(completed * 100 / task_count)
	perc = round(1)

	if task_count == 0:
		perc = round(0)
	elif task_count > 0:
		perc = round(completed * 100 / task_count)
	

	myFilter = TaskFilter(request.GET, queryset=tasks)
	tasks = myFilter.qs

	context = {'match': match,'tasks':tasks, 'task_count': task_count, 'completed': completed, 'pending': pending, 'myFilter': myFilter, 'perc': perc}
	return render(request, 'accounts/task_mentor.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def createTask(request, pk): 
	match = Match.objects.get(id=pk)

	form = UpdateTask(initial={'match':match}) 

	if request.method == 'POST':

		form = UpdateTask(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form, 'match': match}
	
	return render(request, 'accounts/create_task.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def deleteTask(request, pk):
	task = Task.objects.get(id=pk)
	if request.method == "POST":
		task.delete()
		return redirect('/')

	context = {'item': task}
	return render(request, 'accounts/delete_task.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def updateTask(request, pk):
	task = Task.objects.get(id=pk)
	form = UpdateTask(instance=task)

	if request.method == 'POST':
		form = UpdateTask(request.POST, request.FILES, instance=task)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}

	return render(request, 'accounts/create_task.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentee'])
def viewTask(request, pk):
	# tasks = request.user.mentee.task_set.all()

	# total_tasks = tasks.count()
	# completed = tasks.filter(status='Completed').count()
	# pending = tasks.filter(status='Pending').count()

	match = Match.objects.get(id=pk)

	tasks = match.task_set.all() #order_set ni tgk balik relationship parent child tu
	task_count = tasks.count() #ejaan orders based on atas 
	completed = tasks.filter(status='Completed').count()
	pending = tasks.filter(status='Pending').count()
	# perc = round(completed * 100)

	# if task_count == 0:
	# 	perc = 0.0
	# else:
	# 	perc = round(completed * 100 / task_count)
	perc = round(1)

	if task_count == 0:
		perc = round(0)
	elif task_count > 0:
		perc = round(completed * 100 / task_count)
	

	myFilter = TaskFilter(request.GET, queryset=tasks)
	tasks = myFilter.qs
	


	context = {'match': match,'tasks':tasks, 'task_count': task_count, 'completed': completed, 'pending': pending, 'myFilter': myFilter, 'perc': perc}

	return render(request, 'accounts/view_task.html', context)


#-------------------MENTEE ADVERTISEMENT--------------------------------------------------------------------

@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor','mentee'])
def ads(request):
	ads = Ad.objects.all()
	ads2 = Ad2.objects.all()

	mentee = request.user.mentee

	myFilter = AdFilter2(request.GET, queryset=ads)
	ads = myFilter.qs

	context = {'ads': ads,'ads2': ads2, 'mentee':mentee, 'myFilter': myFilter}

	return render(request, 'accounts/ads.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor','mentee'])
def userAd(request, pk):
	mentee = Mentee.objects.get(id=pk)
	ads = mentee.ad_set.all()

	myFilter = AdFilter2(request.GET, queryset=ads)
	ads = myFilter.qs

	context = {'ads': ads, 'mentee':mentee, 'myFilter': myFilter}

	return render(request, 'accounts/user_ad.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor','mentee'])
def createAd(request, pk):
	mentee = Mentee.objects.get(id=pk)
	context = {'mentee':mentee}

	form = UpdateAd(initial={'mentee':mentee})

	if request.method == 'POST':
		form = UpdateAd(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/create_ad.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor','mentee'])
def updateAd(request, pk):
	ad = Ad.objects.get(id=pk)
	form = UpdateAd(instance=ad)

	if request.method == 'POST':
		form = UpdateAd(request.POST, instance=ad)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/create_ad.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor','mentee'])
def deleteAd(request, pk):
	ad = Ad.objects.get(id=pk)
	if request.method == "POST":
		ad.delete()
		return redirect('/')

	context = {'item':ad}
	return render(request, 'accounts/delete_ad.html', context)


#----------------MENTOR ADVERTISEMENT--------------------------------------------------------------------------

@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor','mentee'])
def ads2(request):
	ads = Ad.objects.all()
	ads2 = Ad2.objects.all()

	mentor = request.user.mentor

	myFilter = AdFilter(request.GET, queryset=ads)
	ads = myFilter.qs

	context = {'ads': ads,'ads2': ads2, 'mentor':mentor, 'myFilter': myFilter}

	return render(request, 'accounts/ads2.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor','mentee'])
def userAd2(request, pk):
	mentor = Mentor.objects.get(id=pk)
	ads = mentor.ad2_set.all()

	myFilter = AdFilter(request.GET, queryset=ads)
	ads = myFilter.qs

	context = {'ads': ads, 'mentor':mentor, 'myFilter': myFilter}

	return render(request, 'accounts/user_ad2.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor','mentee'])
def createAd2(request, pk):
	mentor = Mentor.objects.get(id=pk)
	context = {'mentor':mentor}

	form = UpdateAd2(initial={'mentor':mentor})

	if request.method == 'POST':
		form = UpdateAd2(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/create_ad.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor','mentee'])
def updateAd2(request, pk):
	ad = Ad2.objects.get(id=pk)
	form = UpdateAd2(instance=ad)

	if request.method == 'POST':
		form = UpdateAd2(request.POST, instance=ad)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/create_ad.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor','mentee'])
def deleteAd2(request, pk):
	ad = Ad2.objects.get(id=pk)
	if request.method == "POST":
		ad.delete()
		return redirect('/')

	context = {'item':ad}
	return render(request, 'accounts/delete_ad2.html', context)


#------------------------------RESULT----------------------------------------------------------------------------

@login_required(login_url='login')
@allowed_users(allowed_roles=['mentee'])
def createResult(request, pk): 

	mentee = Mentee.objects.get(id=pk)
	form = UpdateResult(initial={'mentee':mentee}) 

	if request.method == 'POST':
		form = UpdateResult(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form, 'item':mentee}
	return render(request, 'accounts/create_result.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentee'])
def updateResult(request, pk):

	result = Result.objects.get(id=pk)
	form = UpdateResult(instance=result) #pre-filled the form
	
	if request.method == 'POST':
		form = UpdateResult(request.POST, instance=result)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/create_result.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentee'])
def deleteResult(request, pk):

	result = Result.objects.get(id=pk)
	if request.method == 'POST':
		result.delete()
		return redirect('/')

	context = {'item':result}
	return render(request, 'accounts/delete_result.html', context)


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


#Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):

		mentee = request.user.mentee
		results = mentee.result_set.all() 

		context = {'results':results, 'mentee':mentee}

		pdf = render_to_pdf('accounts/pdf_template.html', context)
		return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):

		mentee = request.user.mentee
		results = mentee.result_set.all() 

		context = {'results':results, 'mentee':mentee}
		
		pdf = render_to_pdf('accounts/pdf_template.html', context)

		response = HttpResponse(pdf, content_type='application/pdf')
		# filename = "ResultReport%s.pdf" %("")
		content = "attachment;" 
		response['Content-Disposition'] = content
		return response

#--------------------QUIZ-----------------------------------------------------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def mentorQuiz(request, pk):
	# matchs = request.user.mentor.match_set.all()
	match = Match.objects.get(id=pk)

	quizzes = match.quizzes_set.all()
	# categorys = request.user.mentor.quizzes_set.all()
	# mentor = request.user.mentor

	myFilter = QuizzesFilter(request.GET, queryset=quizzes)
	quizzes = myFilter.qs

	context = {'match':match, 'quizzes':quizzes, 'myFilter':myFilter}

	return render(request, 'accounts/mentor_quiz.html', context)

class StartQuiz(APIView):

    def get(self, request, **kwargs):
        quiz = Quizzes.objects.filter(category__name=kwargs['title'])
        serializer = QuizSerializer(quiz, many=True)
        return Response(serializer.data)


class Quiz(generics.ListAPIView):

    serializer_class = QuizSerializer
    queryset = Quizzes.objects.all()


class RandomQuestionTopic(APIView):

    def get(self, request, format=None, **kwargs):
        question = Question.objects.filter(quiz__title=kwargs['topic']).order_by('?')[:1]
        serializer = RandomQuestionSerializer(question, many=True)
        return Response(serializer.data)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def createQuiz(request, pk):

	match = Match.objects.get(id=pk)

	form = UpdateQuiz(initial={'match':match})

	if request.method == 'POST':
		form = UpdateQuiz(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'match': match, 'form':form}
	return render(request, 'accounts/create_quiz.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def updateQuiz(request, pk):

	quiz = Quizzes.objects.get(id=pk)
	form = UpdateQuiz(instance=quiz)

	if request.method == 'POST':
		form = UpdateQuiz(request.POST, instance=quiz)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form, 'quiz': quiz}
	return render(request, 'accounts/create_quiz.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def deleteQuiz(request, pk):
	quiz = Quizzes.objects.get(id=pk)
	if request.method == "POST":
		quiz.delete()
		return redirect('/')

	context = {'item':quiz}
	return render(request, 'accounts/delete_quiz.html', context) 


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def quizDetails(request, pk):
	quiz = Quizzes.objects.get(id=pk)

	question = quiz.question_set.all()
	answer = Answer.objects.all()

	myFilter = QuestionFilter(request.GET, queryset=question)
	question = myFilter.qs

	context = {'quiz':quiz, 'question':question, 'answer':answer, 'myFilter': myFilter}

	return render(request, 'accounts/quiz_details.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def createQuestion(request, pk):
	quiz = Quizzes.objects.get(id=pk)
	context = {'quiz':quiz}

	form = UpdateQuestion(initial={'quiz':quiz})

	if request.method == 'POST':
		form = UpdateQuestion(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/create_question.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def updateQuestion(request, pk):
	question = Question.objects.get(id=pk)
	form = UpdateQuestion(instance=question)

	if request.method == 'POST':
		form = UpdateQuestion(request.POST, instance=question)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/create_question.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def deleteQuestion(request, pk):
	question = Question.objects.get(id=pk)
	if request.method == "POST":
		question.delete()
		return redirect('/')

	context = {'item':question}
	return render(request, 'accounts/delete_question.html', context) 


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def createAnswer(request, pk):

	question = Question.objects.get(id=pk)
	AnswerFormSet = inlineformset_factory(Question, Answer, fields=('answer_text', 'is_right'))
	formset = AnswerFormSet(queryset=Answer.objects.none(),instance=question)
	# form = UpdateAnswer(initial={'question':question})

	if request.method == 'POST':
		# form = UpdateAnswer(request.POST)
		formset = AnswerFormSet(request.POST, instance=question)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'question':question,'form':formset}
	return render(request, 'accounts/create_answer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def updateAnswer(request, pk):
	question = Question.objects.get(id=pk)
	# answer = question.answer_set.all()
	# answer = Answer.objects.get(id=pk)
	AnswerFormSet = inlineformset_factory(Question, Answer, fields=('answer_text', 'is_right'))
	formset = AnswerFormSet(instance=question)

	if request.method == 'POST':
		formset = AnswerFormSet(request.POST, instance=question)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/create_answer.html', context) 

@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def viewAnswer(request, pk):
	question = Question.objects.get(id=pk)
	answer = question.answer_set.all()
	# answer = Answer.objects.all()

	context = {'question':question,'answer':answer}
	return render(request, 'accounts/view_answer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['mentor'])
def deleteAnswer(request, pk):
	answer = Answer.objects.get(id=pk)
	if request.method == "POST":
		answer.delete()
		return redirect('/')

	context = {'item':answer}
	return render(request, 'accounts/delete_answer.html', context) 
#------------------------------------------------------------------------------------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products' : products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
	customer = Customer.objects.get(id=pk)

	orders = customer.order_set.all() #order_set ni tgk balik relationship parent child tu
	order_count = orders.count() #ejaan orders based on atas 

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders': orders, 'order_count':order_count, 'myFilter':myFilter}
	return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	# form = OrderForm(initial={'customer':customer}) #set customer name as initial
	if request.method == 'POST':
		# print('Printing POST:', request.POST)
		# form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/') #after submit, redirect to the dashboard

	context = {'formset':formset}
	return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order) #pre-filled the form
	
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)



# @login_required(login_url='login')
# @allowed_users(allowed_roles=['mentee','mentor'])
# def accountSettings(request):
# 	customer = request.user.customer
# 	form = CustomerForm(instance=customer)

# 	if request.method == 'POST':
# 		form = CustomerForm(request.POST, request.FILES, instance=customer)
# 		if form.is_valid():
# 			form.save()


# 	context = {'form':form}
# 	return render(request, 'accounts/account_settings.html', context)
