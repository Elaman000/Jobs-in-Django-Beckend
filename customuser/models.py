from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class CustomUser(AbstractUser):
    ACTIVITY_TYPE_INDIVIDUAL = [
        ('1', 'Самозанятость'),
        ('2', 'Фриланс'),
        ('3', 'Индивидуальное предпринимательство'),
        ('4', 'Ремесленничество'),
        ('5', 'Услуги на дому'),
        ('6', 'Консультирование'),
        ('7', 'Репетиторство'),
        ('8', 'Творческая деятельность'),
        ('9', 'Сельскохозяйственная деятельность'),
        ('10', 'Интернет-бизнес'),
        ('11', 'Транспортные услуги'),
        ('12', 'Спортивная деятельность'),
        ('13', 'Сфера услуг'),
        ('14', 'Строительство'),
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
    RELOCATION = [
        ('1', 'Не готов к переезду'),
        ('2', 'Готов к переезду в пределах города'),
        ('3', 'Готов к переезду в пределах региона'),
        ('4', 'Готов к переезду в пределах страны'),
        ('5', 'Готов к международному переезду'),
        ('6', 'Готов к переезду на временной основе'),
        ('7', 'Готов к постоянному переезду'),
    ]
    
    EDUCATION_LEVEL = [
        ('1', 'Среднее образование'),
        ('2', 'Среднее профессиональное образование'),
        ('3', 'Высшее образование (бакалавр)'),
        ('4', 'Высшее образование (магистр)'),
        ('5', 'Докторская степень'),
        ('6', 'Неоконченное высшее образование'),
        ('7', 'Специализированное образование (курсы, сертификаты)'),
        ('8', 'Профессиональное обучение'),
        ('9', 'Дополнительное образование'),
    ]
    GENDER_CHOICES = [
        ('М', 'Мужчина'),
        ('Э', 'Женшина'),
        ('Н', 'Не обязательно'),
    ]
    EXPERIENCE = [
        ('1', 'Без опыта'),
        ('2', 'От 1 года до 3 лет'),
        ('3', 'От 3 до 5 лет'),
        ('4', 'От 5 лет'),
        ('5', 'Стажировка'),
        ('6', 'Волонтерский опыт'),
        ('7', 'Производственная практика'),
    ]

    activity = models.CharField(max_length=2,blank=True, null=True,choices=ACTIVITY_TYPE_INDIVIDUAL, verbose_name="Тип деятельности")
    description = models.TextField(max_length=555,blank=True, verbose_name="Описание")
    number_persons = models.IntegerField(blank=True, null=True,verbose_name="Количество человек в команде")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Юридический адрес")
    telegram = models.CharField(max_length=255, blank=True, null=True,verbose_name='Telegram ID или @UserName') 
    web_url = models.CharField(max_length=2000, blank=True, null=True,verbose_name='URL веб сайта')
    whatsapp = models.CharField(max_length=255, blank=True, null=True,verbose_name='whatsapp номер, c кодом страны')
    phone = models.CharField(max_length=15, blank=True, null=True,verbose_name='Номер телефона')
    birth_date = models.DateField(null=True, blank=True,verbose_name="Дата рождения")
    photo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name="Фото")
    gender = models.CharField(max_length=1, null=True, blank=True,choices=GENDER_CHOICES,verbose_name="Пол")
    nationality = CountryField(blank_label='(Выберите страну)', blank=True, null=True,verbose_name="Натция")
    applicant = models.BooleanField(default=False, null=True, blank=True, verbose_name="Соискатель?")
    name_activity=models.CharField(default='', max_length=250,verbose_name="Основные навыки или профессия")
    team = models.BooleanField(default=False, null=True, blank=True, verbose_name="У вас есть команда?")
    schedule = models.CharField(max_length=1, null=True, blank=True,choices=SCHEDULE,verbose_name="График работы")
    relocation = models.CharField(max_length=1,null=True, blank=True, choices=RELOCATION ,verbose_name="Переезд")
    education = models.CharField(max_length=1, null=True, blank=True,choices=EDUCATION_LEVEL,verbose_name="Образование")
    experience = models.CharField(max_length=2, null=True, blank=True,choices=EXPERIENCE,verbose_name="Опыт работы")
    desired_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Требуемая плата")
    enlarge_view = models.IntegerField(default=0,blank=True, null=True, verbose_name="Количество просмотров")
    time_create = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")


    def increase_view(self):
        if self.enlarge_view > 0:
            self.enlarge_view += 1
            self.save()

