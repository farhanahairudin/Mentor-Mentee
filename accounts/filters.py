import django_filters
from django_filters import DateFilter, CharFilter, RangeFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name='date_created', lookup_expr='gte')
	end_date = DateFilter(field_name='date_created', lookup_expr='lte')
	note = CharFilter(field_name='note', lookup_expr='icontains') #icontain = ignore case sensitivity

	class Meta:
		model = Order
		fields = '__all__'
		exclude = ['customer', 'date_created']

class MentorFilter(django_filters.FilterSet):
	CGPA = RangeFilter()

	class Meta:
		model = Mentor
		fields = ['faculty', 'department', 'CGPA']
		
class GoalFilter(django_filters.FilterSet):
	class Meta:
		model = Goal
		fields = ['title', 'category', 'status']

class SessionFilter(django_filters.FilterSet):
	class Meta:
		model = Session
		fields = ['name', 'setup_date', 'location', 'status']

class TaskFilter(django_filters.FilterSet):
	class Meta:
		model = Task
		fields = ['task_title', 'subject', 'status']

class AdFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="publish", lookup_expr='gte')
	end_date = DateFilter(field_name="publish", lookup_expr='lte')
	# description = CharFilter(field_name='description', lookup_expr='icontains')

	class Meta:
		model = Ad
		fields = '__all__'
		exclude = ['mentee', 'description', 'publish']

class AdFilter2(django_filters.FilterSet):
	start_date = DateFilter(field_name="publish", lookup_expr='gte')
	end_date = DateFilter(field_name="publish", lookup_expr='lte')
	# description = CharFilter(field_name='description', lookup_expr='icontains')

	class Meta:
		model = Ad2
		fields = '__all__'
		exclude = ['mentor', 'description', 'publish']

class ResultFilter(django_filters.FilterSet):
	class Meta:
		model = Result
		fields = ['semester', 'subject', 'grade', 'types']


class QuizzesFilter(django_filters.FilterSet):
	class Meta:
		model = Quizzes
		fields = ['title']

class QuestionFilter(django_filters.FilterSet):
	class Meta:
		model = Question
		fields = ['title', 'difficulty']