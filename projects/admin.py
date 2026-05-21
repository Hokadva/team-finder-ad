from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'owner', 'created_at', 'status', 'github_url',
        'get_participants')
    list_filter = ('status', )
    search_fields = ('name', 'owner__email', 'participants__email')

    @admin.display(description='Участники')
    def get_participants(self, obj):
        return obj.participants.count()
