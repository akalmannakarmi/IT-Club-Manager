from django.contrib import admin
from .models import Skill, Course, Batch, Profile

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('userId', 'name', 'courseId', 'batchId')
    list_filter = ('userId', 'courseId', 'batchId')
    search_fields = ('userId__username', 'name')
    filter_horizontal = ('skills',)
