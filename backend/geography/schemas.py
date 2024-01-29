from drf_yasg import openapi

TOWN_TAG = 'Города'

RESPONSE_404 = openapi.Response(
    'Страница не найдена.',
    examples={
        "application/json": {
            "detail": "Страница не найдена."}
    })

RESPONSES_WITH_404 = {
    '404': RESPONSE_404
}

PARAMS_FOR_TOWN = [
    openapi.Parameter('id', openapi.IN_PATH,
                      description="ID города",
                      type=openapi.TYPE_INTEGER)
]

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
            "responses": RESPONSES_WITH_404,
            "params": PARAMS_FOR_TOWN

        },
    'get_specialties':
        {
            "tags": [TOWN_TAG],
            "summary": "Получение списка специальностей врачей,"
                       " имеющихся в городе",
            "description": "Страница доступна всем.",
            "responses": RESPONSE_404,
            "params": PARAMS_FOR_TOWN
        }
}
