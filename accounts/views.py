from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from daily_card.models import DailyCardDraw

@login_required
def profile_view(request):
    latest_draw = DailyCardDraw.objects.filter(user=request.user).order_by('-drawn_at').first()
    recent_draws = DailyCardDraw.objects.filter(user=request.user).exclude(id=latest_draw.id).order_by('-drawn_at')[:5]

    return render(request, 'accounts/profile.html', {
        'latest_draw': latest_draw,
        'recent_draws': recent_draws,  
    })
