from django.db import models


class Speciality(models.Model):
    title = models.CharField('title', max_length=64)

    def __str__(self):
        return self.title


class Exercise(models.Model):
    EVERY_HOUR = 'every_hour'
    EVERY_DAY = 'every_day'
    EVERY_WEEK = 'every_week'
    EVERY_MONTH = 'every_month'

    EXERCISE_FREQUENCY = [
        (EVERY_HOUR, 'Каждый час'),
        (EVERY_DAY, 'Каждый день'),
        (EVERY_WEEK, 'Каждую неделю'),
        (EVERY_MONTH, 'Каждый месяц'),
    ]

    title = models.CharField('title', max_length=128)
    description = models.CharField('description', max_length=1024)
    frequency = models.CharField(
        'frequency',
        max_length=32,
        choices=EXERCISE_FREQUENCY,
        default=EVERY_DAY
    )
    specialisations = models.ManyToManyField(Speciality)

    def __str__(self):
        return self.title


class Patient(models.Model):
    name = models.CharField('name', max_length=128)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField('name', max_length=128)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    patients = models.ManyToManyField(Patient)

    def __str__(self):
        return f"Имя: {self.name}, " \
               f"Специальность: {self.speciality}"


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField('Дата назначения')

    def __str__(self):
        return f"Доктор: {self.doctor.name}, Пациент: {self.patient.name}, Упражнение: {self.exercise.title}"
