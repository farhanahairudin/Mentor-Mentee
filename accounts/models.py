from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _
#Classes that store database here

# Create your models here.
class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.jpg", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	
	#return name instead of customer 1 in database
	def __str__(self):
		return self.name


class Mentor(models.Model):

	FACULTY = (
			('Islamic Studies', 'Islamic Studies'), ('Malay Studies', 'Malay Studies'), ('Cultural', 'Cultural'),
			('Dentistry', 'Dentistry'), ('Education', 'Education'), ('Engineering', 'Engineering'),
			('Law', 'Law'), ('Medicine', 'Medicine'), ('Science', 'Science'),
			('Art & Social Sciences', 'Art & Social Sciences'), ('Business & Accountancy', 'Business & Accountancy'), 
			('Economics & Administration', 'Economics & Administration'), ('Languages & Linguistics', 'Languages & Linguistics'),
			('Built Environment', 'Built Environment'), ('Sports & Exercises Sciences', 'Sports & Exercises Sciences'), 
			('Computer Science & Information Technology', 'Computer Science & Information Technology'),
			)

	DEPARTMENT = [
	    ('Islamic Studies', (
	            ('Usuluddin (Aqidah & Islamic Thought)', 'Usuluddin (Aqidah & Islamic Thought)'), 
	            ('Usuluddin (Al-Quran & Al-Hadith)', 'Usuluddin (Al-Quran & Al-Hadith)'),
	            ('Usuluddin (Daawah & Human Development)', 'Usuluddin (Daawah & Human Development)'), 
	            ('Usuluddin (Islamic History & Civilization)', 'Usuluddin (Islamic History & Civilization)'),
	            ('Islamic Education (Islamic Studies)', 'Islamic Education (Islamic Studies)'), 
	            ('Islamic Studies & Information Technology', 'Islamic Studies & Information Technology'),
	            ('Islamic Studies & Science', 'Islamic Studies & Science'), 
	            ('Muamalat & Management', 'Muamalat & Management'),
	        )
	    ),
	    ('Malay Studies', (
	            ('Bahasa Melayu Profesional', 'Bahasa Melayu Profesional'), ('Linguistik Melayu', 'Linguistik Melayu'),
	            ('Kesusasteraaan Melayu', 'Kesusasteraaan Melayu'), ('Sosio-Budaya Melayu', 'Sosio-Budaya Melayu'),
	            ('Kesenian Melayu', 'Kesenian Melayu'),
	        )
	    ),
	    ('Cultural', (
	            ('Music', 'Music'), ('Drama', 'Drama'),
	            ('Dance', 'Dance'),
	        )
	    ),
	    ('Dentistry', (
	            ('Dental Surgery', 'Dental Surgery'),
	        )
	    ),
	    ('Education', (
	            ('Counselling', 'Counselling'), 
	            ('Early Childhood Education', 'Early Childhood Education'),
	            ('Education Teaching of English as a Second Language', 'Education Teaching of English as a Second Language'),
	        )
	    ),
	    ('Engineering', (
	           ('Biomedical Engineering', 'Biomedical Engineering'), ('Chemical Engineering', 'Chemical Engineering'),
	           ('Civil Engineering', 'Civil Engineering'), ('Electrical Engineering', 'Electrical Engineering'),
	           ('Mechanical Engineering', 'Mechanical Engineering'),
	        )
	    ),
	    ('Law', (
	            ('Laws', 'Laws'),
	            ('Jurisprudence (External)', 'Jurisprudence (External)'),
	        )
	    ),
	    ('Medicine', (
	            ('Medicine', 'Medicine'), ('Biomedical Science', 'Biomedical Science'),
	            ('Nursing', 'Nursing'),
	        )
	    ),
	    ('Science', (
	            ('Chemistry', 'Chemistry'), ('Biochemistry', 'Biochemistry'), ('Biotechnology', 'Biotechnology'),
	            ('Genetics', 'Genetics'), ('Geology', 'Geology'), ('Mathematics', 'Mathematics'),
	            ('Microbiology', 'Microbiology'), ('Physics', 'Physics'), ('Statistics', 'Statistics'),
	        )
	    ),
	    ('Art & Social Sciences', (
	    		('East Asian Studies', 'East Asian Studies'), ('Arts Chinese Studies', 'Arts Chinese Studies'),
	    		('Arts Anthropology and Sociology', 'Arts Anthropology and Sociology'),
	            ('Social Administration', 'Social Administration'), ('Geography', 'Geography'), 
	            ('Environmental Studies', 'Environmental Studies'), ('Arts History', 'Arts History'), 
	            ('Arts English', 'Arts English'), ('Arts Indian Studies', 'Arts Indian Studies'),
	            ('Arts International and Strategic Studies', 'Arts International and Strategic Studies'), 
	            ('Media Studies', 'Media Studies'), ('Arts Southeast Asian Studies', 'Arts Southeast Asian'),
	        )
	    ),
	    ('Business & Accountancy', (
	            ('Accounting', 'Accounting'), ('Business Administration', 'Business Administration'),
	            ('Finance', 'Finance'),
	        )
	    ),
	    ('Economics & Administration', (
	            ('Economics', 'Economics'), ('Administrative Studies and Politics', 'Administrative Studies and Politics'),
	            ('Development Studies', 'Development Studies'), ('Applied Statistic', 'Applied Statistic'),
	        )
	    ),
	    ('Languages & Linguistics', (
	            ('Arabic Language and Linguistics', 'Arabic Language and Linguistics'),
	            ('Chinese Language and Linguistics', 'Chinese Language and Linguistics'), 
	            ('English Language and Linguistics', 'English Language and Linguistics'),
	            ('French Language and Linguistics', 'French Language and Linguistics'), 
	            ('German Language and Linguistics', 'German Language and Linguistics'), 
	            ('Japanese Language and Linguistics', 'Japanese Language and Linguistics'), 
	            ('Spanish Language and Linguistics', 'Spanish Language and Linguistics'),
	            ('Tamil Language and Linguistics', 'Tamil Language and Linguistics'), 
	            ('Italian Language and Linguistics', 'Italian Language and Linguistics'),
	        )
	    ),
	    ('Built Environment', (
	            ('Urban & Regional Planning', 'Urban & Regional Planning'), 
	            ('Science Architecture', 'Science Architecture'), 
	            ('Quantity Surveying', 'Quantity Surveying'), ('Real Estate', 'Real Estate'), 
	            ('Building Surveying', 'Building Surveying'),
	        )
	    ),
	    ('Sports & Exercises Sciences', (
	            ('Sports Science (Exercise Science)', 'Sports Science (Exercise Science)'),
	            ('Sports Management Science', 'Sports Management Science'),
	        )
	    ),
	    ('Computer Science & Information Technology', (
	            ('Artificial Intelligence', 'Artificial Intelligence'), 
	            ('Computer System and Network', 'Computer System and Network'),
	            ('Information Systems', 'Information Systems'), 
	            ('Software Engineering', 'Software Engineering'), 
	            ('Multimedia', 'Multimedia'), ('Data Science', 'Data Science'),
	        )
	    ),
	]

	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	matric_number = models.CharField(max_length=10, null=True)
	faculty = models.CharField(max_length=200, null=True, choices=FACULTY)
	department = models.CharField(max_length=200, null=True, choices=DEPARTMENT)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	CGPA = models.DecimalField(max_digits=4, decimal_places=2, null=True)
	profile_pic = models.ImageField(default="profile1.jpg", null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	
	#return name instead of customer 1 in database
	def __str__(self):
		return self.name



class Mentee(models.Model):

	FACULTY = (
			('Islamic Studies', 'Islamic Studies'), ('Malay Studies', 'Malay Studies'), ('Cultural', 'Cultural'),
			('Dentistry', 'Dentistry'), ('Education', 'Education'), ('Engineering', 'Engineering'),
			('Law', 'Law'), ('Medicine', 'Medicine'), ('Science', 'Science'),
			('Art & Social Sciences', 'Art & Social Sciences'), ('Business & Accountancy', 'Business & Accountancy'), 
			('Economics & Administration', 'Economics & Administration'), ('Languages & Linguistics', 'Languages & Linguistics'),
			('Built Environment', 'Built Environment'), ('Sports & Exercises Sciences', 'Sports & Exercises Sciences'), 
			('Computer Science & Information Technology', 'Computer Science & Information Technology'),
			)

	DEPARTMENT = [
    ('Islamic Studies', (
            ('Usuluddin (Aqidah & Islamic Thought)', 'Usuluddin (Aqidah & Islamic Thought)'), 
            ('Usuluddin (Al-Quran & Al-Hadith)', 'Usuluddin (Al-Quran & Al-Hadith)'),
            ('Usuluddin (Daawah & Human Development)', 'Usuluddin (Daawah & Human Development)'), 
            ('Usuluddin (Islamic History & Civilization)', 'Usuluddin (Islamic History & Civilization)'),
            ('Islamic Education (Islamic Studies)', 'Islamic Education (Islamic Studies)'), 
            ('Islamic Studies & Information Technology', 'Islamic Studies & Information Technology'),
            ('Islamic Studies & Science', 'Islamic Studies & Science'), 
            ('Muamalat & Management', 'Muamalat & Management'),
        )
    ),
    ('Malay Studies', (
            ('Bahasa Melayu Profesional', 'Bahasa Melayu Profesional'), ('Linguistik Melayu', 'Linguistik Melayu'),
            ('Kesusasteraaan Melayu', 'Kesusasteraaan Melayu'), ('Sosio-Budaya Melayu', 'Sosio-Budaya Melayu'),
            ('Kesenian Melayu', 'Kesenian Melayu'),
        )
    ),
    ('Cultural', (
            ('Music', 'Music'), ('Drama', 'Drama'),
            ('Dance', 'Dance'),
        )
    ),
    ('Dentistry', (
            ('Dental Surgery', 'Dental Surgery'),
        )
    ),
    ('Education', (
            ('Counselling', 'Counselling'), 
            ('Early Childhood Education', 'Early Childhood Education'),
            ('Education Teaching of English as a Second Language', 'Education Teaching of English as a Second Language'),
        )
    ),
    ('Engineering', (
           ('Biomedical Engineering', 'Biomedical Engineering'), ('Chemical Engineering', 'Chemical Engineering'),
           ('Civil Engineering', 'Civil Engineering'), ('Electrical Engineering', 'Electrical Engineering'),
           ('Mechanical Engineering', 'Mechanical Engineering'),
        )
    ),
    ('Law', (
            ('Laws', 'Laws'),
            ('Jurisprudence (External)', 'Jurisprudence (External)'),
        )
    ),
    ('Medicine', (
            ('Medicine', 'Medicine'), ('Biomedical Science', 'Biomedical Science'),
            ('Nursing', 'Nursing'),
        )
    ),
    ('Science', (
            ('Chemistry', 'Chemistry'), ('Biochemistry', 'Biochemistry'), ('Biotechnology', 'Biotechnology'),
            ('Genetics', 'Genetics'), ('Geology', 'Geology'), ('Mathematics', 'Mathematics'),
            ('Microbiology', 'Microbiology'), ('Physics', 'Physics'), ('Statistics', 'Statistics'),
        )
    ),
    ('Art & Social Sciences', (
    		('East Asian Studies', 'East Asian Studies'), ('Arts Chinese Studies', 'Arts Chinese Studies'),
    		('Arts Anthropology and Sociology', 'Arts Anthropology and Sociology'),
            ('Social Administration', 'Social Administration'), ('Geography', 'Geography'), 
            ('Environmental Studies', 'Environmental Studies'), ('Arts History', 'Arts History'), 
            ('Arts English', 'Arts English'), ('Arts Indian Studies', 'Arts Indian Studies'),
            ('Arts International and Strategic Studies', 'Arts International and Strategic Studies'), 
            ('Media Studies', 'Media Studies'), ('Arts Southeast Asian Studies', 'Arts Southeast Asian'),
        )
    ),
    ('Business & Accountancy', (
            ('Accounting', 'Accounting'), ('Business Administration', 'Business Administration'),
            ('Finance', 'Finance'),
        )
    ),
    ('Economics & Administration', (
            ('Economics', 'Economics'), ('Administrative Studies and Politics', 'Administrative Studies and Politics'),
            ('Development Studies', 'Development Studies'), ('Applied Statistic', 'Applied Statistic'),
        )
    ),
    ('Languages & Linguistics', (
            ('Arabic Language and Linguistics', 'Arabic Language and Linguistics'),
            ('Chinese Language and Linguistics', 'Chinese Language and Linguistics'), 
            ('English Language and Linguistics', 'English Language and Linguistics'),
            ('French Language and Linguistics', 'French Language and Linguistics'), 
            ('German Language and Linguistics', 'German Language and Linguistics'), 
            ('Japanese Language and Linguistics', 'Japanese Language and Linguistics'), 
            ('Spanish Language and Linguistics', 'Spanish Language and Linguistics'),
            ('Tamil Language and Linguistics', 'Tamil Language and Linguistics'), 
            ('Italian Language and Linguistics', 'Italian Language and Linguistics'),
        )
    ),
    ('Built Environment', (
            ('Urban & Regional Planning', 'Urban & Regional Planning'), 
            ('Science Architecture', 'Science Architecture'), 
            ('Quantity Surveying', 'Quantity Surveying'), ('Real Estate', 'Real Estate'), 
            ('Building Surveying', 'Building Surveying'),
        )
    ),
    ('Sports & Exercises Sciences', (
            ('Sports Science (Exercise Science)', 'Sports Science (Exercise Science)'),
            ('Sports Management Science', 'Sports Management Science'),
        )
    ),
    ('Computer Science & Information Technology', (
            ('Artificial Intelligence', 'Artificial Intelligence'), 
            ('Computer System and Network', 'Computer System and Network'),
            ('Information Systems', 'Information Systems'), 
            ('Software Engineering', 'Software Engineering'), 
            ('Multimedia', 'Multimedia'), ('Data Science', 'Data Science'),
        )
    ),
]

	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	matric_number = models.CharField(max_length=10, null=True)
	faculty = models.CharField(max_length=200, null=True, choices=FACULTY)
	department = models.CharField(max_length=200, null=True, choices=DEPARTMENT)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	CGPA = models.DecimalField(max_digits=4, decimal_places=2, null = True)
	profile_pic = models.ImageField(default="profile1.jpg", null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	
	#return name instead of customer 1 in database
	def __str__(self):
		return self.name


class Match(models.Model):
	STATUS = (
			('Active', 'Active'),
			('Not Active', 'Not Active'),
			)

	mentor = models.ForeignKey(Mentor, null=True, on_delete=models.SET_NULL) #whenever customer is deleed, order still ada cuma null
	mentee = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL) 
	date_matched = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS, default='Active')


	def __str__(self):
		return self.mentee.name


class Goal(models.Model):
	STATUS = (
			('Active', 'Active'),
			('Completed', 'Completed'),
			('Inactive', 'Inactive'),
			)
	# mentor = models.ForeignKey(Mentor, null=True, on_delete=models.SET_NULL) #whenever customer is deleed, order still ada cuma null
	# mentee = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL) 
	match = models.ForeignKey(Match, null=True, on_delete=models.SET_NULL)
	title = models.CharField(max_length=500, null=True)
	category = models.CharField(max_length=200, null=True) 
	description = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)

	def __str__(self):
		return self.title



class Session(models.Model):
	STATUS = (
			('Accepted', 'Accepted'),
			('Rejected', 'Rejected'),
			('Pending', 'Pending'),
			)
	match = models.ForeignKey(Match, null=True, on_delete=models.SET_NULL)
	name = models.CharField(max_length=200, null=True)
	setup_date = models.DateTimeField(help_text = "  e.g 11/28/2020 13:30")
	location = models.CharField(max_length=200, null=True)
	status = models.CharField(max_length=200, null=True, default='Pending', choices=STATUS)
	note = models.CharField(max_length=1000, null=True, blank=True)

	def __str__(self):
		return self.name



class Task(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Completed', 'Completed'),
			)

	# mentor = models.ForeignKey(Mentor, null=True, on_delete=models.SET_NULL) #whenever customer is deleted, order still ada cuma null
	# mentee = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL)
	match = models.ForeignKey(Match, null=True, on_delete=models.SET_NULL)
	task_title = models.CharField(max_length=200, null=True)
	subject = models.CharField(max_length=200, null=True)
	description = models.CharField(max_length=500, blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	document = models.FileField(blank=True)

	def __str__(self):
		return self.task_title or ''


class Ad(models.Model):
	CATEGORY = (
			('Academic', 'Academic'),
			('Non-Academic', 'Non-Academic'),
			) 

	mentee = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL)
	ad_title = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.TextField(blank=True, null=True)
	publish = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.ad_title or ''

class Ad2(models.Model):
	CATEGORY = (
			('Academic', 'Academic'),
			('Non-Academic', 'Non-Academic'),
			) 
	
	mentor = models.ForeignKey(Mentor, null=True, on_delete=models.SET_NULL)
	ad_title = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.TextField(blank=True, null=True)
	publish = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.ad_title or ''

class Result(models.Model):
	TYPES = (
			('Quiz', 'Quiz'),
			('Mid-Exam', 'Mid-Exam'),
			('Final-Exam', 'Final-Exam'),
			)

	mentee = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL)
	semester = models.CharField(max_length=200, null=True)
	subject = models.CharField(max_length=200, null=True)
	grade = models.CharField(max_length=200, null=True)
	types = models.CharField(max_length=200, null=True, choices=TYPES)
	
	def __str__(self):
		return self.subject or ''

class Category(models.Model):
	# mentor = models.ForeignKey(Mentor, null=True, on_delete=models.SET_NULL)
	# mentee = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL)
	match = models.ForeignKey(Match, null=True, on_delete=models.SET_NULL)

	name = models.CharField(max_length=255)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


class Quizzes(models.Model):

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")
        ordering = ['id']

    # mentee = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL)
    # mentor = models.ForeignKey(Mentor, null=True, on_delete=models.SET_NULL)   
    match = models.ForeignKey(Match, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255, default=_("New Quiz"), verbose_name=_("Quiz Title"))
    # category = models.ForeignKey(Category, default=1, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UpdatedQuestion(models.Model):

    date_updated = models.DateTimeField(verbose_name=_("Last Updated"), auto_now=True)

    class Meta:
        abstract = True


class Question(UpdatedQuestion):

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['id']

    SCALE = (
        (0, _('Fundamental')),
        (1, _('Beginner')),
        (2, _('Intermediate')),
        (3, _('Advanced')),
        (4, _('Expert'))
    )

    TYPE = (
        (0, _('Multiple Choice')),
    )

    quiz = models.ForeignKey(Quizzes, null=True, on_delete=models.DO_NOTHING)
    technique = models.IntegerField(choices=TYPE, default=0, verbose_name=_("Type of Question"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    difficulty = models.IntegerField(choices=SCALE, default=0, verbose_name=_("Difficulty"))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Created"))
    is_active = models.BooleanField(default=False, verbose_name=_("Active Status"))

    def __str__(self):
        return self.title


class Answer(UpdatedQuestion):

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ['id']

    question = models.ForeignKey(Question, null=True, on_delete=models.DO_NOTHING)
    answer_text = models.CharField(max_length=255, verbose_name=_("Answer Text"))
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text


#-------------------------------------------------------------------------------------------------------------
class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)
	
	#return name instead of customer in database
	def __str__(self):
		return self.name



class Product(models.Model):
	CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			)

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name


class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)

	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL) #whenever customer is deleed, order still ada cuma null
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True)
	
	def __str__(self):
		return self.product.name


	

	