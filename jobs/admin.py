from django.contrib import admin

from jobs.models import *

# class JobsAdmin(admin.ModelAdmin):
#     list_display = ('title','id',"time_create","published")
    #prepopulated_fields = {"slug" : ("title",)}


admin.site.register(Jobs)
admin.site.register(Company)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(Review)
admin.site.register(TextEntry)
admin.site.register(Application)





