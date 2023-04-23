from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import Movie, Profile, UserProfile
from .forms import LoginForm, ProfileForm
from django.views import generic


class RegisterView(generic.CreateView):
    form_class = UserForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')


def login_request(request):
    context = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password1')
        user = authenticate(email=email, password=password)
        print(email)
        print(password)
        print(form)
        if form.is_valid():
            login(request, user)
            messages.success(request, "Logged In")
            return reverse_lazy('profile_list')
        else:
            print(user)
            print("form invalid")
            form = LoginForm()
            context['login_form'] = form
            return render(request, "registration/login.html", context)
    else:
        print("no post")
        form = LoginForm()
        context['login_form'] = form
        return render(request, "registration/login.html", context)


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return reverse_lazy('start_view')


def start_view(request):
    if request.user.is_authenticated:
        return redirect('my_video_platform:profile_list')
    else:
        return render(request, 'mainpage.html', {})


@method_decorator(login_required, name='dispatch')
class ProfileList(View):

    def get(self, request, *args, **kwargs):
        profiles = request.user.profiles.all()
        print('ESTONIA')
        print(profiles)

        return render(request, 'profileList.html', {
            'profiles': profiles
        })


@method_decorator(login_required, name='dispatch')
class ProfileCreate(View):

    def get(self, request, *args, **kwargs):
        form = ProfileForm()
        print('GRECJA')
        return render(request, 'profileCreate.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        print('ATENY')
        if form.is_valid():
            print(form.cleaned_data)
            print('MOSKWA')
            profile = Profile.objects.create(**form.cleaned_data)
            print(profile)
            if profile:
                print(form.cleaned_data)
                request.user.profiles.add(profile)
                return redirect(f'/watch/{profile}')
        else:
            print(form.errors)
            print(form.cleaned_data)
        return render(request, 'profileCreate.html', {
            'form': form
        })

@method_decorator(login_required, name='dispatch')
class Watch(View):
    def get(self, request, profile_id, *args, **kwargs):
        print('TURYN')
        print(profile_id)
        try:
            profile = Profile.objects.get(id=profile_id)

            movies = Movie.objects.filter(profile_type=profile.profile_type)

            try:
                showcase = movies[0]
            except:
                showcase = None

            if profile not in request.user.profiles.all():
                return redirect(to='profile_list')
            else:
                return render(request, 'movieList.html', {
                    'movies': movies,
                    'show_case': showcase
                })
        except Profile.DoesNotExist:
            return redirect(to='profile_list')


@method_decorator(login_required, name='dispatch')
class ShowMovieDetail(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:

            movie = Movie.objects.get(id=movie_id)

            return render(request, 'movieDetail.html', {
                'movie': movie
            })
        except Movie.DoesNotExist:
            return redirect('profile_list')


@method_decorator(login_required, name='dispatch')
class ShowMovie(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:

            movie = Movie.objects.get(id=movie_id)

            movie = movie.videos.values()

            return render(request, 'showMovie.html', {
                'movie': list(movie)
            })
        except Movie.DoesNotExist:
            return redirect('profile_list')
