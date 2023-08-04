from django.db import models


class Speciality(models.Model):
    """
    Сущность "Специальность".

    Attributes:
        title (CharField): Название специальности. Поле типа CharField, максимальная длина 64 символа.
    """

    title = models.CharField('title', max_length=64)

    def __str__(self):
        """
        Возвращает строковое представление объекта специальности.

        Returns:
            str: Строковое представление названия специальности.
        """
        return self.title


class Exercise(models.Model):
    """
    Сущность "Упражнение".

    Attributes:
        EVERY_HOUR (str): Константа для частоты выполнения "Каждый час".
        EVERY_DAY (str): Константа для частоты выполнения "Каждый день".
        EVERY_WEEK (str): Константа для частоты выполнения "Каждую неделю".
        EVERY_MONTH (str): Константа для частоты выполнения "Каждый месяц".
        EXERCISE_FREQUENCY (list of tuple): Список с кортежами частот выполнения упражнений.
            Каждый кортеж содержит два элемента: строковый идентификатор частоты и текстовое описание частоты.

        title (CharField): Название упражнения. Поле типа CharField, максимальная длина 128 символов.
        description (CharField): Описание упражнения. Поле типа CharField, максимальная длина 1024 символа.
        frequency (CharField): Частота выполнения упражнения. Поле типа CharField с ограниченными вариантами
            выбора из списка EXERCISE_FREQUENCY. По умолчанию установлено значение "Каждый день".
        specialisations (ManyToManyField): Связь с моделью Speciality для определения специализаций, к которым
            относится упражнение.

    Methods:
        __str__(): Возвращает строковое представление объекта упражнения (название упражнения).

    """
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
        """
        Возвращает строковое представление объекта упражнения (название упражнения).

        Returns:
            str: Строковое представление названия упражнения.
        """
        return self.title


class Patient(models.Model):
    """
    Сущность "Пациент".

    Attributes:
        name (CharField): Имя пациента. Поле типа CharField, максимальная длина 128 символов.

    Methods:
        __str__(): Возвращает строковое представление объекта пациента (имя пациента).

    """
    name = models.CharField('name', max_length=128)

    def __str__(self):
        """
        Возвращает строковое представление объекта пациента (имя пациента).

        Returns:
            str: Строковое представление имени пациента.
        """
        return self.name


class Doctor(models.Model):
    """
    Сущность "Врач".

    Attributes:
        name (CharField): Имя врача. Поле типа CharField, максимальная длина 128 символов.
        speciality (ForeignKey): Специальность врача. Внешний ключ на модель Speciality,
                                 с вариантом удаления CASCADE.
        patients (ManyToManyField): Пациенты, связанные с врачом. Множественное отношение "многие ко многим"
                                   с моделью Patient.

    Methods:
        __str__(): Возвращает строковое представление объекта врача.

    """
    name = models.CharField('name', max_length=128)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    patients = models.ManyToManyField(Patient)

    def __str__(self):
        """
        Возвращает строковое представление объекта врача.

        Returns:
            str: Строковое представление объекта врача в формате "Имя: <имя врача>, Специальность: <специальность>".
        """
        return f"Имя: {self.name}, Специальность: {self.speciality}"


class Appointment(models.Model):
    """
    Сущность "Назначение".

    Attributes:
        doctor (ForeignKey): Внешний ключ на модель Doctor. Ссылается на врача, связанного с назначением.
                             С вариантом удаления CASCADE, что означает удаление связанного назначения при удалении врача.
        patient (ForeignKey): Внешний ключ на модель Patient. Ссылается на пациента, связанного с назначением.
                              С вариантом удаления CASCADE, что означает удаление связанного назначения при удалении пациента.
        exercise (ForeignKey): Внешний ключ на модель Exercise. Ссылается на упражнение, связанное с назначением.
                               С вариантом удаления CASCADE, что означает удаление связанного назначения при удалении упражнения.
        appointment_date (DateTimeField): Дата назначения упражнения. Поле типа DateTimeField.

    Methods:
        __str__(): Возвращает строковое представление объекта назначения.

    """
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField('Дата назначения')

    def __str__(self):
        """
        Возвращает строковое представление объекта назначения.

        Returns:
            str: Строковое представление объекта назначения в формате "Доктор: <имя врача>, Пациент: <имя пациента>,
                 Упражнение: <название упражнения>".
        """
        return f"Доктор: {self.doctor.name}, Пациент: {self.patient.name}, Упражнение: {self.exercise.title}"
