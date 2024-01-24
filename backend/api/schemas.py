from drf_yasg import openapi

APPOINTMENT_TAG = 'Талоны'
MAIN_TAG = 'Организации'
SPEC_TAG = 'Специальности врачей'
TOWN_TAG = 'Города'
MANAGMENT_ACCOUNT = "Управление учётной записью"

RESPONSE_404 = openapi.Response('Страница не найдена.',
                                examples={
                                    "application/json": {
                                        "detail": "Страница не найдена."}
                                })
RESPONSE_204_FOR_APPOINTMENT = openapi.Response('Нет контента')

RESPONSE_400_REGISTRATION = openapi.Response(
    'Пользователь с такой почтой уже существует!',
    examples={
        "application/json": {
            "detail": "Пользователь с такой почтой уже существует!"}
    })

RESPONSE_201_REGISTRATION = openapi.Response(
    'Пользователь успешно создан!',
    examples={
        "application/json": {
            "detail": "Пользователь успешно создан!"}
    })

RESPONSE_400_AUTHORIZATION = openapi.Response(
    'Неверное имя пользователя или пароль!',
    examples={
        "application/json": {
            "detail": "Неверное имя пользователя или пароль!"}
    })

RESPONSE_200_AUTHORIZATION = openapi.Response(
    'Авторизация успешна!',
    examples={
        "application/json": {
            "detail": "Авторизация успешна!",
            "access": "access_token",
            "refresh": "refresh_token"
        }
    })

RESPONSES_REGISTRATION = {
    '201': RESPONSE_201_REGISTRATION,
    '400': RESPONSE_400_REGISTRATION
}

RESPONSES_AUTHORIZATION = {
    '200': RESPONSE_200_AUTHORIZATION,
    '400': RESPONSE_400_AUTHORIZATION
}

RESPONSES_WITH_404 = {
    '404': RESPONSE_404
}

RESPONSES_FOR_APPOINTMENT = {
    '404': RESPONSE_404,
    '204': RESPONSE_204_FOR_APPOINTMENT
}

PARAMS_FOR_DISTANCE_FILTER = [
    openapi.Parameter("lat",
                      openapi.IN_QUERY,
                      type=openapi.TYPE_NUMBER,
                      default=54.51367),
    openapi.Parameter("long",
                      openapi.IN_QUERY,
                      type=openapi.TYPE_NUMBER,
                      default=36.26134),
]

ORGS_SCHEMAS = {
    "list":
        {
            "tags": [MAIN_TAG],
            "summary": "Список организаций",
            "description": ("Страница доступна всем. "
                            "Доступен поиск по наименованию организации. "
                            "Доступна фильтрация "
                            "по специальностям врачей, районам, "
                            "государственной или коммерческой организации,"
                            "а также по круглосуточным организациям"),
            "responses": [],
            "params": PARAMS_FOR_DISTANCE_FILTER
        },
    "retrieve":
        {
            "tags": [MAIN_TAG],
            "summary": "Получение организации",
            "description": "Страница доступна всем.",
            "responses": RESPONSES_WITH_404
        },
    "create":
        {
            "tags": [MAIN_TAG],
            "summary": "Добавление организации",
            "description": ('Страница доступна пользователям и '
                            'администраторам.'),
            "responses": []
        },
    "destroy":
        {
            "tags": [MAIN_TAG],
            "summary": "Удаление организации",
            "description": ('Страница доступна пользователям, создавшим '
                            'конкретную организацию (владельцам), и '
                            'администраторам.'),
            "responses": []
        },
    "partial_update":
        {
            "tags": [MAIN_TAG],
            "summary": "Обновление свойств организации",
            "description": ('Страница доступна пользователям, создавшим '
                            'конкретную организацию (владельцам), и '
                            'администраторам.'),
            "responses": []
        },
    "get_free_tickets":
        {
            "tags": [MAIN_TAG],
            "summary": "Получение списка талонов для записи на прием в "
                       "организацию",
            "description": 'Страница доступна всем.',
            "responses": [],
        }
}

SPEC_SCHEMAS = {
    "list":
        {
            "tags": [SPEC_TAG],
            "summary": "Список специальностей",
            "description": "Страница доступна всем.",
            "responses": []
        },
    "retrieve":
        {
            "tags": [SPEC_TAG],
            "summary": "Получение специальности",
            "description": "Страница доступна всем.",
            "responses": RESPONSES_WITH_404
        }
}

TOWN_SCHEMAS = {
    "list":
        {
            "tags": [TOWN_TAG],
            "summary": "Список городов",
            "description": "Страница доступна всем.",
            "responses": []
        },
    "retrieve":
        {
            "tags": [TOWN_TAG],
            "summary": "Получение города",
            "description": "Страница доступна всем.",
            "responses": RESPONSES_WITH_404
        }
}

APPOINT_SCHEMAS = {
    "update":
        {
            "tags": [APPOINTMENT_TAG],
            "summary": "Запись к врачу",
            "description": "Страница доступна всем.",
            "responses": RESPONSES_FOR_APPOINTMENT
        }
}

SIGNUP_SCHEMAS = {
    "post":
        {
            "tags": [MANAGMENT_ACCOUNT],
            "summary": "Создание нового пользователя",
            "description": "Используется для регистрации."
                           " Нужно ввести емейл и пароль.",
            "responses": RESPONSES_REGISTRATION
        }
}

LOGIN_SCHEMAS = {
    "post":
        {
            "tags": [MANAGMENT_ACCOUNT],
            "summary": "Авторизация существующего пользователя",
            "description": "Используется для авторизации по емейлу и паролю,"
                           " чтобы далее использовать токен при запросах.",
            "responses": RESPONSES_AUTHORIZATION
        }
}
