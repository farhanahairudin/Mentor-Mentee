from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import Quiz, RandomQuestionTopic, StartQuiz

urlpatterns = [
	path('register/', views.registerPage, name='register'),
	path('register_mentor/', views.registerMentor, name='register_mentor'),
	path('register_mentee/', views.registerMentee, name='register_mentee'),
	path('login/', views.loginPage, name='login'),
	path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),
    path('mentor/', views.mentorPage, name='mentor-page'),
    path('mentee/', views.menteePage, name='mentee-page'),
    
    path('mentor_account/', views.accountSettingsMentor, name='mentor_account'),
    path('mentee_account/', views.accountSettingsMentee, name='mentee_account'),

    path('match_mentor/', views.matchMentor, name='match-mentor'),
    path('delete_match/<str:pk>', views.deleteMatch, name='delete_match'),

    path('mentee_modules/', views.menteeModules, name='mentee_modules'),
    path('mentor_modules/', views.mentorModules, name='mentor_modules'),

    path('goal_page/<str:pk>', views.mentee, name='goal_page'),
    path('create_goal/<str:pk>', views.createGoal, name='create_goal'),
    path('update_goal/<str:pk>', views.updateGoal, name='update_goal'),
    path('delete_goal/<str:pk>', views.deleteGoal, name='delete_goal'),
    path('view_goal/<str:pk>', views.viewGoal, name='view_goal'),

    path('mentor_sess/<str:pk>', views.mentorSession, name='mentor_session'),
    path('setup_sess/<str:pk>', views.setupSession, name='create_session'),
    path('update_sess/<str:pk>', views.updateSession, name='update_session'),
    path('delete_sess/<str:pk>', views.deleteSession, name='delete_session'),
    path('book_sess/<str:pk>', views.bookSession, name='book_session'),
    path('mentee_schedule/<str:pk>', views.menteeSchedule, name='mentee_schedule'),
    path('mentor_schedule/<str:pk>', views.mentorSchedule, name='mentor_schedule'),



    path('mentor_task/<str:pk>', views.mentorTask, name='mentor_task'),
    path('create_task/<str:pk>', views.createTask, name='create_task'),
    path('delete_task/<str:pk>/', views.deleteTask, name="delete_task"),
    path('update_task/<str:pk>', views.updateTask, name='update_task'),
    path('view_task/<str:pk>', views.viewTask, name='view_task'),

    path('ads/', views.ads, name="ads"),
    path('user_ad/<str:pk>/', views.userAd, name="user_ad"),
    path('create_ad/<str:pk>/', views.createAd, name="create_ad"),
    path('update_ad/<str:pk>/', views.updateAd, name="update_ad"),
    path('delete_ad/<str:pk>/', views.deleteAd, name="delete_ad"),

    path('ads2/', views.ads2, name="ads2"),
    path('user_ad2/<str:pk>/', views.userAd2, name="user_ad2"),
    path('create_ad2/<str:pk>/', views.createAd2, name="create_ad2"),
    path('update_ad2/<str:pk>/', views.updateAd2, name="update_ad2"),
    path('delete_ad2/<str:pk>/', views.deleteAd2, name="delete_ad2"),


    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
    path('create_result/<str:pk>', views.createResult, name='create_result'),
    path('update_result/<str:pk>', views.updateResult, name='update_result'),
    path('delete_result/<str:pk>', views.deleteResult, name='delete_result'),

    path('quiz/', Quiz.as_view(), name='quiz'),
    path('mentor_quiz/<str:pk>/', views.mentorQuiz, name="mentor_quiz"),
    path('quiz_details/<str:pk>/', views.quizDetails, name='quiz_details'),

    path('create_quiz/<str:pk>/', views.createQuiz, name="create_quiz"),
    path('update_quiz/<str:pk>/', views.updateQuiz, name="update_quiz"),
    path('delete_quiz/<str:pk>/', views.deleteQuiz, name="delete_quiz"),

    path('create_question/<str:pk>/', views.createQuestion, name="create_question"),
    path('update_question/<str:pk>/', views.updateQuestion, name="update_question"),
    path('delete_question/<str:pk>/', views.deleteQuestion, name="delete_question"),

    path('create_answer/<str:pk>/', views.createAnswer, name="create_answer"),
    path('update_answer/<str:pk>/', views.updateAnswer, name="update_answer"),
    path('view_answer/<str:pk>/', views.viewAnswer, name="view_answer"),
    path('delete_answer/<str:pk>/', views.deleteAnswer, name="delete_answer"),
    
    path('random/<str:topic>/', RandomQuestionTopic.as_view(), name='RandomQuestionTopic'),
    path('start/<str:title>/', StartQuiz.as_view(), name='quiz'),



    path('product/', views.product, name='products'),
    path('customer/<str:pk>', views.customer, name='customer'), #dynamic url


    # path('mentor_list/', views.mentor, name='mentor-list'),
    
    path('create_order/<str:pk>', views.createOrder, name='create_order'),
    path('update_order/<str:pk>', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>', views.deleteOrder, name='delete_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)