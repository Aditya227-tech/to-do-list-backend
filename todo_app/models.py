from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils import timezone

class TodoStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    WORKING = 'WORKING', 'Working'
    PENDING_REVIEW = 'PENDING_REVIEW', 'Pending Review'
    COMPLETED = 'COMPLETED', 'Completed'
    OVERDUE = 'OVERDUE', 'Overdue'
    CANCELLED = 'CANCELLED', 'Cancelled'

class TodoItem(models.Model):
    """
    Model representing a Todo item with comprehensive tracking
    """
    # Timestamp (auto-set, not editable)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    # Title (max 100 chars, mandatory)
    title = models.CharField(
        max_length=100, 
        validators=[
            MinLengthValidator(1, "Title cannot be empty"),
            MaxLengthValidator(100, "Title cannot exceed 100 characters")
        ]
    )

    # Description (max 1000 chars, mandatory)
    description = models.TextField(
        validators=[
            MinLengthValidator(1, "Description cannot be empty"),
            MaxLengthValidator(1000, "Description cannot exceed 1000 characters")
        ]
    )

    # Due Date (optional)
    due_date = models.DateTimeField(null=True, blank=True)

    # Tag (optional, unique per entry)
    tag = models.SlugField(
        max_length=50, 
        unique=True, 
        null=True, 
        blank=True
    )

    # Status (default OPEN, mandatory)
    status = models.CharField(
        max_length=20,
        choices=TodoStatus.choices,
        default=TodoStatus.OPEN
    )

    def save(self, *args, **kwargs):
        """
        Override save method to handle status updates
        """
        # Auto-update status to OVERDUE if due date has passed
        if self.due_date and self.due_date < timezone.now() and self.status not in [
            TodoStatus.COMPLETED, 
            TodoStatus.CANCELLED
        ]:
            self.status = TodoStatus.OVERDUE

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.status}"

    class Meta:
        verbose_name = "Todo Item"
        verbose_name_plural = "Todo Items"
        ordering = ['-created_at']