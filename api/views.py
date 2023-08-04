import json

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import View

from api.models import Doctor, Patient, Exercise, Appointment


def api(request):
    """
    Вью для отображения главной страницы API.

    Parameters:
        request (HttpRequest): Объект запроса от клиента.

    Returns:
        HttpResponse: HTTP-ответ с содержимым '<h1>API page</h1>', которое будет отображено на странице клиента.

    Example:
        Пример использования в URL-маршрутах:
        ```
        urlpatterns = [
            path('', views.api, name='api'),
        ]
        ```
    """
    return HttpResponse('<h1>API page</h1>')


class DoctorView(View):
    """
    Класс представления для работы с доктором.

    """

    def get(self, request, pk=None):
        """
        Обработчик GET-запроса для отображения списка докторов или деталей конкретного доктора.

        Parameters:
            request (HttpRequest): Объект запроса от клиента.
            pk (int, optional): ID доктора. Если указан, то отображаются детали конкретного доктора.

        Returns:
            HttpResponse: HTTP-ответ с отображением списка докторов или деталей конкретного доктора.

        Raises:
            Http404: Если не найден доктор с указанным ID (при запросе деталей конкретного доктора).
        """

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

    def post(self, request, pk=None):
        """
        Обработчик POST-запроса для создания нового доктора или назначения упражнения пациенту.

        Parameters: request (HttpRequest): Объект запроса от клиента. pk (int, optional): ID доктора. Если НЕ указан,
        то создается заданный в body доктор, если УКАЗАН, то происходит назначение упражнения заданному в body пациенту.

        Returns:
            HttpResponse: JSON ответ с успешностью создания доктора или назначения лекарства.

        Raises:
            Http404: Если не найден доктор с указанным ID.
            Http400: Если неверно указаны данные в body.
        """

        if pk is not None and request.path.endswith('appoint/'):
            try:
                data = json.loads(request.body.decode('utf-8'))
                patient_id = data['patient_id']
                exercise_id = data['exercise_id']
                doctor = Doctor.objects.get(pk=pk)
                exercise = Exercise.objects.get(pk=exercise_id)
                patient = Patient.objects.get(pk=patient_id)

                if exercise.specialisations.filter(pk=doctor.speciality.pk).exists():
                    if patient in doctor.patients.all():
                        appointment_exists = Appointment.objects.filter(doctor=doctor, patient=patient,
                                                                        exercise=exercise).exists()
                        if appointment_exists:
                            return JsonResponse(
                                {
                                    'status': 'error',
                                    'message': 'Такое назначение уже существует.'
                                },
                                status=400
                            )
                        else:
                            # Создаем новую запись в таблице Appointment
                            appointment = Appointment(
                                doctor=doctor,
                                patient=patient,
                                exercise=exercise,
                                appointment_date=timezone.now()  # Используем из модуля django.utils.timezone
                            )
                            appointment.full_clean()
                            appointment.save()

                            return JsonResponse(
                                {
                                    'status': 'success',
                                    'message': 'Назначение успешно создано.'
                                }
                            )
                    else:
                        return JsonResponse(
                            {
                                'status': 'error',
                                'message': 'Данный доктор не имеет разрешения назначать упражнения данному пациенту.'
                            },
                            status=400
                        )
                else:
                    return JsonResponse(
                        {
                            'status': 'error',
                            'message': 'Данный доктор не имеет необходимой специальности для назначения этого '
                                       'упражнения.'
                        },
                        status=400
                    )
            except (ValidationError, KeyError) as e:
                return JsonResponse(
                    {
                        'status': 'error',
                        'message': str(e)
                    },
                    status=400
                )

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
        """
        Обработчик PUT-запроса для обновления данных о докторе.

        Parameters:
            request (HttpRequest): Объект запроса от клиента.
            pk (int): ID доктора, которого нужно обновить.

        Returns:
            JsonResponse: JSON-ответ с информацией об успешном обновлении или ошибке.

        Raises:
            Http404: Если не найден доктор с указанным ID.
        """

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
        """
        Обработчик PATCH-запроса для частичного обновления данных о докторе.

        Parameters:
            request (HttpRequest): Объект запроса от клиента.
            pk (int): ID доктора, которого нужно обновить.

        Returns:
            JsonResponse: JSON-ответ с информацией об успешном обновлении или ошибке.

        Raises:
            Http404: Если не найден доктор с указанным ID.

        """

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
        """
        Обработчик DELETE-запроса для удаления доктора.

        Parameters:
            request (HttpRequest): Объект запроса от клиента.
            pk (int): ID доктора, которого нужно удалить.

        Returns:
            JsonResponse: JSON-ответ с информацией об успешном удалении.

        Raises:
            Http404: Если не найден доктор с указанным ID.

        """

        doctor = get_object_or_404(Doctor, pk=pk)
        doctor.delete()

        return JsonResponse(
            {
                'status': 'success',
                'message': 'Доктор успешно удален.'
            }
        )


class PatientView(View):
    """
    Класс представления для работы с пациентом.

    """

    def get(self, request, pk=None):
        """
        Обработчик GET-запроса для получения информации о пациентах.

        Parameters:
            request (HttpRequest): Объект запроса от клиента.
            pk (int, optional): ID пациента, если указан - возвращает информацию о конкретном пациенте.
                                        Если None - возвращает информацию обо всех пациентах.

        Returns:
            HttpResponse: Ответ с отображением информации о пациентах.

        Raises:
            Http404: Если не найден пациент с указанным ID.

        """

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
        """
        Обработчик POST-запроса для создания нового пациента.

        Parameters:
            request (HttpRequest): Объект запроса от клиента.

        Returns:
            JsonResponse: Ответ в формате JSON с результатом операции создания пациента.

        Raises:
            ValidationError: Если данные пациента не прошли валидацию.

        """

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
        """
        Обработчик PUT-запроса для обновления информации о пациенте по его идентификатору.

        Parameters:
            request (HttpRequest): Объект запроса от клиента.
            pk (int): Идентификатор пациента, которого необходимо обновить.

        Returns:
            JsonResponse: Ответ в формате JSON с результатом операции обновления пациента.

        Raises:
            ValidationError: Если данные пациента не прошли валидацию.

        """

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
        """
        Обработчик PATCH-запроса для частичного обновления информации о пациенте по его идентификатору.

        Parameters:
            request (HttpRequest): Объект запроса от клиента.
            pk (int): Идентификатор пациента, которого необходимо обновить.

        Returns:
            JsonResponse: Ответ в формате JSON с результатом операции обновления пациента.

        Raises:
            ValidationError: Если данные пациента не прошли валидацию.

        """

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
        """
        Обработчик DELETE-запроса для удаления пациента по его идентификатору.

        Parameters:
            request (HttpRequest): Объект запроса от клиента.
            pk (int): Идентификатор пациента, которого необходимо удалить.

        Returns:
            JsonResponse: Ответ в формате JSON с результатом операции удаления пациента.

        """

        patient = get_object_or_404(Patient, pk=pk)
        patient.delete()

        return JsonResponse(
            {
                'status': 'success',
                'message': 'Пациент успешно удален.'
            }
        )


class ExerciseView(View):
    """
    Класс представления для работы с упражнением.

    """

    def get(self, request, pk=None):
        """
        Обработчик GET-запроса для получения информации об упражнениях.

        Parameters:
            request (HttpRequest): Объект запроса от клиента.
            pk (int, optional): Идентификатор упражнения. Если передан, то возвращается информация о конкретном
            упражнении, иначе возвращается список всех упражнений.

        Returns:
            HttpResponse or JsonResponse: Ответ с HTML-страницей (если запрошен список упражнений) или JSON-ответом
            с информацией об упражнении (если передан идентификатор упражнения).

        """

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
        """
        Обработчик POST-запроса для создания нового упражнения.

        Parameters:
            request (HttpRequest): Объект запроса от клиента.

        Returns:
            JsonResponse: JSON-ответ с результатом создания упражнения или ошибкой валидации.

        """

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
        """
        Обработчик PUT-запроса для обновления упражнения.

        Parameters:
            request (HttpRequest): Объект запроса от клиента.
            pk (int): Идентификатор упражнения, которое нужно обновить.

        Returns:
            JsonResponse: JSON-ответ с результатом обновления упражнения или ошибкой валидации.

        """

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
        """
        Обработчик PATCH-запроса для частичного обновления упражнения.

        Parameters:
            request (HttpRequest): Объект запроса от клиента.
            pk (int): Идентификатор упражнения, которое нужно обновить.

        Returns:
            JsonResponse: JSON-ответ с результатом частичного обновления упражнения или ошибкой валидации.

        """

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
        """
        Обработчик DELETE-запроса для удаления упражнения.

        Parameters:
            request (HttpRequest): Объект запроса от клиента.
            pk (int): Идентификатор упражнения, которое нужно удалить.

        Returns:
            JsonResponse: JSON-ответ с результатом удаления упражнения.

        """

        exercise = get_object_or_404(Exercise, pk=pk)
        exercise.delete()

        return JsonResponse(
            {
                'status': 'success',
                'message': 'Упражнение успешно удалено.'
            }
        )
