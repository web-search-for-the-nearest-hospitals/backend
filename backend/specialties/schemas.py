from drf_yasg import openapi

SPEC_TAG = 'Специальности врачей'

RESPONSE_404 = openapi.Response(
    'Страница не найдена.',
    examples={
        "application/json": {
            "detail": "Страница не найдена."}
    })

RESPONSES_WITH_404 = {
    '404': RESPONSE_404
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
