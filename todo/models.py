from django.db import models
from django.utils import timezone
from auth_service.models import UserLogins


class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField(default=timezone.now)
    dead_line = models.DateTimeField()
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(blank=True, null=True)
    priority = models.PositiveIntegerField(default=0)
    user_logins = models.ForeignKey(UserLogins, on_delete=models.CASCADE, related_name="todos")

    def __str__(self):
        return f"{self.title} | {self.user_logins.user.email}"

    class Meta:
        verbose_name = 'Todo'
        verbose_name_plural = 'Todos'
        db_table = 'Todo_DB'
        ordering = ("priority", "start_date")

    def save(self, *args, **kwargs):
        if self.completed:
            self.completed_date = timezone.now()
        super(Todo, self).save()
