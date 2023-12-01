import abc
from typing import Iterable

from organizations.models import Organization

from ._parsers import GenerateOrgParser


class Handler(abc.ABC):
    """
    Обработчик сведений об организациях.

    Методы
    -------
    handle()
        Абстрактный метод обработки. При наследовании логику
        переопределить
    """

    @abc.abstractmethod
    def handle(self):
        pass


class OrgSaver:
    """
    Сохранятор в БД сведений об организациях.

    Атрибуты
    ----------
    batch_size : int (по умолчанию 10 000)
        Максимальное количество сущностей на один `INSERT`

    Методы
    -------
    save(orgs: Iterable['Organization'])
        Порционно сохраняет сведения об организациях в БД
    """

    def __init__(self, batch_size: int = 10000) -> None:
        self.batch_size: int = batch_size

    def save(self, orgs: Iterable['Organization']) -> None:
        """
        Сохраняет в БД переданные организации.

        Параметры
        -------
        orgs : Iterable['Organization']
            Последовательность организаций, которые необходимо сохранить в БД
        """
        if orgs:
            Organization.objects.bulk_create(orgs, batch_size=self.batch_size)


class TestDataHandler(Handler):
    """
    Обработчик сведений о демонстрационных организациях.

    Атрибуты
    ----------
    num : int
        Количество демонстрационных организаций

    Методы
    -------
    handle()
        Управляет обработкой сведениями
    """

    def __init__(self, num: int):
        self.num = num

    def handle(self) -> dict:
        """
        Управляет обработкой сведениями о демонстрационных организациях.
        Создает несуществующие реквизиты организаций, сохраняет их в БД,
        возвращает словарь с результатами обработки.
        """
        parser = GenerateOrgParser(self.num)
        orgs, stats = parser.parse()
        OrgSaver().save(orgs)
        return {
            stats['counter_new']['verbose_name']: stats['counter_new']['value']
        }
