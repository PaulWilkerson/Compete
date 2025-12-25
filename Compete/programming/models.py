from django.db import models

class NewProgrammingChallenge(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    DIFFICULTY_LEVELS = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    difficulty = models.CharField(choices=DIFFICULTY_LEVELS, max_length=10, default='Easy')
    CATEGORY_CHOICES = [
        ('Python', 'Python'),
        ('JavaScript', 'JavaScript'),
        ('C++', 'C++'),
        ('Java', 'Java'),
        ('Miscellaneous', 'Miscellaneous'),
    ]
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, default='Miscellaneous')
    flag = models.CharField(max_length=100)

    def __str__(self):
        return self.title