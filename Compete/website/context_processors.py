from .models import SolvedChallenge
from django.contrib.auth.models import User
from django.db.models import Sum

def user_rank(request):
    """
    Context processor to add user's rank to all templates
    """
    if request.user.is_authenticated:
        # Get all users with their total points using aggregation
        users_with_points = User.objects.annotate(
            total_points=Sum('solved_challenges__points')
        ).filter(
            total_points__gt=0
        ).order_by('-total_points', 'id')  # Secondary sort by id for deterministic ordering
        
        # Find current user's rank
        current_user_rank = None
        for i, user in enumerate(users_with_points):
            if user == request.user:
                current_user_rank = i + 1
                break
        
        return {'user_rank': current_user_rank}
    
    return {'user_rank': None}
