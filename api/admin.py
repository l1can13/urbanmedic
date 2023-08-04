from django.contrib import admin

from api.models import Speciality, Exercise, Patient, Doctor, Appointment

admin.register(Speciality)
admin.register(Exercise)
admin.register(Patient)
admin.register(Doctor)
admin.register(Appointment)
