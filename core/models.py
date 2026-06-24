from django.db import models
from django.contrib.auth.models import User

# Class ka naam 'Pet' hona chahiye (P capital)
class Pet(models.Model):
    PET_TYPES = [('Dog', 'Dog'), ('Cat', 'Cat'), ('Rabbit', 'Rabbit')]
    
    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=20, choices=PET_TYPES)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='pet_images/')
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, default="91xxxxxxxx") # Contact ke liye
    owner_name = models.CharField(max_length=100, default="Anonymous") # Name ke liye
    is_adopted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets', null=True, blank=True)

    def __str__(self):
        return self.name

# AdoptionRequest class bhi check karein
class AdoptionRequest(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.pet.name}"

class FavoritePet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_pets')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pet')

    def __str__(self):
        return f"{self.user.username} likes {self.pet.name}"
