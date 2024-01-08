from drf_yasg import openapi

APPOINTMENT_TAG = 'Талоны'
MAIN_TAG = 'Организации'
SPEC_TAG = 'Специальности врачей'
TOWN_TAG = 'Города'

RESPONSE_404 = openapi.Response('Страница не найдена.',
                                examples={
                                    "application/json": {
                                        "detail": "Страница не найдена."}
                                })
RESPONSE_FOR_APPOINTMENT = openapi.Response('Нет контента')

RESPONSES_WITH_404 = {
    '404': RESPONSE_404
}

RESPONSES_FOR_APPOINTMENT = {
    '404': RESPONSE_404,
    '204': RESPONSE_FOR_APPOINTMENT
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
            "description": ("Страница доступна всем пользователям. "
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
            "description": "Страница доступна всем пользователям.",
            "responses": RESPONSES_WITH_404
        },
    "create":
        {
            "tags": [MAIN_TAG],
            "summary": "Добавление организации",
            "description": ('Страница доступна пользователям с ролями '
                            'пользователь и администратор.'),
            "responses": []
        },
    "destroy":
        {
            "tags": [MAIN_TAG],
            "summary": "Удаление организации",
            "description": ('Страница доступна пользователям с ролями '
                            'администратор и представитель больницы, который '
                            'создал эту больницу (OWNER)'),
            "responses": []
        },
    "partial_update":
        {
            "tags": [MAIN_TAG],
            "summary": "Обновление свойств организации",
            "description": ('Страница доступна пользователям с ролями'
                            'администратор и представитель больницы, который '
                            'создал эту больницу (OWNER)'),
            "responses": []
        },
    "get_free_tickets":
        {
            "tags": [MAIN_TAG],
            "summary": "Получение списка талонов для записи на прием в "
                       "организацию",
            "description": ('Страница доступна пользователям с ролями '
                            'пользователь и администратор.'),
            "responses": [],
        }
}

SPEC_SCHEMAS = {
    "list":
        {
            "tags": [SPEC_TAG],
            "summary": "Список специальностей",
            "description": "Страница доступна всем пользователям.",
            "responses": []
        },
    "retrieve":
        {
            "tags": [SPEC_TAG],
            "summary": "Получение специальности",
            "description": "Страница доступна всем пользователям.",
            "responses": RESPONSES_WITH_404
        }
}

TOWN_SCHEMAS = {
    "list":
        {
            "tags": [TOWN_TAG],
            "summary": "Список городов",
            "description": "Страница доступна всем пользователям.",
            "responses": []
        },
    "retrieve":
        {
            "tags": [TOWN_TAG],
            "summary": "Получение города",
            "description": "Страница доступна всем пользователям.",
            "responses": RESPONSES_WITH_404
        }
}

APPOINT_SCHEMAS = {
    "update":
        {
            "tags": [APPOINTMENT_TAG],
            "summary": "Запись к врачу",
            "description": "Страница доступна всем пользователям.",
            "responses": RESPONSES_FOR_APPOINTMENT
        }
}
