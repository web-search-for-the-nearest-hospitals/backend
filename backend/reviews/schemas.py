from drf_yasg import openapi

REVIEW_TAG = 'Отзывы'

RESPONSE_401 = openapi.Response(
    'Отзыв могут оставлять только авторизованные пользователи',
    examples={
        "application/json": {
            "detail": "Отзыв могут оставлять "
                      "только авторизованные пользователи"}
    }
)
RESPONSE_200 = openapi.Response(
    'Все отзывы',
    examples={
        "application/json": {
            "detail": "Успешный запрос!",
            "id": 0,
            "text": "string",
            "author": "string",
            "score": 1,
            "pub_date": "2019-08-24T14:15:22Z"
        }
    }
)

RESPONSES_REVIEWS = {
    '200': RESPONSE_200,
    '401': RESPONSE_401
}

REVIEWS_SCHEMAS = {
    "list":
        {
            "tags": [REVIEW_TAG],
            "summary": "Отзывы",
            "description": "Получение всех отзывов",
            "responses": []
        },
    "create":
        {
            "tags": [REVIEW_TAG],
            "summary": "Добавление отзыва",
            "description": "Отзыв может оставить "
                           "только зарегистрированный пользователь",
            "responses": RESPONSES_REVIEWS
        },
}
