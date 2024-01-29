from drf_yasg import openapi

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
