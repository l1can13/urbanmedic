import json

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.models import Doctor, Patient, Exercise


def api(request):
    return HttpResponse('<h1>API page</h1>')


class DoctorView(View):
    def get(self, request, pk=None):
        template = 'api/html/doctor.html'

        if pk is not None:
            doctors = get_object_or_404(Doctor, pk=pk)

            template = 'api/html/doctor_exercises.html' \
                if request.path.endswith('exercises/') \
                else template
        else:
            doctors = Doctor.objects.all()

        return render(
            request,
            template,
            context={'doctors': doctors if isinstance(doctors, QuerySet) else [doctors]}
        )

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            doctor = Doctor(
                name=data['name'],
                speciality_id=data['speciality']
            )

            doctor.full_clean()
            doctor.save()

            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Доктор успешно создан.'
                }
            )
        except ValidationError as e:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': str(e)
                },
                status=400
            )

    def put(self, request, pk):
        try:
            data = json.loads(request.body.decode('utf-8'))
            doctor = get_object_or_404(Doctor, pk=pk)
            doctor.name = data['name']
            doctor.speciality_id = data['speciality']

            doctor.full_clean()
            doctor.save()

            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Доктор успешно обновлен.'
                }
            )
        except ValidationError as e:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': str(e)
                },
                status=400
            )

    def patch(self, request, pk):
        try:
            data = json.loads(request.body.decode('utf-8'))
            doctor = get_object_or_404(Doctor, pk=pk)
            if 'name' in data:
                doctor.name = data['name']
            if 'speciality' in data:
                doctor.speciality_id = data['speciality']

            doctor.full_clean()
            doctor.save()

            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Доктор успешно обновлен.'
                }
            )
        except ValidationError as e:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': str(e)
                },
                status=400
            )

    def delete(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        doctor.delete()

        return JsonResponse(
            {
                'status': 'success',
                'message': 'Доктор успешно удален.'
            }
        )


class PatientView(View):
    def get(self, request, pk=None):
        template = 'api/html/patient.html'

        if pk is not None:
            patients = get_object_or_404(Patient, pk=pk)

            template = 'api/html/patient_exercises.html' \
                if request.path.endswith('exercises/') \
                else template
        else:
            patients = Patient.objects.all()

        return render(
            request,
            template,
            context={'patients': patients if isinstance(patients, QuerySet) else [patients]}
        )

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            patient = Patient(
                name=data['name']
            )

            patient.full_clean()
            patient.save()

            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Пациент успешно создан.'
                }
            )
        except ValidationError as e:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': str(e)
                },
                status=400
            )

    def put(self, request, pk):
        try:
            data = json.loads(request.body.decode('utf-8'))
            patient = get_object_or_404(Patient, pk=pk)
            patient.name = data['name']

            patient.full_clean()
            patient.save()

            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Пациент успешно обновлен.'
                }
            )
        except ValidationError as e:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': str(e)
                },
                status=400
            )

    def patch(self, request, pk):
        try:
            data = json.loads(request.body.decode('utf-8'))
            patient = get_object_or_404(Patient, pk=pk)
            if 'name' in data:
                patient.name = data['name']

            patient.full_clean()
            patient.save()

            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Пациент успешно обновлен.'
                }
            )
        except ValidationError as e:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': str(e)
                },
                status=400
            )

    def delete(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        patient.delete()

        return JsonResponse(
            {
                'status': 'success',
                'message': 'Пациент успешно удален.'
            }
        )


class ExerciseView(View):
    def get(self, request, pk=None):
        template = 'api/html/exercise.html'

        if pk is not None:
            exercises = get_object_or_404(Exercise, pk=pk)
        else:
            exercises = Exercise.objects.all()

        return render(
            request,
            template,
            context={'exercises': exercises if isinstance(exercises, QuerySet) else [exercises]}
        )

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            exercise = Exercise(
                title=data['title'],
                description=data['description'],
                frequency=data['frequency']
            )

            exercise.full_clean()
            exercise.save()

            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Упражнение успешно создано.'
                }
            )
        except ValidationError as e:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': str(e)
                },
                status=400
            )

    def put(self, request, pk):
        try:
            data = json.loads(request.body.decode('utf-8'))
            exercise = get_object_or_404(Exercise, pk=pk)
            exercise.title = data['title']
            exercise.description = data['description']
            exercise.frequency = data['frequency']

            exercise.full_clean()
            exercise.save()

            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Упражнение успешно обновлено.'
                }
            )
        except ValidationError as e:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': str(e)
                },
                status=400
            )

    def patch(self, request, pk):
        try:
            data = json.loads(request.body.decode('utf-8'))
            exercise = get_object_or_404(Exercise, pk=pk)
            if 'title' in data:
                exercise.title = data['title']
            if 'description' in data:
                exercise.description = data['description']
            if 'frequency' in data:
                exercise.frequency = data['frequency']

            exercise.full_clean()
            exercise.save()

            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Упражнение успешно обновлено.'
                }
            )
        except ValidationError as e:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': str(e)
                },
                status=400
            )

    def delete(self, request, pk):
        exercise = get_object_or_404(Exercise, pk=pk)
        exercise.delete()

        return JsonResponse(
            {
                'status': 'success',
                'message': 'Упражнение успешно удалено.'
            }
        )
