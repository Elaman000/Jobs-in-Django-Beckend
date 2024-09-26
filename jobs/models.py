from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError
import os


class City(models.Model):
    city = models.CharField(max_length=255, unique=True,verbose_name="Название города")
    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
    def __str__(self):
        return self.city

class Area(models.Model):
    area = models.CharField(max_length=255, unique=True, verbose_name="Название района")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")
    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"
    def __str__(self):
        return self.area
    def to_json(self):
        return {
            'id': self.id,
            'area': self.area
        }



class Company(models.Model):

    ACTIVITY_TYPE = [
        ('13', 'Сельское хозяйство'),
        ('1', 'Производство'),
        ('2', 'Торговля'),
        ('3', 'Сфера услуг'),
        ('4', 'Образование'),
        ('5', 'Здравоохранение'),
        ('6', 'ИТ и телекоммуникации'),
        ('7', 'Строительство'),
        ('8', 'Транспорт и логистика'),
        ('9', 'Финансы и страхование'),
        ('10', 'Наука и исследования'),
        ('11', 'Искусство и культура'),
        ('12', 'Государственная служба'),
    ]
    TYPE_OF_OWN = [
        ('1', 'Государственная собственность'),
        ('2', 'Иностранная собственность'),
        ('3', 'Частная собственность'),
        ('4', 'Муниципальная собственность'),
        ('5', 'Собственность общественных организаций'),
        ('6', 'Совместная собственность'),
        ('7', 'Акционерная собственность'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Пользователь')
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name="Логотип")
    address = models.CharField(max_length=255, verbose_name="Юридический адрес")
    reviews = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Review', related_name='reviews', verbose_name="Отзывы")
    private = models.BooleanField(default=True, verbose_name="Предприятие является частным агентством занятости")
    activity = models.CharField(max_length=2, null=True, blank=True,choices=ACTIVITY_TYPE,verbose_name="Вид деятельности")
    own = models.CharField(max_length=1, null=True, blank=True,choices=TYPE_OF_OWN,verbose_name="Форма собственности")
    contact = models.CharField(max_length=255, verbose_name="Контактные данные")
    telegram = models.CharField(max_length=255, blank=True, null=True,verbose_name='Telegram номер или @Name')
    web_url = models.CharField(max_length=2000, blank=True, null=True,verbose_name='URL веб сайта')
    whatsapp = models.CharField(max_length=255, blank=True, null=True,verbose_name='whatsapp номер')
    phone = models.CharField(max_length=15, blank=True, null=True,verbose_name='Номер телефона')
    enlarge_view = models.IntegerField(default=0,blank=True, null=True, verbose_name="Количество просмотров")

    def enlarge_viewё(self):
        if self.enlarge_view > 0:
            self.enlarge_view += 1
            self.save()

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организаци"
    def __str__(self):
        return self.name

class Review(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review_text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Рейтинга")
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
    def __str__(self):
        return f"Оставил отзыв {self.user.username} к {self.company.name}"

class Jobs(models.Model):

    SCHEDULE = [
        ('1', 'Полный рабочий день'),
        ('2', 'Частичная занятость'),
        ('3', 'Удаленная работа'),
        ('4', 'Гибкий график'),
        ('5', 'Сменный график'),
        ('6', 'Свободный график'),
        ('7', 'Вахтовый метод'),
        ]

    EXPERIENCE = [
        ('1', 'Без опыта'),
        ('2', 'От 1 до 3 лет'),
        ('3', 'От 3 до 5 лет'),
        ('4', 'Более 5 лет'),
        ('5', 'Стажировка'),
        ('6', 'Волонтерский опыт'),
        ('7', 'Производственная практика'),
        ]
    SCHEDULE = [
        ('1', 'Полный рабочий день'),
        ('2', 'Неполный рабочий день'),
        ('3', 'Частичная занятость'),
        ('4', 'Удаленная работа'),
        ('5', 'Надомная работа'),
        ('6', 'Гибкий график'),
        ('7', 'Посменный'),
        ('8', 'Свободный график'),
        ('9', 'Вахтовый метод'),
        ]
    

    TYPE_OF_WORK =  [
        ('1', 'Строительство'),
        ('2', 'Дворник'),
        ('3', 'Сантехник'),
        ('4', 'Электрик'),
        ('5', 'Слесарь'),
        ('6', 'Маляр'),
        ('7', 'Каменщик'),
        ('8', 'Уборщик'),
        ('9', 'Плотник'),
        ('10', 'Грузчик'),
        ('11', 'Монтажник'),
        ('12', 'Кровельщик'),
        ('13', 'Водитель'),
        ('14', 'Штукатур'),
        ('15', 'Столяр'),
        ('16', 'Сварщик'),
        ('17', 'Токарь'),
        ('18', 'Плиточник'),
        ('19', 'Разнорабочий'),
        ('20', 'Машинист'),
    ]

    title=models.CharField(max_length=250,verbose_name="Загаловак")
    title_info = models.CharField(max_length=150, verbose_name="Под загаловок")
    content = models.TextField(blank=True, verbose_name="Описание")
    time_create = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    published = models.BooleanField(default=True, verbose_name="Опубликовано")
    city = models.ForeignKey(City, on_delete=models.CASCADE,verbose_name="Город")
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name="Район")
    wage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Заработная плата")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Компания")
    experience = models.CharField(max_length=1, null=True, blank=True,choices=EXPERIENCE,verbose_name="Опыт работы")
    schedule = models.CharField(max_length=1, null=True, blank=True,choices=SCHEDULE,verbose_name="График работы")
    type_of_work = models.CharField(max_length=2, null=True, blank=True,choices=TYPE_OF_WORK,verbose_name="Тип работы")
    number_persons = models.IntegerField(verbose_name="Количество необходимых человек")
    data_add = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    enlarge_view = models.IntegerField(default=0, blank=True, null=True,verbose_name="Количество просмотров")

    def decrement_number_persons(self):
        if self.number_persons > 0:
            self.number_persons -= 1
            self.save()

    # def enlarge_view(self):
    #     if self.enlarge_view > 0:
    #         self.enlarge_view += 1
    #         self.save()
    def increase_view(self):
        if self.enlarge_view is not None:
            self.enlarge_view += 1
            self.save()

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.title


class TextEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Ключевые навык")
    
    class Meta:
        verbose_name = "Навык пользователя"
        verbose_name_plural = "Навыки пользователя"
    
    def __str__(self):
        return self.text
    
class Application(models.Model):
    job = models.ForeignKey(Jobs,on_delete=models.CASCADE, verbose_name="Вакансия")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Отклик на вакасию"
        verbose_name_plural = "Отклики на вакасию"

    def __str__(self):
        return f"Отклик от {self.user} на вакансию {self.job}"