from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
import uuid
import math
from django.utils import timezone

# Create your models here.


# ----------------------
# Custom Username Validator
# ----------------------
custom_username_validator = RegexValidator(
    regex=r'^[\w.@+\- ]+$',
    message='Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_/space characters.'
)


# ----------------------
# Profile (instead of User)
# ----------------------
class Profile(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[custom_username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    departement = models.CharField(max_length=100, null=True, blank=True, default='')
    extension = models.CharField(max_length=20, null=True, blank=True, default='')
    district_name = models.CharField(max_length=50, null=True, blank=True, default='')
    title = models.CharField(max_length=200, null=True, blank=True, default='')
    description_dpt = models.CharField(max_length=400, null=True, blank=True, default='')
    employeeId = models.CharField(max_length=50, blank=True, null=True)

    ROLE_CHOICES = [
        ("admin", "Administrateur"),
        ("responsable", "Responsable Département"),
        ("technicien", "Technicien"),
        ("chef_service", "Chef Service Maintenance"),
        ("directeur", "Directeur Informatique"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


# ----------------------
# Matériel
# ----------------------
class Materiel(models.Model):
    categorie = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    fournisseur = models.CharField(max_length=100)
    date_garantie = models.DateField()
    num_contrat = models.CharField(max_length=100)

    def __str__(self):
        return self.modele


# ----------------------
# Demande Intervention
# ----------------------
class DemandeIntervention(models.Model):
    date_demande = models.DateField()
    date_validation = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=100)
    description = models.TextField()
    etat = models.CharField(max_length=50)
    commentaire = models.TextField(blank=True, null=True)
    lieu_intervention = models.CharField(max_length=255)
    departement = models.CharField(max_length=100)

    demandeur = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="demandes")
    technicien = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="interventions")

    def __str__(self):
        return f"{self.type} - {self.date_demande}"


# ----------------------
# Notification
# ----------------------
class Notification(models.Model):
    message = models.TextField()
    type = models.CharField(max_length=50)
    date_notif = models.DateTimeField(auto_now_add=True)

    destinataire = models.ForeignKey(Profile, on_delete=models.CASCADE)
    demande = models.ForeignKey(DemandeIntervention, on_delete=models.CASCADE)

    def __str__(self):
        return self.message


# ----------------------
# Fiche Intervention
# ----------------------
class FicheIntervention(models.Model):
    date = models.DateField()
    heure = models.TimeField()
    reference_pr = models.CharField(max_length=100)

    montant = models.FloatField()
    montant_mo_ht = models.FloatField()
    montant_mo_ttc = models.FloatField()

    email = models.EmailField()
    commentaire = models.TextField()

    demande = models.OneToOneField(DemandeIntervention, on_delete=models.CASCADE)

    def __str__(self):
        return f"Fiche {self.id}"


# ----------------------
# Prestations
# ----------------------
class PrestationInterne(models.Model):
    fiche = models.OneToOneField(FicheIntervention, on_delete=models.CASCADE)

    entree_atelier = models.DateField()
    debut_travaux = models.DateField()
    fin_travaux = models.DateField()
    travaux_effectues = models.TextField()


class PrestationExterne(models.Model):
    fiche = models.OneToOneField(FicheIntervention, on_delete=models.CASCADE)

    reference_contrat = models.CharField(max_length=100)


# ----------------------
# Rapport d'activité
# ----------------------
class RapportActivite(models.Model):
    date_rapport = models.DateField()
    fiche = models.ForeignKey(FicheIntervention, on_delete=models.CASCADE)


# ----------------------
# Fiche de suivi indicateurs
# ----------------------
class FicheSuivi(models.Model):
    fiche = models.ForeignKey(FicheIntervention, on_delete=models.CASCADE)

    processus = models.CharField(max_length=100)
    objectif = models.CharField(max_length=255)
    indicateurs = models.TextField()
    periodicite = models.CharField(max_length=50)
    commentaire = models.TextField()
    actions = models.TextField()
    date_suivi = models.DateField()