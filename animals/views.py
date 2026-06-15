from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import (
    Animal,
    Adopter,
    Vet,
    Medication,
    AnimalHealthRecord,
    ContactMessage,
    VetChatMessage,
)
from .forms import (
    AnimalForm,
    AdopterForm,
    VetForm,
    MedicationForm,
    HealthRecordForm,
    ContactForm,
    ChatMessageForm,
)


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
def dashboard(request):
    records = AnimalHealthRecord.objects.select_related('animal', 'animal__breed').order_by('recorded_at')
    breed_date_stats = {}

    for record in records:
        breed_label = record.animal.breed_text or (record.animal.breed.name if record.animal.breed else 'Non renseigné')
        date_label = record.recorded_at.isoformat()
        if breed_label not in breed_date_stats:
            breed_date_stats[breed_label] = {}
        if date_label not in breed_date_stats[breed_label]:
            breed_date_stats[breed_label][date_label] = {'weight_total': 0.0, 'height_total': 0.0, 'count': 0}
        breed_date_stats[breed_label][date_label]['weight_total'] += float(record.weight)
        breed_date_stats[breed_label][date_label]['height_total'] += float(record.height)
        breed_date_stats[breed_label][date_label]['count'] += 1

    weight_series = []
    height_series = []
    for breed_label, date_stats in breed_date_stats.items():
        sorted_dates = sorted(date_stats.keys())
        weight_series.append({
            'label': breed_label,
            'data': [
                {'x': date, 'y': round(date_stats[date]['weight_total'] / date_stats[date]['count'], 1)}
                for date in sorted_dates
            ],
            'fill': False,
        })
        height_series.append({
            'label': breed_label,
            'data': [
                {'x': date, 'y': round(date_stats[date]['height_total'] / date_stats[date]['count'], 1)}
                for date in sorted_dates
            ],
            'fill': False,
        })

    context = {
        'title': 'Tableau de bord santé',
        'weight_series': json.dumps(weight_series, ensure_ascii=False),
        'height_series': json.dumps(height_series, ensure_ascii=False),
        'chart_available': bool(weight_series or height_series),
        'record_count': records.count(),
        'vet_count': Vet.objects.count(),
        'medication_count': Medication.objects.count(),
        'recent_records': records[:10],
    }
    return render(request, 'animals/dashboard.html', context)


@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre message a bien été envoyé. Nous reviendrons vers vous rapidement.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'animals/contact.html', {
        'form': form,
        'title': 'Contactez le refuge'
    })


@login_required
def chat_list(request):
    vets = Vet.objects.filter(active=True)
    recent_messages = VetChatMessage.objects.select_related('vet').order_by('-created_at')[:10]
    return render(request, 'animals/chat_list.html', {
        'vets': vets,
        'recent_messages': recent_messages,
        'title': 'Discussion avec le vétérinaire'
    })


@login_required
def chat_thread(request, vet_id):
    vet = get_object_or_404(Vet, pk=vet_id)
    chat_messages = VetChatMessage.objects.filter(vet=vet).order_by('created_at')

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.vet = vet
            message.user = request.user
            message.sender_name = request.user.username
            message.is_from_vet = False
            message.save()
            messages.success(request, 'Message envoyé au vétérinaire.')
            return redirect('chat_thread', vet_id=vet.id)
    else:
        form = ChatMessageForm()

    return render(request, 'animals/chat_thread.html', {
        'vet': vet,
        'chat_messages': chat_messages,
        'form': form,
        'title': f'Discussion avec {vet.name}'
    })


@login_required
def chat_message_edit(request, message_id):
    message = get_object_or_404(VetChatMessage, pk=message_id)
    
    # Only the original sender can edit
    if message.user != request.user:
        messages.error(request, 'Vous ne pouvez pas modifier ce message.')
        return redirect('chat_thread', vet_id=message.vet.id)
    
    if request.method == 'POST':
        form = ChatMessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message modifié avec succès.')
            return redirect('chat_thread', vet_id=message.vet.id)
    else:
        form = ChatMessageForm(instance=message)
    
    return render(request, 'animals/chat_message_form.html', {
        'form': form,
        'message': message,
        'title': 'Modifier le message'
    })


@login_required
def chat_message_delete(request, message_id):
    message = get_object_or_404(VetChatMessage, pk=message_id)
    vet = message.vet
    
    # Only the original sender can delete
    if message.user != request.user:
        messages.error(request, 'Vous ne pouvez pas supprimer ce message.')
        return redirect('chat_thread', vet_id=vet.id)
    
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message supprimé avec succès.')
        return redirect('chat_thread', vet_id=vet.id)
    
    return render(request, 'animals/chat_message_confirm_delete.html', {
        'message': message,
        'title': 'Supprimer le message'
    })


@login_required
def health_record_list(request):
    records = AnimalHealthRecord.objects.select_related('animal').all()
    return render(request, 'animals/health_record_list.html', {
        'records': records,
        'title': 'Suivi santé des animaux'
    })


@login_required
def health_record_add(request):
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fiche de santé enregistrée avec succès !')
            return redirect('health_record_list')
    else:
        form = HealthRecordForm()
    return render(request, 'animals/health_record_form.html', {
        'form': form,
        'title': 'Ajouter une fiche de santé'
    })


@login_required
def vet_list(request):
    vets = Vet.objects.all()
    return render(request, 'animals/vet_list.html', {
        'vets': vets,
        'title': 'Équipe vétérinaire'
    })


@login_required
def vet_add(request):
    if request.method == 'POST':
        form = VetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vétérinaire ajouté avec succès !')
            return redirect('vet_list')
    else:
        form = VetForm()
    return render(request, 'animals/vet_form.html', {
        'form': form,
        'title': 'Ajouter un vétérinaire'
    })


@login_required
def vet_edit(request, pk):
    vet = get_object_or_404(Vet, pk=pk)
    if request.method == 'POST':
        form = VetForm(request.POST, instance=vet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fiche vétérinaire mise à jour !')
            return redirect('vet_list')
    else:
        form = VetForm(instance=vet)
    return render(request, 'animals/vet_form.html', {
        'form': form,
        'title': 'Modifier un vétérinaire'
    })


@login_required
def pharmacy_list(request):
    medicines = Medication.objects.all()
    return render(request, 'animals/pharmacy_list.html', {
        'medicines': medicines,
        'title': 'Pharmacie'
    })


@login_required
def medication_add(request):
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit ajouté à la pharmacie !')
            return redirect('pharmacy_list')
    else:
        form = MedicationForm()
    return render(request, 'animals/pharmacy_form.html', {
        'form': form,
        'title': 'Ajouter un produit'
    })


@login_required
def medication_edit(request, pk):
    medicine = get_object_or_404(Medication, pk=pk)
    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit mis à jour !')
            return redirect('pharmacy_list')
    else:
        form = MedicationForm(instance=medicine)
    return render(request, 'animals/pharmacy_form.html', {
        'form': form,
        'title': 'Modifier un produit'
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