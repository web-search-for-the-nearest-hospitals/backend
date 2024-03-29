from drf_yasg import openapi

REVIEW_TAG = 'Отзывы'

PARAMS_FOR_UUID = [
    openapi.Parameter("uuid",
                      openapi.IN_PATH,
                      type=openapi.FORMAT_UUID,
                      description="Уникальный идентификатор организации",
                      ),

]

RESPONSE_401 = openapi.Response(
    'Отзыв могут оставлять только авторизованные пользователи',
    examples={
        "application/json": {
            "detail": "Отзыв могут оставлять "
                      "только авторизованные пользователи"}
    }
)
RESPONSE_201 = openapi.Response(
    'Все отзывы',
    examples={
        "application/json": {
            "text": "string",
            "first_name": "string",
            "score": 1,
            "pub_date": "2019-08-24T14:15:22Z"
        }
    }
)

RESPONSES_REVIEWS = {
    '201': RESPONSE_201,
    '401': RESPONSE_401
}

REVIEWS_SCHEMAS = {
    "list":
        {
            "tags": [REVIEW_TAG],
            "summary": "Отзывы",
            "description": "Получение всех отзывов",
            "responses": [],
            "params": PARAMS_FOR_UUID
        },
    "create":
        {
            "tags": [REVIEW_TAG],
            "summary": "Добавление отзыва",
            "description": "Отзыв может оставить "
                           "только зарегистрированный пользователь",
            "responses": RESPONSES_REVIEWS,
            "params": PARAMS_FOR_UUID
        },
}
