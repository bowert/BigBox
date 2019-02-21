from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class Post(models.Model):
    LAWNMOWING='LM'
    SNOWSHOVELING='SS'
    DOGWALKING='DW'
    PETSITTING='PS'
    BABYSITTING='BS'
    CLEANING='C'
    MOVING='M'
    OTHER='O'

    TYPE_CHOICES = (
            (LAWNMOWING, 'Lawn Mowing'),
            (SNOWSHOVELING, 'Snow Shoveling'),
            (DOGWALKING, 'Dog Walking'),
            (PETSITTING, 'Pet Sitting'),
            (BABYSITTING, 'Baby Sitting'),
            (CLEANING, 'Cleaning'),
            (MOVING, 'Moving'),
            (OTHER, 'Other'),
    )

    Pay = models.FloatField()
    Location = models.TextField()
    DateTime = models.DateTimeField()
    #Interested = models.ManyToManyField(Seeker)
    Description = models.TextField()
    JobType = models.CharField(
            max_length=100,
            choices=TYPE_CHOICES,
    )

class Report(models.Model):
    PAYMENT = 'PI'
    VIOLENCE = 'V'
    NOSHOW = 'NS'
    SCAM = 'S'
    OTHER = 'O'

    REPORT_CHOICES = (    
        (PAYMENT, 'Payment Issue'),
        (VIOLENCE, 'Violence'),
        (NOSHOW, 'No show'),
        (SCAM, 'Scam'),
        (OTHER, 'Other'),
    )

    Classification = models.CharField(
        max_length=100,
        choices=REPORT_CHOICES
    )
    Details = models.TextField()

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    User = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True)
    Email = models.CharField(max_length = 60, unique=True)
    FirstName = models.CharField(max_length = 50)
    LastName = models.CharField(max_length = 50)
    Description = models.TextField()
    Age = models.SmallIntegerField()
    #image
    Contacts = models.ManyToManyField("self", blank=True)
    Reports = models.ForeignKey(Report, on_delete=models.CASCADE, blank=True, null=True)

    is_anonymous = False
    is_authenticated = True
    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class JobChoices(models.Model):
    Types = models.CharField(
            max_length=100,
            choices=Post.TYPE_CHOICES,
    )
            
class Review(models.Model):
    Rating = models.SmallIntegerField() #Precision undecided

class Seeker(User):     #Job Seeker, subclass to User
    
    PrefType = models.ForeignKey(
            JobChoices,
            on_delete=models.CASCADE,
    )
    IntJob = models.ManyToManyField(Post)
    Reviews = models.ManyToManyField(Review)
    Location = models.TextField()

class Creator(User):    #Job Creator
    Posts = models.ManyToManyField(Post)
    Reviews = models.ManyToManyField(Review)


