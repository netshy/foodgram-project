from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import redirect, render


from foodgram import settings
from .forms import CreationForm
from .utils import anonymous_required


@anonymous_required
def signup(request):
    form = CreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        email = form.cleaned_data['email']
        send_mail_ls(email)

        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')
    return render(request, 'signup.html', {'form': form})


def send_mail_ls(email):
    send_mail(
        'Подтверждение регистрации FoodGram', 'Вы зарегистрированы!',
        f'FoodGram.tk <{settings.EMAIL_HOST_USER}>', [email],
        fail_silently=False
    )
