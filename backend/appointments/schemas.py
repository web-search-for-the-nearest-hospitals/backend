from drf_yasg import openapi

APPOINTMENT_TAG = 'Талоны'

RESPONSE_404 = openapi.Response(
    'Страница не найдена.',
    examples={
        "application/json": {
            "detail": "Страница не найдена."}
    })

RESPONSE_204_FOR_APPOINTMENT = openapi.Response('Нет контента')

RESPONSES_WITH_404 = {
    '404': RESPONSE_404
}

RESPONSES_FOR_APPOINTMENT = {
    '404': RESPONSE_404,
    '204': RESPONSE_204_FOR_APPOINTMENT
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
