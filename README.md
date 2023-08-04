# API методы

Данный API предоставляет возможность управления информацией о докторах, пациентах и упражнениях.

## Установка и запуск

1. Убедитесь, что у вас установлен Python версии 3.x.
2. Установите зависимости, выполнив команду: `pip install -r requirements.txt`.
3. Запустите сервер, выполните: `python manage.py runserver`.

## Доступные методы API

### `api/doctor/`

#### Описание

Метод для получения списка всех докторов или создания нового доктора.

#### Методы

- `GET`: Возвращает список всех докторов.

  **Параметры запроса**: Отсутствуют.

  **Параметры ответа**:
  
  - `id` (int): Идентификатор доктора.
  - `name` (str): Имя доктора.
  - `speciality` (int): Идентификатор специальности доктора.

- `POST`: Создает нового доктора.

  **Параметры запроса**:
  
  - `name` (str, обязательный): Имя нового доктора.
  - `speciality` (int, обязательный): Идентификатор специальности нового доктора.

  **Параметры ответа**:
  
  - `status` (str): Статус операции ("success" или "error").
  - `message` (str): Сообщение о результате операции.

### `api/doctor/<int:pk>/`

#### Описание

Метод для получения информации о конкретном докторе, обновления его данных или удаления.

#### Методы

- `GET`: Возвращает информацию о конкретном докторе.

  **Параметры запроса**: Отсутствуют.

  **Параметры ответа**:
  
  - `id` (int): Идентификатор доктора.
  - `name` (str): Имя доктора.
  - `speciality` (int): Идентификатор специальности доктора.

- `PUT`: Обновляет данные конкретного доктора.

  **Параметры запроса**:
  
  - `name` (str, обязательный): Новое имя доктора.
  - `speciality` (int, обязательный): Новый идентификатор специальности доктора.

  **Параметры ответа**:
  
  - `status` (str): Статус операции ("success" или "error").
  - `message` (str): Сообщение о результате операции.

- `PATCH`: Частично обновляет данные конкретного доктора.

  **Параметры запроса**:
  
  - `name` (str, необязательный): Новое имя доктора.
  - `speciality` (int, необязательный): Новый идентификатор специальности доктора.

  **Параметры ответа**:
  
  - `status` (str): Статус операции ("success" или "error").
  - `message` (str): Сообщение о результате операции.

- `DELETE`: Удаляет конкретного доктора.

  **Параметры запроса**: Отсутствуют.

  **Параметры ответа**:
  
  - `status` (str): Статус операции ("success" или "error").
  - `message` (str): Сообщение о результате операции.

### `api/doctor/<int:pk>/exercises/`

#### Описание

Метод для получения списка упражнений, которые назначены конкретному доктору.

#### Методы

- `GET`: Возвращает список упражнений, назначенных конкретному доктору.

  **Параметры запроса**: Отсутствуют.

  **Параметры ответа**:
  
  - `id` (int): Идентификатор упражнения.
  - `title` (str): Название упражнения.
  - `description` (str): Описание упражнения.
  - `frequency` (str): Частота выполнения упражнения (может быть "every_hour", "every_day", "every_week" или "every_month").

### `api/doctor/<int:pk>/appoint/`

#### Описание

Метод для назначения нового упражнения пациенту конкретным доктором.

#### Методы

- `POST`: Назначает новое упражнение пациенту конкретным доктором.

  **Параметры запроса**:
  
  - `patient` (int, обязательный): Идентификатор пациента, которому назначается упражнение.
  - `exercise` (int, обязательный): Идентификатор упражнения, которое назначается.
  - `appointment_date` (str, обязательный): Дата назначения упражнения в формате "YYYY-MM-DD HH:MM".

  **Параметры ответа**:
  
  - `status` (str): Статус операции ("success" или "error").
  - `message` (str): Сообщение о результате операции.

### `api/patient/`

#### Описание

Метод для получения списка всех пациентов или создания нового пациента.

#### Методы

- `GET`: Возвращает список всех пациентов.

  **Параметры запроса**: Отсутствуют.

  **Параметры ответа**:
  
  - `id` (int): Идентификатор пациента.
  - `name` (str): Имя пациента.

- `POST`: Создает нового пациента.

  **Параметры запроса**:
  
  - `name` (str, обязательный): Имя нового пациента.

  **Параметры ответа**:
  
  - `status` (str): Статус операции ("success" или "error").
  - `message` (str): Сообщение о результате операции.

### `api/patient/<int:pk>/`

#### Описание

Метод для получения информации о конкретном пациенте, обновления его данных или удаления.

#### Методы

- `GET`: Возвращает информацию о конкретном пациенте.

  **Параметры запроса**: Отсутствуют.

  **Параметры ответа**:
  
  - `id` (int): Идентификатор пациента.
  - `name` (str): Имя пациента.

- `PUT`: Обновляет данные конкретного пациента.

  **Параметры запроса**:
  
  - `name` (str, обязательный): Новое имя пациента.

  **Параметры ответа**:
  
  - `status` (str): Статус операции ("success" или "error").
  - `message` (str): Сообщение о результате операции.

- `PATCH`: Частично обновляет данные конкретного пациента.

  **Параметры запроса**:
  
  - `name` (str, необязательный): Новое имя пациента.

  **Параметры ответа**:
  
  - `status` (str): Статус операции ("success" или "error").
  - `message` (str): Сообщение о результате операции.

- `DELETE`: Удаляет конкретного пациента.

  **Параметры запроса**: Отсутствуют.

  **Параметры ответа**:
  
  - `status` (str): Статус операции ("success" или "error").
  - `message` (str): Сообщение о результате операции.

### `api/patient/<int:pk>/exercises/`

#### Описание

Метод для получения списка упражнений, назначенных конкретному пациенту.

#### Методы

- `GET`: Возвращает список упражнений, назначенных конкретному пациенту.

  **Параметры запроса**: Отсутствуют.

  **Параметры ответа**:
  
  - `id` (int): Идентификатор упражнения.
  - `title` (str): Название упражнения.
  - `description` (str): Описание упражнения.
  - `frequency` (str): Частота выполнения упражнения (может быть "every_hour", "every_day", "every_week" или "every_month").

### `api/exercise/`

#### Описание

Метод для получения списка всех упражнений или создания нового упражнения.

#### Методы

- `GET`: Возвращает список всех упражнений.

  **Параметры запроса**: Отсутствуют.

  **Параметры ответа**:
  
  - `id` (int): Идентификатор упражнения.
  - `title` (str): Название упражнения.
  - `description` (str): Описание упражнения.
  - `frequency` (str): Частота выполнения упражнения (может быть "every_hour", "every_day", "every_week" или "every_month").

- `POST`: Создает новое упражнение.

  **Параметры запроса**:
  
  - `title` (str, обязательный): Название нового упражнения.
  - `description` (str, обязательный): Описание нового упражнения.
  - `frequency` (str, обязательный): Частота выполнения упражнения (может быть "every_hour", "every_day", "every_week" или "every_month").

  **Параметры ответа**:
  
  - `status` (str): Статус операции ("success" или "error").
  - `message` (str): Сообщение о результате операции.

### `api/exercise/<int:pk>/`

#### Описание

Метод для получения информации о конкретном упражнении, обновления его данных или удаления.

#### Методы

- `GET`: Возвращает информацию о конкретном упражнении.

  **Параметры запроса**: Отсутствуют.

  **Параметры ответа**:
  
  - `id` (int): Идентификатор упражнения.
  - `title` (str): Название упражнения.
  - `description` (str): Описание упражнения.
  - `frequency` (str): Частота выполнения упражнения (может быть "every_hour", "every_day", "every_week" или "every_month").

- `PUT`: Обновляет данные конкретного упражнения.

  **Параметры запроса**:
  
  - `title` (str, обязательный): Новое название упражнения.
  - `description` (str, обязательный): Новое описание упражнения.
  - `frequency` (str, обязательный): Новая частота выполнения упражнения (может быть "every_hour", "every_day", "every_week" или "every_month").

  **Параметры ответа**:
  
  - `status` (str): Статус операции ("success" или "error").
  - `message` (str): Сообщение о результате операции.

- `PATCH`: Частично обновляет данные конкретного упражнения.

  **Параметры запроса**:
  
  - `title` (str, необязательный): Новое название упражнения.
  - `description` (str, необязательный): Новое описание упражнения.
  - `frequency` (str, необязательный): Новая частота выполнения упражнения (может быть "every_hour", "every_day", "every_week" или "every_month").

  **Параметры ответа**:
  
  - `status` (str): Статус операции ("success" или "error").
  - `message` (str): Сообщение о результате операции.

- `DELETE`: Удаляет конкретное упражнение.

  **Параметры запроса**: Отсутствуют.

  **Параметры ответа**:
  
  - `status` (str): Статус операции ("success" или "error").
  - `message` (str): Сообщение о результате операции.