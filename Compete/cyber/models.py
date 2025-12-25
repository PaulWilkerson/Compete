from django.db import models

class NewCyberChallenge(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    DIFFICULTY_LEVELS = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    difficulty = models.CharField(choices=DIFFICULTY_LEVELS, max_length=10, default='Easy')
    CATEGORY_CHOICES = [
        ('Red Team', 'Red Team'),
        ('Blue Team', 'Blue Team'),
        ('Miscellaneous', 'Miscellaneous'),
    ]
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, default='Miscellaneous')
    flag = models.CharField(max_length=100)

    def __str__(self):
        return self.title