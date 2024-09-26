from django.shortcuts import redirect,get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseNotFound
from django.views.generic import ListView,DetailView, CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout,login
from django.urls import reverse_lazy
from customuser.models import CustomUser
from django.http import JsonResponse
from django.utils.html import strip_tags
from .send_sms_to_telegram import send_sms_to_telegram
from django.db.models import Q
from django.views.decorators.http import require_POST
# from rest_framework import generics

from .config import *
from .models import *
from .forms import *
from .utils import *


@require_POST
def apply_for_job(request):
    job_id = request.POST.get('job_id')
    
    # # Получаем вакансию
    try:
        job = Jobs.objects.get(id=job_id)
    except Jobs.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Вакансия не найдена.'})
    
    # Создаем отклик
    Application.objects.create(job=job, user=request.user)
    
    return JsonResponse({'success': True, 'message': 'Отклик отправлен успешно!'})


@require_POST
def cancel_application(request):
    job_id = request.POST.get('job_id')
    
    # Получаем вакансию
    try:
        job = Jobs.objects.get(id=job_id)
    except Jobs.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Вакансия не найдена.'})
    
    # Удаляем отклик
    application = Application.objects.filter(job=job, user=request.user).first()
    if application:
        application.delete()
        return JsonResponse({'success': True, 'message': 'Отклик отменен.'})
    else:
        return JsonResponse({'success': False, 'message': 'Отклик не найден.'})


class JobsHome(DataMixin, ListView):
    model = Jobs
    template_name = "jobs/index.html" # ссылка на файл
    # allow_empty = False # Генератор ошыпки как DEBUG
    context_object_name = "post"

    def get_queryset(self):
        # Используем select_related для загружки связанных объектов
        return list(Jobs.objects.select_related('user', 'company',"area").filter(published=True).reverse()[:5])
    

    def get_context_data(self, *, object_list=None,**kwargs):
        user_profile = CustomUser.objects.filter(applicant=True).all()
        context = super().get_context_data(**kwargs)
        context['type_of_work'] = Jobs.TYPE_OF_WORK
        if user_profile:
            context['user_profile'] = user_profile
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items())+list(c_def.items()))


class JobsVakatsi(DataMixin,ListView):
    template_name = "jobs/vakatsi.html" # ссылка на файл
    context_object_name = "post"

    def get_queryset(self):
        search = self.request.GET.get('search')
        city_id = self.request.GET.get('cities')
        wage = self.request.GET.get('wage')
        experience = self.request.GET.get('experiences')
        schedules = self.request.GET.get('schedules')

        if search:
            queryset = Jobs.objects.select_related('user', 'city', 'company', "area").filter(Q(title__icontains=search) | Q(content__icontains=search ) | Q(title_info__icontains=search))
        else:
            queryset = Jobs.objects.select_related('user', 'city', 'company', "area").all()
        if city_id:
            queryset = queryset.filter(city__city=city_id)
        if wage:
            queryset = queryset.filter(wage__gte=wage)
        if experience:
            for i in Jobs.EXPERIENCE:
                if i[1] ==  experience:
                    queryset = queryset.filter(experience=i[0])
        if schedules:
            for i in Jobs.SCHEDULE:
                if i[1] ==  schedules:
                    queryset = queryset.filter(schedule=i[0])
        return queryset

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        cities = City.objects.all()
        context['schedules'] = Jobs.SCHEDULE
        context['experiences'] = Jobs.EXPERIENCE
        if cities:
            context['cities'] = cities

        c_def = self.get_user_context(title="Все вакацы")
        return  dict(list(context.items())+list(c_def.items()))


class JobsApplicant(DataMixin,ListView):
    template_name = "jobs/applicant.html" # ссылка на файл
    context_object_name = "profile_user"

    def get_queryset(self):
        queryset = CustomUser.objects.filter(applicant=True)
        
        searchValue = self.request.GET.get('search')
        schedule = self.request.GET.get('schedule')
        education = self.request.GET.get('education')
        relocation = self.request.GET.get('relocation')
        experience = self.request.GET.get('experience')
        
        if searchValue:
            queryset = queryset.filter(Q(name_activity__icontains=searchValue) | Q(description__icontains=searchValue))
        if schedule:
            for i in CustomUser.SCHEDULE:
                if i[1] ==  schedule:
                    queryset = queryset.filter(schedule=i[0])
        if relocation:
            for i in CustomUser.RELOCATION:
                if i[1] ==  relocation:
                    queryset = queryset.filter(relocation=i[0])
        if education:
            for i in CustomUser.EDUCATION_LEVEL:
                if i[1] ==  education:
                    queryset = queryset.filter(education=i[0])
        if experience:
            for i in CustomUser.EXPERIENCE:
                if i[1] ==  experience:
                    queryset = queryset.filter(experience=i[0])
        
        return queryset

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule'] = CustomUser.SCHEDULE
        context['relocation'] = CustomUser.RELOCATION
        context['education'] = CustomUser.EDUCATION_LEVEL
        context['experience'] = CustomUser.EXPERIENCE
        c_def = self.get_user_context(title="Все соискатели")
        return  dict(list(context.items())+list(c_def.items()))


class JobsPost(DataMixin, DetailView):
    model = Jobs 
    template_name = "jobs/post.html"
    context_object_name = "post"

    def get_queryset(self):
        # Используем select_related для загружки связанных объектов
        return Jobs.objects.select_related('user', 'company',"area")

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        jobs = Jobs.objects.filter(
                    ~Q(id=context['post'].id) &
                    (Q(title=context['post'].title) | 
                    Q(title_info=context['post'].title_info))
                )
        context['jobs'] = jobs

        message_text= (
            f'{self.request.user.username}\n'
            'посмотрель вашу заявку\n'
            f'{context["post"].title}\n'
            
        )
        job = self.get_object()
        viewed_key = f'viewed_job_{job.pk}'
        if not self.request.session.get(viewed_key, False):
            job.increase_view()
            self.request.session[viewed_key] = True
            message = {
            "text": strip_tags(message_text),  
            }
            send_sms_to_telegram(BOT_TOKEN, context['post'].user.telegram, message, "user")

        c_def = self.get_user_context(title=context["post"].title)
        return  dict(list(context.items())+list(c_def.items()))    


class JobsProfileUser(DataMixin, DetailView):
    model = CustomUser
    template_name = "jobs/profile_user.html"
    context_object_name = "user_profile"
    
    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.filter(owner=self.request.user)
        jubs = Jobs.objects.filter(user=self.request.user).exclude(company__in=company).all
        context['comp'] = company
        context['jubs'] = jubs
        text = None
        url = None
        
        text = self.request.user.username
        if self.request.user.applicant:
            url = f'http://127.0.0.1:8000/profile/{self.request.user.id}/'
        else:
            url = 'ФИЗ лицо'
        message_text= (
            f'{text}\n'
            f'{url}\n'
            'посмотрель вашу резюме'
        )
        # Обрабатываем увеличение количества просмотров
        user = self.get_object()
        viewed_key = f'viewed_user_{user.pk}'
        if not self.request.session.get(viewed_key, False):
            user.increase_view()
            self.request.session[viewed_key] = True
            message = {
                    "text": strip_tags(message_text),
                }
            send_sms_to_telegram(BOT_TOKEN, context['user_profile'].telegram, message, "user")

        c_def = self.get_user_context(title=context["user_profile"].username)
        return  dict(list(context.items())+list(c_def.items()))


class JobsCompany(DataMixin,DetailView):
    model = Company
    template_name = "jobs/jobs_company.html"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Организатция {context['post'].name}')
        context['review_form'] = ReviewForm()
        context['jobs'] = Jobs.objects.filter(company = context['post'].id).all
        context['rating_range'] = range(1, 6)  # Добавляем диапазон значений для рейтинга
        context['reviews'] = self.object.review_set.all().order_by('-created_at')  # Выборка отзывов в обратном порядке
        context.update(c_def)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.company = self.object
            review.user = request.user
            review.save()
            return redirect(request.get_full_path())  
        return self.get(request, *args, **kwargs)
    
    def get_queryset(self):
        # Используем prefetch_related для загружки связанных объектов
        return Company.objects.prefetch_related('owner').all()


class AddPage(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = "jobs/addpage.html"
    success_url = reverse_lazy("profile")
    login_url = reverse_lazy("login")
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Форма добавлении"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Определяем заголовок компании или пользователя и ссылку на него
        if form.instance.company:
            company_or_user = form.instance.company.name  # Поле name у Company
            link = f"http://127.0.0.1:8000/company/{form.instance.company.id}/"
        else:
            company_or_user = self.request.user.username
            if self.request.user.applicant:
                link = f"http://127.0.0.1:8000/vakatsi/{self.request.user.id}/"
            else:
                link = "ФИЗ лицо"

        # Формируем текст сообщения
        message_text = (
            f"{company_or_user}: {form.instance.title}\n"
            f"Тип: {dict(form.fields['schedule'].choices).get(form.instance.schedule, 'Не указан')}\n"
            f"{form.instance.content}\n"
            f"<b>{form.instance.wage} сом</b>\n"
            f"📍 {form.instance.area.area}, {form.instance.city.city}\n"
            f"Нужен: {form.instance.number_persons} человек.\n"
            f"Ссылка: {link}"
        )

        message = {
            "text": strip_tags(message_text),  
        }
        send_sms_to_telegram(BOT_TOKEN, GROUP_ID, message, "group")
        return super().form_valid(form)


class EditPost(DataMixin, UpdateView):
    model = Jobs
    form_class = JobListingForm
    template_name = 'jobs/edit_post.html'  # Ваш шаблон для формы
    success_url = reverse_lazy('profile')  # URL, на который будет перенаправлен пользователь после успешного обновления
    
    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'{context['object']}')
        return dict(list(context.items())+list(c_def.items()))


class EditCompany(DataMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'jobs/edit_post.html'  # Ваш шаблон для формы
    success_url = reverse_lazy('profile')  # URL, на который будет перенаправлен пользователь после успешного обновления

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'{context['object']}')
        return dict(list(context.items())+list(c_def.items()))


class AddJobsCompany(LoginRequiredMixin, DataMixin, CreateView):
    model = Company
    form_class = AddCompanyForm
    template_name = "jobs/add_jobs_company.html"
    success_url = reverse_lazy("profile") # Перенаправление на другу страницу по имени в urls
    raise_exception = True # Страница 403 доступ запрешён

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Форма добавлени организатцы")
        return  dict(list(context.items())+list(c_def.items()))
    
    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем текущего пользователя
        form.instance.logo = self.request.FILES['logo']
        return super().form_valid(form)


class JobsRegister(DataMixin, CreateView):
    form_class = LogRegisterUserForm
    template_name = "jobs/register_user.html"
    success_url = reverse_lazy("vakatsi")

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Форма регистрацы")
        return  dict(list(context.items())+list(c_def.items()))
    
    def form_valid(self,form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class JobsLogIn(DataMixin, LoginView):
    form_class = LogInForm
    template_name = "jobs/login_user.html"

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Форма входа")
        return  dict(list(context.items())+list(c_def.items()))
    
    # def get_success_url(self):          Редирек если пользователь зарегистрирован
    #     return reverse_lazy("vakatsi")


def get_areas_by_city(request):
    city_id = request.GET.get('city_id')
    areas = Area.objects.filter(city_id=city_id).all()
    return JsonResponse({'areas': [area.to_json() for area in areas]})


class JobsProfile(LoginRequiredMixin, DataMixin, ListView):
    template_name = "jobs/profile.html"

    def get_queryset(self):
        return CustomUser.objects.none()

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)

        user_profile = CustomUser.objects.filter(username=self.request.user.username).first()
        jobs = Jobs.objects.filter(user=self.request.user).select_related('user', 'city', 'company', "area").all()
        company = Company.objects.filter(owner=self.request.user).all()
        skills = TextEntry.objects.filter(user=self.request.user).all()
        formCustomUser = CustomUserForm(instance=self.request.user)
        context['formCustomUser'] = formCustomUser

        if user_profile:
            context['user_profile'] = user_profile
        if jobs:
            context['jobs'] = jobs
        if company:
            context['company'] = company
        if skills:
            context['skills'] = skills
        c_def = self.get_user_context(title=f"Прифиль {self.request.user.username}")
        return  dict(list(context.items())+list(c_def.items()))
    
    def post(self, request, *args, **kwargs):
        form = CustomUserForm(request.POST, request.FILES, instance=request.user)
        
        if form.is_valid():
            form.save()

        return JsonResponse({'success': True})


class JobsSettingsProfile(LoginRequiredMixin, DataMixin, UpdateView):
    model = CustomUser
    form_class = SettingsProfileFormActive
    template_name = "jobs/settings_profile.html"
    success_url = reverse_lazy("profile")
    raise_exception = True
    
    def get_object(self, queryset=None):
        return self.request.user  # Возвращаем текущего пользователя

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Форма изминени данных пользователя")
        return  dict(list(context.items())+list(c_def.items()))


def LogUp_User(request):
    logout(request)
    return redirect("login")

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдено!!!</h1>")