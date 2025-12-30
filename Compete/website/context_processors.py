from .models import SolvedChallenge
from django.contrib.auth.models import User

def user_rank(request):
    """
    Context processor to add user's rank to all templates
    """
    if request.user.is_authenticated:
        # Get all users with their total points
        users_with_points = []
        all_users = User.objects.all()
        
        for user in all_users:
            solved_challenges = SolvedChallenge.objects.filter(user=user)
            total_points = sum(challenge.points for challenge in solved_challenges)
            
            if total_points > 0:  # Only include users who have earned points
                users_with_points.append({
                    'user': user,
                    'total_points': total_points,
                })
        
        # Sort by points (descending)
        users_with_points.sort(key=lambda x: x['total_points'], reverse=True)
        
        # Find current user's rank
        current_user_rank = None
        for i, user_data in enumerate(users_with_points):
            if user_data['user'] == request.user:
                current_user_rank = i + 1
                break
        
        return {'user_rank': current_user_rank}
    
    return {'user_rank': None}
