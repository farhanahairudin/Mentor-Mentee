from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import *

from .models import *



class MentorForm(ModelForm):
	class Meta:
		model = Mentor
		fields = '__all__'
		exclude = ['user']

class MenteeForm(ModelForm):
	class Meta:
		model = Mentee
		fields = '__all__'
		exclude = ['user','note']

class MatchForm(ModelForm):
	class Meta:
		model = Match
		fields = ['mentee','mentor']

class UpdateGoal(ModelForm):
	class Meta:
		model = Goal
		fields = '__all__'


class SetupSession(ModelForm):
	class Meta:
		model = Session
		fields = ['match', 'name', 'setup_date', 'location']

		setup_date = forms.DateTimeField(input_formats = ('%m/%d/%Y %H:%M'))

class UpdateSession(ModelForm):
	class Meta:
		model = Session
		fields = ['status', 'note']


class UpdateTask(ModelForm):
	class Meta:
		model = Task
		fields = '__all__'

class UpdateAd(ModelForm):
	class Meta:
		model = Ad
		fields = '__all__'

class UpdateAd2(ModelForm):
	class Meta:
		model = Ad2
		fields = '__all__'

class UpdateResult(ModelForm):
	class Meta:
		model = Result
		fields = '__all__'

class UpdateCategory(ModelForm):
	class Meta:
		model = Category
		fields = '__all__'

class UpdateQuiz(ModelForm):
	class Meta:
		model = Quizzes
		fields = '__all__'

class UpdateQuestion(ModelForm):
	class Meta:
		model = Question
		fields = '__all__'
		exclude = ['is_active']

class UpdateAnswer(ModelForm):
	class Meta:
		model = Answer
		fields = '__all__'

class CreateUserForm(UserCreationForm):
	email = forms.EmailField()
	CGPA = forms.DecimalField(validators=[MinValueValidator(3.7)])

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2', 'CGPA']




#-------------------------------------------------------------------------------------------------------------
class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']


class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__' #use all field, kalau tak just ['products,customer']






