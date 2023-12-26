from drf_yasg import openapi

MAIN_TAG = 'Организации'
SPEC_TAG = 'Специальности врачей'
TOWN_TAG = 'Города'

RESPONSES_FOR_404_ERROR = {
    '404': openapi.Response('Страница не найдена.',
                            examples={
                                "application/json": {
                                    "detail": "Страница не найдена."}
                            })
}

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
            "responses": []
        },
    "retrieve":
        {
            "tags": [MAIN_TAG],
            "summary": "Получение организации",
            "description": "Страница доступна всем пользователям.",
            "responses": RESPONSES_FOR_404_ERROR
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
            "responses": RESPONSES_FOR_404_ERROR
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
            "responses": RESPONSES_FOR_404_ERROR
        }
}
