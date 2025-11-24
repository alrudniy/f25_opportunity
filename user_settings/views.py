from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserSettingsForm
from .models import UserSettings

@login_required
def settings_view(request):
    # get_or_create handles users that existed before the settings app was added
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            return redirect('user_settings:settings')
    else:
        form = UserSettingsForm(instance=user_settings)
    
    return render(request, 'user_settings/settings.html', {'form': form})
