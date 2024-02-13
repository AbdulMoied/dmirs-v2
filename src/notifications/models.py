from django.db import models


class Notification(models.Model):
    heading = models.CharField(max_length=30, verbose_name="Notification Heading")
    content = models.CharField(max_length=200, verbose_name="Notification Content")
    viewed = models.BooleanField(default=False, verbose_name="Notification Viewed")
    status = models.BooleanField(default=True, verbose_name="Notification Status")
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Notification Created On")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Notification Last Updated")

    def __str__(self):
        return f"{self.heading}"

    class Meta:
        verbose_name_plural = 'Notification Management'
        
class NotificationStatistics(models.Model):
    project_count = models.IntegerField(default=0, verbose_name="Project Count")
    client_count = models.IntegerField(default=0, verbose_name="Client Count")
    # Add more fields as needed
    
    def __str__(self):
        return "Notification Statistics"

    class Meta:
        verbose_name_plural = 'Notification Statistics'