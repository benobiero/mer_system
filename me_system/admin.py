from django.contrib import admin

# Register your models here.
from .models import Grant,Thematic,Name,Frequency,Test,MonthlyTable,Comment

# Register your models here.


admin.site.register(Thematic)

admin.site.register(Name)

admin.site.register(Frequency)

admin.site.register(Test)
admin.site.register(Comment)
@admin.register(Grant)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("project_name", "thematic_area",'project_start','project_end','status')

@admin.register(MonthlyTable)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "activity_list",'unaccomplished_list','reason_list','planned_list','month','project1','lesson')