from django.urls import path, re_path
from jobs.views import *


urlpatterns = [
    path('', JobsHome.as_view(), name="home"),
    path('vakatsi/', JobsVakatsi.as_view(), name="vakatsi"),
    path('applicant/', JobsApplicant.as_view(), name="applicant"),
    path('add/company/', AddJobsCompany.as_view(), name="add_company"),
    path('company/<int:pk>/',JobsCompany.as_view(), name="company"),
    path('register/', JobsRegister.as_view(), name="register"),
    path('login/', JobsLogIn.as_view(), name="login"),
    path('post/<int:pk>/', JobsPost.as_view(), name="post"),

    path('edit/post/<int:pk>/', EditPost.as_view(), name="edit_post"),
    path('edit/company/<int:pk>/', EditCompany.as_view(), name="edit_company"),

    
    path('add/vacancy/', AddPage.as_view(), name="add_vacancy"),
    path('profile/', JobsProfile.as_view(), name="profile"),
    path('profile/<int:pk>/', JobsProfileUser.as_view(), name="profile_user"),
    path('profile/settings/', JobsSettingsProfile.as_view(), name="settings"),

    path('logout/', LogUp_User, name="logout"),
    path('apply/', apply_for_job, name='apply_for_job'),
    path('cancel/', cancel_application, name='cancel_application'),
    path('get_areas/', get_areas_by_city, name='get_areas_by_city'),
] 
#  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)