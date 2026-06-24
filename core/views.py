from django.shortcuts import render, redirect, get_object_or_404
from .models import Pet, AdoptionRequest, FavoritePet
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import PetForm

def home(request):
    pet_type = request.GET.get('type')
    query = request.GET.get('q')
    
    pets = Pet.objects.filter(is_adopted=False)
    
    if pet_type:
        pets = pets.filter(pet_type=pet_type)
        
    if query:
        pets = pets.filter(
            Q(name__icontains=query) | 
            Q(breed__icontains=query) | 
            Q(location__icontains=query)
        )
        
    # Check favorites if user is authenticated
    if request.user.is_authenticated:
        favorites = FavoritePet.objects.filter(user=request.user).values_list('pet_id', flat=True)
    else:
        favorites = []
        
    return render(request, 'home.html', {'pets': pets, 'favorites': favorites, 'search_query': query})

@login_required
def adopt_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    # Check if request already exists
    exists = AdoptionRequest.objects.filter(user=request.user, pet=pet).exists()
    if not exists:
        AdoptionRequest.objects.create(user=request.user, pet=pet)
    return redirect('dashboard')

@login_required
def upload_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES) # request.FILES zaroori hai photo ke liye
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, "Pet uploaded successfully! Ab ye home page par dikhega.")
            return redirect('home')
    else:
        form = PetForm()
    return render(request, 'upload_pet.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    all_requests = AdoptionRequest.objects.all().order_by('-request_date')
    return render(request, 'admin_panel.html', {'all_requests': all_requests})

@login_required
def update_status(request, req_id, status):
    if request.user.is_staff:
        req = get_object_or_404(AdoptionRequest, id=req_id)
        req.status = status
        req.save()
        
        # Agar approve hua toh pet ko 'Adopted' mark karo
        if status == 'Approved':
            req.pet.is_adopted = True
            req.pet.save()
            
    return redirect('admin_dashboard')

# core/views.py

# This first dashboard view definition is removed.
# It is merged into the second one below.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Register hote hi login kar do
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please check the details.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login Logic
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout Logic
def logout_view(request):
    logout(request)
    return redirect('home')

def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoritePet.objects.filter(user=request.user, pet=pet).exists()
    return render(request, 'pet_detail.html', {'pet': pet, 'is_favorite': is_favorite})
@login_required
def dashboard(request):
    # User ke apne pets
    user_pets = Pet.objects.filter(owner=request.user)
    
    # User ki requests
    user_requests = AdoptionRequest.objects.filter(user=request.user)
    
    # User ke favorites
    favorite_pets = FavoritePet.objects.filter(user=request.user)
    
    # Stats calculate karna
    total_uploads = user_pets.count()
    active_listings = user_pets.filter(is_adopted=False).count()
    adopted_count = user_pets.filter(is_adopted=True).count()
    
    context = {
        'user_pets': user_pets,
        'requests': user_requests,
        'favorite_pets': favorite_pets,
        'total_uploads': total_uploads,
        'active_listings': active_listings,
        'adopted_count': adopted_count,
    }
    return render(request, 'dashboard.html', context)

@login_required
def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user) # Security: Dusre ka pet edit na ho
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PetForm(instance=pet)
    return render(request, 'upload_pet.html', {'form': form, 'edit_mode': True})

@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    if request.method == 'POST':
        pet.delete()
        return redirect('dashboard')
    return render(request, 'delete_confirm.html', {'pet': pet})


@login_required
def mark_as_adopted(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    pet.is_adopted = True
    pet.save()
    return redirect('dashboard')

@login_required
def toggle_favorite(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    favorite, created = FavoritePet.objects.get_or_create(user=request.user, pet=pet)
    if not created:
        favorite.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def success_stories(request):
    pets = Pet.objects.filter(is_adopted=True)
    return render(request, 'success_stories.html', {'pets': pets})
