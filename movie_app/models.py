from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class DressingRoom(models.Model):
    floor = models.IntegerField()
    room = models.IntegerField()

    def __str__(self):
        return f'{self.floor} {self.room}'

class Actor(models.Model):

    MALE = 'Male'
    FEMALE = "Female"

    gender_choise =[
        (MALE,'Male'),
        (FEMALE,"Female"),]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    slug=models.SlugField(default='',null=False, db_index=True)
    gender=models.CharField(max_length=6,choices=gender_choise,default=MALE)
    dressing=models.OneToOneField(DressingRoom,on_delete=models.SET_NULL,null=True,blank=True)
    profile_pic=models.ImageField(upload_to='images/',blank=True)

    def save(self,*args,**kwargs):
        full_name=f'{self.first_name} {self.last_name}'
        self.slug=slugify(full_name)
        super(Actor,self).save(*args,**kwargs)

    def get_url(self):
        return reverse('slug_actor', args=[self.slug])

    def __str__(self):
        if self.gender == self.MALE:
            return f' Актер {self.first_name} {self.last_name}'
        else:
            return f' Актриса {self.first_name} {self.last_name}'


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_director = models.EmailField( max_length=254)
    slug=models.SlugField(default='',null=False, db_index=True)
    profile_pic=models.ImageField(upload_to='images/',blank=True)


    def save(self,*args,**kwargs):
        full_name=f'{self.first_name} {self.last_name}'
        self.slug=slugify(full_name)
        super(Director,self).save(*args,**kwargs)

    def get_url(self):
        return reverse('slug_director', args=[self.slug])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Movie(models.Model):
    EUR = 'EUR'
    USD = "USD"
    RUB = 'RUB'

    currency_choice =[
        (EUR,'Euro'),
        (USD,'Dollar'),
        (RUB,'Ruble'),]


    name=models.CharField(max_length=40)
    rating=models.IntegerField(validators=[MinValueValidator(1),
                                        MaxValueValidator(100)]) 
    year=models.IntegerField(null=True,blank=True) 
    budget=models.IntegerField(default=100,blank=True, validators=[MinValueValidator(1)]) 
    currency=models.CharField(max_length=3,choices=currency_choice,default=RUB)
    slug=models.SlugField(default='',null=False, db_index=True)
    director=models.ForeignKey(Director,on_delete=models.CASCADE,null=True,blank=True, related_name='movies')
    actors=models.ManyToManyField(Actor,related_name='movies')
    profile_pic=models.ImageField(upload_to='images/',blank=True,null=True)



    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        super(Movie,self).save(*args,**kwargs)


    def __str__(self):
        return f'{self.name} | {self.rating}%'

    def get_url(self):
        return reverse('slug_movie', args=[self.slug])