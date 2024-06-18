from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, RecipeForm
from .models import Recipe
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'recipes/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'recipes/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('recipe_list')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'recipes/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('recipes/logout.html')

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.created_by = request.user
            new_recipe.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})