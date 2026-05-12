from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Animal, Adopter
from .forms import AnimalForm, AdopterForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, 'Inscription réussie ! Bienvenue !')
            return redirect('animal_list')
        else:
            messages.error(request, 'Erreur lors de l’inscription. Veuillez corriger les erreurs ci-dessous.')
    else:
        form = UserCreationForm()
    return render(request, 'animals/register.html', {'form': form})

def login_view(request):
    next_url = request.POST.get('next') or request.GET.get('next')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {username} !')
            if next_url:
                return redirect(resolve_url(next_url))
            return redirect('animal_list')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    
    return render(request, 'animals/login.html', {'next': next_url})

def logout_view(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('login')


@login_required
def animal_add(request):
    
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Animal ajouté avec succès !')
            return redirect('animal_list')
    else:
        form = AnimalForm()
    
    return render(request, 'animals/animal_add.html', {
        'form': form,
        'title': 'Ajouter un animal'
    })


@login_required
def animal_edit(request, pk):
    """UPDATE - Edit an existing animal"""
    animal = get_object_or_404(Animal, pk=pk)
    
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES, instance=animal)  # Ajouter request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'Animal modifié avec succès !')
            return redirect('animal_list')
    else:
        form = AnimalForm(instance=animal)
    
    return render(request, 'animals/animal_edit.html', {
        'form': form,
        'animal': animal,
        'title': "Modifier l'animal"
    })

@login_required
def animal_delete(request, pk):
    """DELETE - Remove an animal"""
    animal = get_object_or_404(Animal, pk=pk)
    
    if request.method == 'POST':
        animal_name = animal.name
        animal.delete()
        messages.success(request, f'{animal_name} a été supprimé du refuge.')
        return redirect('animal_list')
    
    return render(request, 'animals/animal_confirm_delete.html', {
        'animal': animal,
        'title': 'Supprimer l\'animal'
    })

@login_required
def animal_list(request):
    """READ - Display all animals"""
    query = request.GET.get('q', '')
    animals = Animal.objects.all()
    
    if query:
        animals = animals.filter(
            models.Q(name__icontains=query) |
            models.Q(breed__name__icontains=query) |
            models.Q(breed_text__icontains=query) |
            models.Q(species__icontains=query)
        )
    
    stats = {
        'total': animals.count(),
        'available': animals.filter(status='available').count(),
        'adopted': animals.filter(status='adopted').count(),
        'medical': animals.filter(status='medical').count(),
    }
    return render(request, 'animals/animal_list.html', {
        'animals': animals,
        'stats': stats,
        'title': 'Liste des animaux',
        'query': query
    })


@login_required
def adopter_list(request):
    adopters = Adopter.objects.select_related('animal').all()
    return render(request, 'animals/adopter_list.html', {
        'adopters': adopters,
        'title': 'Liste des adoptants'
    })


@login_required
def adopter_add(request):
    if request.method == 'POST':
        form = AdopterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Demande d’adoption enregistrée avec succès !')
            return redirect('adopter_list')
    else:
        form = AdopterForm()
    return render(request, 'animals/adopter_add.html', {
        'form': form,
        'title': 'Ajouter un nouvel adoptant'
    })


@login_required
def adopter_edit(request, pk):
    adopter = get_object_or_404(Adopter, pk=pk)
    if request.method == 'POST':
        form = AdopterForm(request.POST, instance=adopter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Adoptant modifié avec succès !')
            return redirect('adopter_list')
    else:
        form = AdopterForm(instance=adopter)
    return render(request, 'animals/adopter_add.html', {
        'form': form,
        'title': 'Modifier un adoptant'
    })


@login_required
def adopter_delete(request, pk):
    adopter = get_object_or_404(Adopter, pk=pk)
    if request.method == 'POST':
        adopter_name = adopter.name
        adopter.delete()
        messages.success(request, f'Adoption de {adopter_name} supprimée avec succès.')
        return redirect('adopter_list')
    return render(request, 'animals/adopter_confirm_delete.html', {
        'adopter': adopter,
        'title': 'Supprimer une adoption'
    })