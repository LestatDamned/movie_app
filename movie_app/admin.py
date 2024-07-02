from typing import Any
from django.contrib import admin, messages
from .models import Movie,Director,Actor,DressingRoom
from django.db.models import QuerySet
# Register your models here.


@admin.register(DressingRoom)
class DressingRoomAdmin(admin.ModelAdmin):
  list_display = ['floor','room','actor']

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ['first_name','last_name']}


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
  list_display = ['full_name','email_director',]
  list_editable=['email_director']
  prepopulated_fields = {'email_director': ['first_name','last_name']}


  @admin.display(description='Full name')
  def full_name(self, director:Director):
    return f'{director.first_name} {director.last_name}'
  

class Ratingfilter(admin.SimpleListFilter):
  title = 'Rating filter'
  parameter_name = 'rating'


  def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
    return [
      ('<40','Low rating'),
      ('from 40 until 59','Mid rating'),
      ('from 60 until 79','High rating'),
      ('>=80','Legedary'),
    ]
  
  def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
    if self.value()=='<40':
      return queryset.filter(rating__lt=40)
    elif self.value()=='from 40 until 59':
      return queryset.filter(rating__gte=40).filter(rating__lt=59)
    elif self.value()=='from 60 until 79':
      return queryset.filter(rating__gte=60).filter(rating__lt=79)
    elif self.value()=='>=80':
      return queryset.filter(rating__gte=80)
    return queryset

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
  # fields = ['name','rating']
  # exclude = ['slug']
  readonly_fields = ['currency','slug']
  #prepopulated_fields = {'slug': ('name', )}
  list_display=['name','rating','year','budget','director','rating_status']
  list_editable=['rating','year','budget','director']
  ordering = ['-rating','-name']
  list_per_page = 9
  actions = ['set_dollar','set_euro']
  search_fields = ['name__istartswith','rating']
  list_filter = [Ratingfilter]
  filter_horizontal = ['actors']


  @admin.display(ordering='rating',description='Оценка')
  def rating_status(self,movie:Movie):
    if movie.rating < 50:
      return 'Плохое кино'
    elif movie.rating < 70:
      return 'Нормальное кино'
    elif movie.rating <= 85:
      return 'Хорошоее кино'
    else:
      return 'Отличное кино'
    
  @admin.action(description='установить валюту доллар')
  def set_dollar(self,request,qs: QuerySet):
    count_updated = qs.update(currency=Movie.USD)
    self.message_user(
      request,f'Было зарегестрированное количество - {count_updated} записей')
    
  @admin.action(description='установить валюту евро')
  def set_euro(self,request,qs: QuerySet):
    count_updated = qs.update(currency=Movie.EUR)
    self.message_user(
      request,f'Было зарегестрированное количество - {count_updated} записей',
      messages.ERROR)