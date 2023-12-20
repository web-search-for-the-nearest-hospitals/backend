from django.conf import settings


def test_secret_key_set():
    """ Проверка, что секретный ключ установлен."""
    assert settings.SECRET_KEY, "SECRET_KEY должен быть установлен."


def test_debug_mode_disabled():
    """Проверка, что режим DEBUG отключен в продакшн."""
    assert not settings.DEBUG, "Режим DEBUG должен быть отключен в продакшн."


def test_allowed_hosts_set():
    """Проверка, что ALLOWED_HOSTS установлен"""
    assert settings.ALLOWED_HOSTS, "ALLOWED_HOSTS должен быть установлен."


def test_static_url_set():
    """Проверка, что STATIC_URL установлен."""
    assert settings.STATIC_URL, "STATIC_URL должен быть установлен."


def test_media_url_set():
    """Проверка, что MEDIA_URL установлен."""
    assert settings.MEDIA_URL, "MEDIA_URL должен быть установлен."


def test_default_auto_field_set():
    """Проверка, что DEFAULT_AUTO_FIELD установлен."""
    assert settings.DEFAULT_AUTO_FIELD, (
        "DEFAULT_AUTO_FIELD должен быть установлен.")


def test_database_settings():
    """Проверка настройок базы данных."""
    assert settings.DATABASES['default']['ENGINE'], (
        "DB_ENGINE должен быть установлен.")
    assert settings.DATABASES['default']['NAME'], (
        "DB_NAME должен быть установлен.")
    assert settings.DATABASES['default']['USER'], (
        "POSTGRES_USER должен быть установлен.")
    assert settings.DATABASES['default']['PASSWORD'], (
        "POSTGRES_PASSWORD должен быть установлен.")
    assert settings.DATABASES['default']['HOST'], (
        "DB_HOST должен быть установлен.")
    assert settings.DATABASES['default']['PORT'], (
        "DB_PORT должен быть установлен.")
