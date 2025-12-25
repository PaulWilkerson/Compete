from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    website = models.CharField(max_length=90)
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    about = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

class SolvedChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solved_challenges')
    challenge_type = models.CharField(max_length=20)  # 'cli', 'cyber', or 'programming'
    challenge_id = models.IntegerField()
    challenge_title = models.CharField(max_length=200)
    points = models.IntegerField(default=100)
    solved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'challenge_type', 'challenge_id')
        ordering = ['-solved_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge_title}"
