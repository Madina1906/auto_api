from django.db import models
from django.contrib.auth.models import User

class AutoPlate(models.Model):
    plate_number = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    deadline = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plates_created', limit_choices_to={'is_staff': True})
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.plate_number

class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    plate = models.ForeignKey(AutoPlate, on_delete=models.CASCADE, related_name='bids')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'plate')  

    def __str__(self):
        return f"{self.user.username} - {self.amount} on {self.plate.plate_number}"

