# myapp/models.py
from django.db import models
from django.contrib.auth.models import User as DjangoUser

class UserProfile(models.Model):
    """
    Модель пользователя с дополнительной информацией
    """
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    hashed_password = models.CharField(max_length=255)  # Хранение пароля в открытом виде - НЕ рекомендуется

    def __str__(self):
        return self.user.username

class Hospital(models.Model):
    """
    Модель больницы
    """
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

class HospitalRepresentative(models.Model):
    """
    Модель представителя больницы
    """
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    hospitals = models.ManyToManyField(Hospital)

    def __str__(self):
        return self.user_profile.user.username

class Review(models.Model):
    """
    Модель отзыва
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.hospital}"

class Appointment(models.Model):
    """
    Модель записи на прием
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.hospital} - {self.appointment_date}"

class PatientCard(models.Model):
    """
    Модель карточки пациента
    """
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=5, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user_profile.user.username