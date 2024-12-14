from django.contrib import admin
from django.utils import timezone
from .models import TodoItem, TodoStatus

@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    """
    Custom Admin configuration for TodoItem model
    """
    # Fieldsets for better organization
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'tag')
        }),
        ('Status and Timing', {
            'fields': ('status', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    # Readonly fields for timestamps
    readonly_fields = ('created_at', 'updated_at')

    # List display for changelist view
    list_display = (
        'title', 
        'status', 
        'due_date', 
        'tag', 
        'created_at', 
        'is_overdue'
    )

    # Filters for easy navigation
    list_filter = (
        'status', 
        ('due_date', admin.DateFieldListFilter),
        ('created_at', admin.DateFieldListFilter)
    )

    # Search fields
    search_fields = ('title', 'description', 'tag')

    def is_overdue(self, obj):
        """
        Custom method to highlight overdue tasks
        """
        return (obj.due_date and obj.due_date < timezone.now() and 
                obj.status not in [TodoStatus.COMPLETED, TodoStatus.CANCELLED])
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'

    # Custom action to mark selected tasks as completed
    @admin.action(description='Mark selected tasks as completed')
    def mark_completed(modeladmin, request, queryset):
        queryset.update(status=TodoStatus.COMPLETED)

    # Custom action to mark selected tasks as cancelled
    @admin.action(description='Cancel selected tasks')
    def mark_cancelled(modeladmin, request, queryset):
        queryset.update(status=TodoStatus.CANCELLED)

    # Add actions
    actions = [mark_completed, mark_cancelled]